#!/usr/bin/env python
"""
Parallel multi-device test runner for the Luna Pytest-BDD framework.

Runs a different feature (pytest marker) on each connected Android device
*simultaneously*, with every device fully isolated:

  * its own Appium server   (unique --port + systemPort + mjpegServerPort)
  * its own .env            (unique UDID / DEVICE_NAME / APPIUM_SERVER)
  * its own Allure results  (parallel/_output/allure-results/<udid>)

The existing framework is NOT modified. conftest.py already loads the .env from
the *current working directory* (`Path(os.getcwd()) / ".env"`), so this runner
simply launches each pytest process inside a per-device working directory that
contains a generated .env. All runner state lives under parallel/_output/.

Usage (from the project root, with myenv activated):

    # Use the default marker defined per-device in devices.json
    python parallel/run_parallel.py

    # Assign markers by device order (1st token -> 1st device in devices.json)
    python parallel/run_parallel.py heart_rate stress

    # Assign explicitly with marker@udid (order/count independent)
    python parallel/run_parallel.py heart_rate@70f31eb6b9fc stress@TWL77DU8U4TKIBYT

Options:
    --list          Print the resolved device/marker assignments and exit.
    --collect-only  Only collect tests per device (fast config sanity check; no
                    Appium server / no device session needed).
    --no-appium     Do not start/stop Appium servers (assume already running on
                    the ports in devices.json).
    --keep-appium   Leave runner-started Appium servers running after the tests.
    --report        After the run, generate + open a combined Allure report.
"""
from __future__ import annotations

import argparse
import json
import os
import socket
import subprocess
import sys
import threading
import time
import urllib.request
from pathlib import Path

PARALLEL_DIR = Path(__file__).resolve().parent
ROOT = PARALLEL_DIR.parent
OUTPUT = PARALLEL_DIR / "_output"
WORK_DIR = OUTPUT / "work"
LOG_DIR = OUTPUT / "logs"
ALLURE_DIR = OUTPUT / "allure-results"
DEVICES_JSON = PARALLEL_DIR / "devices.json"
SOURCE_ENV = ROOT / ".env"

IS_WINDOWS = os.name == "nt"


# ── config ───────────────────────────────────────────────────────────────────
def load_config() -> dict:
    with DEVICES_JSON.open("r", encoding="utf-8") as f:
        return json.load(f)


def resolve_assignments(cfg: dict, tokens: list[str]) -> list[tuple[dict, str]]:
    """Map (device -> marker). See module docstring for the token forms."""
    devices = cfg["devices"]
    by_udid = {d["udid"]: d for d in devices}

    if not tokens:
        return [(d, d["marker"]) for d in devices]

    if any("@" in t for t in tokens):
        assignments = []
        for t in tokens:
            if "@" not in t:
                raise SystemExit(f"Mix of '@' and plain tokens not allowed: {t!r}")
            marker, _, udid = t.partition("@")
            if udid not in by_udid:
                raise SystemExit(f"Unknown udid {udid!r}. Known: {list(by_udid)}")
            assignments.append((by_udid[udid], marker))
        return assignments

    if len(tokens) > len(devices):
        raise SystemExit(f"Got {len(tokens)} markers but only {len(devices)} devices.")
    return [(devices[i], tokens[i]) for i in range(len(tokens))]


# ── networking helpers ─────────────────────────────────────────────────────────
def port_open(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex((host, port)) == 0


def wait_for_status(host: str, port: int, base_path: str, timeout: float = 60.0) -> bool:
    url = f"http://{host}:{port}{base_path.rstrip('/')}/status"
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=2) as r:
                if r.status == 200:
                    return True
        except Exception:
            time.sleep(1)
    return False


# ── appium lifecycle ────────────────────────────────────────────────────────────
def start_appium(dev: dict, host: str, base_path: str) -> subprocess.Popen | None:
    """Start an Appium server for a device. Returns the Popen we own, or None if a
    server is already listening on that port (we then reuse it, don't kill it)."""
    port = dev["appium_port"]
    if port_open(host, port):
        print(f"[{short(dev)}] Appium already on {host}:{port} -> reusing (won't stop it)")
        return None

    work = WORK_DIR / dev["udid"]
    work.mkdir(parents=True, exist_ok=True)
    platform = str(dev.get("platform", "Android")).lower()
    caps = {"appium:udid": dev["udid"]}
    if platform == "ios":
        # iOS / XCUITest: a unique WebDriverAgent port per device keeps parallel
        # sessions from clashing (the Android systemPort has no iOS equivalent).
        if dev.get("wda_local_port"):
            caps["appium:wdaLocalPort"] = dev["wda_local_port"]
    else:
        # Android / UiAutomator2: unique bridge ports per device + the OnePlus/OPPO/
        # Xiaomi/Realme workaround (their ROMs deny WRITE_SECURE_SETTINGS to the adb
        # shell, which otherwise fails UiAutomator2's hidden_api_policy setup).
        caps["appium:systemPort"] = dev["system_port"]
        caps["appium:mjpegServerPort"] = dev["mjpeg_port"]
        caps["appium:ignoreHiddenApiPolicyError"] = True
    # Per-device overrides via "extra_caps" in devices.json (e.g. iOS bundleId, or the
    # OnePlus enforceXpath1 fix).
    caps.update(dev.get("extra_caps", {}))
    caps_file = work / "default_caps.json"
    caps_file.write_text(json.dumps(caps), encoding="utf-8")

    appium_log = LOG_DIR / f"appium_{dev['udid']}.log"
    cmd = [
        "cmd", "/c", "appium",
        "--address", host,
        "--port", str(port),
        "--base-path", base_path,
        "--default-capabilities", str(caps_file),
        "--log", str(appium_log),
        "--log-level", "info",
    ] if IS_WINDOWS else [
        "appium",
        "--address", host, "--port", str(port), "--base-path", base_path,
        "--default-capabilities", str(caps_file),
        "--log", str(appium_log), "--log-level", "info",
    ]
    port_note = dev.get("system_port") or dev.get("wda_local_port") or "-"
    print(f"[{short(dev)}] starting Appium on :{port} (bridge port {port_note}) -> {appium_log.name}")
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return proc


def kill_proc_tree(proc: subprocess.Popen) -> None:
    if proc is None or proc.poll() is not None:
        return
    try:
        if IS_WINDOWS:
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            proc.terminate()
    except Exception as e:
        print(f"  (could not kill pid {proc.pid}: {e})")


# ── per-device .env ─────────────────────────────────────────────────────────────
def write_device_env(dev: dict, appium_url: str) -> Path:
    """Copy the project .env verbatim into the device work dir, then append the
    device-specific overrides. conftest loads with override=True, and python-dotenv
    keeps the LAST assignment of a duplicate key, so the appended lines win.
    Nothing in the source .env is lost (secrets, HEALTH_TARGET_DATE, etc. carry over)."""
    work = WORK_DIR / dev["udid"]
    work.mkdir(parents=True, exist_ok=True)

    base = SOURCE_ENV.read_text(encoding="utf-8") if SOURCE_ENV.exists() else ""
    platform = dev.get("platform", "Android")
    automation = dev.get("automation_name") or ("XCUITest" if str(platform).lower() == "ios" else "UiAutomator2")
    overrides = "\n".join([
        "",
        f"# ===== parallel runner overrides for device {dev['udid']} =====",
        f"PLATFORM_NAME={platform}",
        f"AUTOMATION_NAME={automation}",
        f"APPIUM_SERVER={appium_url}",
        f"UDID={dev['udid']}",
        f"DEVICE_NAME={dev['name']}",
        f"PLATFORM_VERSION={dev.get('platform_version', '')}",
        "IMPLICIT_WAIT=0",
        "",
    ])
    env_path = work / ".env"
    env_path.write_text(base.rstrip() + "\n" + overrides, encoding="utf-8")
    return work


# ── pytest launch + live output ──────────────────────────────────────────────────
def build_pytest_cmd(marker=None, node_ids=None, allure_dir=None, junit_path=None,
                     clean_allure=True, extra=None):
    """Assemble a device-agnostic pytest command. Reused by the CLI and the
    dashboard backend so both run tests identically. `node_ids` (to run specific
    tests) must be ABSOLUTE node ids, since the process cwd is a per-device work
    dir. An absolute `allure_dir` overrides the relative one in pytest.ini."""
    cmd = [sys.executable, "-m", "pytest",
           "-c", str(ROOT / "pytest.ini"), "--rootdir", str(ROOT),
           "-p", "no:cacheprovider"]
    if marker:
        cmd += ["-m", marker]
    if node_ids:
        cmd += list(node_ids)
    else:
        cmd += [str(ROOT / "features" / "steps")]
    if allure_dir:
        cmd += ["--alluredir", str(allure_dir)]
        if clean_allure:
            cmd += ["--clean-alluredir"]
    if junit_path:
        cmd += ["--junitxml", str(junit_path)]
    if extra:
        cmd += list(extra)
    cmd += ["-v"]
    return cmd


def launch_pytest(dev: dict, marker: str, work: Path, collect_only: bool) -> subprocess.Popen:
    allure_out = ALLURE_DIR / dev["udid"]
    allure_out.mkdir(parents=True, exist_ok=True)
    cmd = build_pytest_cmd(marker=marker, allure_dir=allure_out,
                           extra=(["--collect-only"] if collect_only else None))

    env = os.environ.copy()
    # Belt-and-suspenders: also expose the values via process env. The generated
    # .env still wins (override=True), this just avoids surprises if cwd changes.
    env["APPIUM_SERVER"] = f"http://{load_config()['appium']['host']}:{dev['appium_port']}"
    env["UDID"] = dev["udid"]
    # conftest writes the Allure environment.* files to ALLURE_RESULTS_DIR; point it
    # at this device's results dir so that env info lands with the results.
    env["ALLURE_RESULTS_DIR"] = str(allure_out)
    # Stream the child's stdout line-by-line instead of block-buffering it through
    # the pipe, so the live per-device log is real-time.
    env["PYTHONUNBUFFERED"] = "1"

    return subprocess.Popen(
        cmd, cwd=str(work), env=env,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, bufsize=1, encoding="utf-8", errors="replace",
    )


def _console_write(text: str) -> None:
    """Write to the console WITHOUT ever crashing on characters the console
    codepage (e.g. Windows cp1252) can't encode. A raw sys.stdout.write can raise
    UnicodeEncodeError on chars like '–' or '\\ufffd'; if the pump thread died on
    that, its subprocess pipe would fill and the pytest process would hang. So we
    fall back to an encode/decode with errors='replace' and never propagate."""
    try:
        sys.stdout.write(text)
    except UnicodeEncodeError:
        enc = sys.stdout.encoding or "utf-8"
        sys.stdout.write(text.encode(enc, "replace").decode(enc, "replace"))
    except Exception:
        pass
    try:
        sys.stdout.flush()
    except Exception:
        pass


def pump(proc: subprocess.Popen, prefix: str, log_path: Path) -> None:
    with log_path.open("w", encoding="utf-8") as lf:
        for line in proc.stdout:
            lf.write(line)
            lf.flush()
            _console_write(f"{prefix} {line}")


def short(dev: dict) -> str:
    return dev["name"]


# ── report ──────────────────────────────────────────────────────────────────────
def build_report() -> None:
    result_dirs = [str(p) for p in sorted(ALLURE_DIR.glob("*")) if p.is_dir()]
    if not result_dirs:
        print("No allure results found to report.")
        return
    report_out = OUTPUT / "allure-report"
    prefix = ["cmd", "/c"] if IS_WINDOWS else []
    print("Generating combined Allure report from:", result_dirs)
    subprocess.run(prefix + ["allure", "generate", *result_dirs, "-o", str(report_out), "--clean"])
    subprocess.run(prefix + ["allure", "open", str(report_out)])


# ── main ──────────────────────────────────────────────────────────────────────────
def main() -> int:
    ap = argparse.ArgumentParser(description="Parallel multi-device Luna test runner")
    ap.add_argument("markers", nargs="*", help="marker tokens, e.g. 'heart_rate stress' or 'heart_rate@<udid>'")
    ap.add_argument("--list", action="store_true", help="print resolved assignments and exit")
    ap.add_argument("--collect-only", action="store_true", help="only collect tests (no device needed)")
    ap.add_argument("--no-appium", action="store_true", help="do not manage Appium servers")
    ap.add_argument("--keep-appium", action="store_true", help="leave runner-started Appium servers up")
    ap.add_argument("--report", action="store_true", help="generate + open combined Allure report at the end")
    args = ap.parse_args()

    # Make console output robust to non-codepage chars (en-dash, replacement char)
    # so mirroring test output never crashes the pump threads (which would hang the
    # child pytest processes by leaving their stdout pipe undrained).
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    cfg = load_config()
    host = cfg["appium"]["host"]
    base_path = cfg["appium"].get("base_path", "/")
    assignments = resolve_assignments(cfg, args.markers)

    for d in (WORK_DIR, LOG_DIR, ALLURE_DIR):
        d.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("Parallel run plan:")
    for dev, marker in assignments:
        url = f"http://{host}:{dev['appium_port']}"
        print(f"  {dev['name']:<18} udid={dev['udid']:<18} marker={marker:<12} appium={url}")
    print("=" * 70)
    if args.list:
        return 0

    manage_appium = not args.no_appium and not args.collect_only
    started: list[subprocess.Popen] = []
    try:
        # 1) start (or reuse) an Appium server per device, then wait until each is ready
        if manage_appium:
            for dev, _ in assignments:
                p = start_appium(dev, host, base_path)
                if p is not None:
                    started.append(p)
            for dev, _ in assignments:
                if not wait_for_status(host, dev["appium_port"], base_path):
                    print(f"[{short(dev)}] ERROR: Appium :{dev['appium_port']} not ready in time; "
                          f"see {LOG_DIR / ('appium_' + dev['udid'] + '.log')}")
                else:
                    print(f"[{short(dev)}] Appium ready on :{dev['appium_port']}")

        # 2) launch all pytest processes concurrently
        procs: list[tuple[dict, str, subprocess.Popen, threading.Thread]] = []
        for dev, marker in assignments:
            work = write_device_env(dev, f"http://{host}:{dev['appium_port']}")
            proc = launch_pytest(dev, marker, work, args.collect_only)
            log_path = LOG_DIR / f"pytest_{dev['udid']}.log"
            prefix = f"[{marker}|{dev['name']}]"
            t = threading.Thread(target=pump, args=(proc, prefix, log_path), daemon=True)
            t.start()
            procs.append((dev, marker, proc, t))
            print(f"{prefix} launched pytest (pid {proc.pid}) -> {log_path.name}")

        # 3) wait for all (continue-on-fail: never abort the others)
        results = []
        for dev, marker, proc, t in procs:
            proc.wait()
            t.join()
            results.append((dev, marker, proc.returncode))

        # 4) summary
        print("\n" + "=" * 70)
        print("RESULTS")
        exit_code = 0
        for dev, marker, rc in results:
            status = "PASS" if rc == 0 else f"FAIL (exit {rc})"
            if rc != 0:
                exit_code = 1
            print(f"  {dev['name']:<18} {marker:<12} {status}")
        print(f"  Allure results: {ALLURE_DIR}")
        print(f"  Logs:           {LOG_DIR}")
        print("=" * 70)
    finally:
        if manage_appium and not args.keep_appium and started:
            print("Stopping runner-started Appium servers...")
            for p in started:
                kill_proc_tree(p)

    if args.report:
        build_report()
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
