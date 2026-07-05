#!/usr/bin/env python
"""
Luna Automation Dashboard — Flask backend.

Control the Sleep / Heart Rate / Stress Appium suites from a web UI: run a full
suite or a single test case, on a per-feature mapped device, several features at
once (parallel across devices), with live logs and a post-run results summary.

Reuses the device-isolation engine already built in parallel/run_parallel.py
(per-device Appium server, per-device .env, OnePlus caps). The existing framework
(conftest.py / pytest.ini / .env / pages / features) is NOT modified.

Run:  dashboard\run_dashboard.bat   (or: python dashboard\app.py)  -> http://127.0.0.1:5000
"""
from __future__ import annotations

import atexit
import json
import os
import re
import subprocess
import sys
import threading
import time
import xml.etree.ElementTree as ET
from pathlib import Path

from flask import Flask, jsonify, request, send_file

DASH_DIR = Path(__file__).resolve().parent
ROOT = DASH_DIR.parent
OUTPUT = DASH_DIR / "_output"
CONFIG_PATH = DASH_DIR / "config.json"

# Reuse the parallel runner's device-isolation primitives.
sys.path.insert(0, str(ROOT / "parallel"))
import run_parallel as rp  # noqa: E402

app = Flask(__name__)


# ── CORS (so a remotely-hosted UI, e.g. on Vercel, can call this local backend) ──
@app.after_request
def _add_cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resp


@app.before_request
def _preflight():
    if request.method == "OPTIONS":
        return ("", 204)


# ── config ─────────────────────────────────────────────────────────────────────
_config_lock = threading.Lock()


def load_dashboard_config() -> dict:
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_feature_device_map(mapping: dict) -> None:
    with _config_lock:
        cfg = load_dashboard_config()
        cfg["feature_device_map"] = mapping
        with CONFIG_PATH.open("w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2, ensure_ascii=False)


def devices_config() -> dict:
    """{udid: device-dict} from parallel/devices.json (ports, caps, name)."""
    return {d["udid"]: d for d in rp.load_config()["devices"]}


def appium_settings() -> tuple[str, str]:
    ap = rp.load_config().get("appium", {})
    return ap.get("host", "127.0.0.1"), ap.get("base_path", "/")


# ── adb / device discovery ──────────────────────────────────────────────────────
def adb_connected() -> set[str]:
    try:
        out = subprocess.run(["adb", "devices"], capture_output=True, text=True, timeout=10).stdout
    except Exception:
        return set()
    ids = set()
    for line in out.splitlines()[1:]:
        parts = line.split()
        if len(parts) >= 2 and parts[1] == "device":
            ids.add(parts[0])
    return ids


def _ios_tool_present() -> bool:
    try:
        subprocess.run(["idevice_id", "-h"], capture_output=True, timeout=5)
        return True
    except Exception:
        return False


def connected_devices() -> set[str]:
    """Android UDIDs (adb) + iOS UDIDs (libimobiledevice, on a Mac). On Windows the
    iOS probe is simply absent."""
    ids = set(adb_connected())
    try:
        out = subprocess.run(["idevice_id", "-l"], capture_output=True, text=True, timeout=8).stdout
        ids |= {l.strip() for l in out.splitlines() if l.strip()}
    except Exception:
        pass
    return ids


def is_connected(dev: dict, connected: set[str]) -> bool:
    if dev["udid"] in connected:
        return True
    # iOS on a Mac without libimobiledevice installed: don't hard-block the run —
    # Appium/XCUITest will surface a clear error if the phone really isn't there.
    if str(dev.get("platform", "Android")).lower() == "ios" and not _ios_tool_present():
        return True
    return False


def device_for_feature(feature_key: str):
    cfg = load_dashboard_config()
    udid = cfg.get("feature_device_map", {}).get(feature_key)
    return devices_config().get(udid) if udid else None


# ── test discovery (scenario titles + absolute node ids) ────────────────────────
_tests_cache: dict[str, list] = {}
_tests_lock = threading.Lock()


def _abs_node(rel: str) -> str:
    path, _, rest = rel.partition("::")
    return f"{ROOT / path}::{rest}"


_STEP_KW = ("given ", "when ", "then ", "and ", "but ", "* ")


def _scenario_defs(marker: str) -> list[dict]:
    """Parse a feature file into [{title, steps:[{text, key}]}] in scenario order.
    Each scenario is one end-to-end flow; `steps` are its Gherkin steps. `key` is
    the step minus its keyword — that matches conftest's step.name / Allure step
    names, so per-step run status can later be attached by index."""
    fpath = ROOT / "features" / f"{marker}.feature"
    if not fpath.exists():
        return []
    scenarios = []
    for raw in fpath.read_text(encoding="utf-8").splitlines():
        s = raw.strip()
        low = s.lower()
        if low.startswith("scenario outline:") or low.startswith("scenario:"):
            scenarios.append({"title": s.split(":", 1)[1].strip(), "steps": []})
        elif scenarios and any(low.startswith(k) for k in _STEP_KW):
            key = re.sub(r"^(given|when|then|and|but|\*)\s+", "", s, flags=re.I)
            scenarios[-1]["steps"].append({"text": s, "key": key})
    return scenarios


def discover_tests(marker: str) -> list[dict]:
    """Return [{node_id (abs), title, steps:[{text,key}]}] for a marker.
    Cached; refresh via /api/refresh."""
    with _tests_lock:
        if marker in _tests_cache:
            return _tests_cache[marker]
    cmd = [sys.executable, "-m", "pytest", "-m", marker, "--collect-only", "-q",
           "-p", "no:cacheprovider", "-c", str(ROOT / "pytest.ini"),
           "--rootdir", str(ROOT), str(ROOT / "features" / "steps")]
    try:
        res = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True, timeout=120)
        rels = [ln.strip() for ln in res.stdout.splitlines()
                if "::" in ln and "test_" in ln and not ln.strip().startswith(("<", "="))]
    except Exception:
        rels = []
    defs = _scenario_defs(marker)
    tests = []
    for i, rel in enumerate(rels):
        d = defs[i] if i < len(defs) else {"title": rel.split("::")[-1], "steps": []}
        tests.append({"node_id": _abs_node(rel), "title": d["title"], "steps": d["steps"]})
    with _tests_lock:
        _tests_cache[marker] = tests
    return tests


def parse_allure_steps(allure_dir: Path) -> dict:
    """{scenario_title: {status, steps:[{name,status}]}} from Allure result files
    (written for the current run — --clean-alluredir wipes prior ones)."""
    out = {}
    if not allure_dir.exists():
        return out
    for p in allure_dir.glob("*-result.json"):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        name = data.get("name") or data.get("fullName")
        if not name:
            continue
        steps = [{"name": s.get("name"), "status": s.get("status")} for s in data.get("steps", [])]
        out[name] = {"status": data.get("status"), "steps": steps}
    return out


# ── Appium lifecycle (start once per device, reuse, kill on exit) ────────────────
_appium_procs: list = []
_appium_lock = threading.Lock()


def ensure_appium(dev: dict) -> str:
    host, base = appium_settings()
    port = dev["appium_port"]
    with _appium_lock:
        if not rp.port_open(host, port):
            p = rp.start_appium(dev, host, base)
            if p is not None:
                _appium_procs.append(p)
    rp.wait_for_status(host, port, base, timeout=60)
    return f"http://{host}:{port}"


@atexit.register
def _shutdown_appium():
    for p in _appium_procs:
        rp.kill_proc_tree(p)


# ── job model ───────────────────────────────────────────────────────────────────
class Job:
    def __init__(self, feature_key, marker, mode, node_ids, title, device):
        self.feature_key = feature_key
        self.marker = marker
        self.mode = mode                    # "suite" | "tests"
        self.node_ids = node_ids or []      # specific test node ids when mode == "tests"
        self.title = title                  # what's being run (for display)
        self.device = device
        self.status = "pending"             # pending|running|passed|failed|stopped|error
        self.logs: list[str] = []
        self.proc = None
        self.stop_requested = False
        self.start_ts = None
        self.end_ts = None
        self.results = None                 # parsed junit summary
        self.returncode = None

    def duration(self):
        if self.start_ts and self.end_ts:
            return round(self.end_ts - self.start_ts, 1)
        if self.start_ts:
            return round(time.time() - self.start_ts, 1)
        return None

    def to_dict(self):
        return {
            "feature": self.feature_key, "mode": self.mode, "title": self.title,
            "status": self.status, "returncode": self.returncode,
            "device": {"udid": self.device["udid"], "name": self.device["name"]} if self.device else None,
            "duration": self.duration(), "results": self.results,
            "log_count": len(self.logs),
        }


jobs: dict[str, Job] = {}
jobs_lock = threading.Lock()
_device_locks: dict[str, threading.Lock] = {}
_device_locks_guard = threading.Lock()


def _device_lock(udid: str) -> threading.Lock:
    with _device_locks_guard:
        return _device_locks.setdefault(udid, threading.Lock())


# ── junit parsing ───────────────────────────────────────────────────────────────
def parse_junit(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        root = ET.parse(path).getroot()
    except Exception:
        return None
    suites = root.findall("testsuite") if root.tag == "testsuites" else [root]
    total = failed = errors = skipped = 0
    total_time = 0.0
    cases = []
    for s in suites:
        total += int(s.get("tests", 0) or 0)
        failed += int(s.get("failures", 0) or 0)
        errors += int(s.get("errors", 0) or 0)
        skipped += int(s.get("skipped", 0) or 0)
        total_time += float(s.get("time", 0) or 0)
        for tc in s.findall("testcase"):
            status, msg = "passed", ""
            if tc.find("failure") is not None:
                status, msg = "failed", tc.find("failure").get("message", "")
            elif tc.find("error") is not None:
                status, msg = "error", tc.find("error").get("message", "")
            elif tc.find("skipped") is not None:
                status, msg = "skipped", tc.find("skipped").get("message", "")
            cases.append({"name": tc.get("name"), "time": round(float(tc.get("time", 0) or 0), 1),
                          "status": status, "message": (msg or "")[:600]})
    passed = total - failed - errors - skipped
    return {"total": total, "passed": passed, "failed": failed + errors,
            "skipped": skipped, "time": round(total_time, 1), "cases": cases}


# ── job execution ───────────────────────────────────────────────────────────────
def _run_job(job: Job):
    dev = job.device
    out_dir = OUTPUT / job.feature_key
    allure_dir = out_dir / "allure-results"
    junit_path = out_dir / "results.xml"
    out_dir.mkdir(parents=True, exist_ok=True)

    job.logs.append(f"[dashboard] Queued '{job.title}' on {dev['name']} ({dev['udid']})")
    lock = _device_lock(dev["udid"])
    with lock:
        if job.stop_requested:
            job.status = "stopped"
            job.logs.append("[dashboard] Stopped before start.")
            return
        job.status = "running"
        job.start_ts = time.time()
        try:
            job.logs.append(f"[dashboard] Ensuring Appium for {dev['name']} on :{dev['appium_port']} ...")
            url = ensure_appium(dev)
            work = rp.write_device_env(dev, url)

            node_ids = None if job.mode == "suite" else job.node_ids
            marker = job.marker if job.mode == "suite" else None
            if junit_path.exists():
                junit_path.unlink()
            cmd = rp.build_pytest_cmd(marker=marker, node_ids=node_ids,
                                      allure_dir=allure_dir, junit_path=junit_path)

            env = os.environ.copy()
            env["APPIUM_SERVER"] = url
            env["UDID"] = dev["udid"]
            env["ALLURE_RESULTS_DIR"] = str(allure_dir)
            env["PYTHONUNBUFFERED"] = "1"

            run_desc = f"-m {marker}" if marker else f"{len(node_ids)} selected test(s)"
            job.logs.append(f"[dashboard] Running: pytest {run_desc}")
            job.proc = subprocess.Popen(
                cmd, cwd=str(work), env=env,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1, encoding="utf-8", errors="replace")
            for line in job.proc.stdout:
                job.logs.append(line.rstrip("\n"))
                if len(job.logs) > 6000:
                    del job.logs[:1500]
            job.returncode = job.proc.wait()
        except Exception as e:
            job.status = "error"
            job.logs.append(f"[dashboard] ERROR: {e}")
            job.end_ts = time.time()
            return

        job.end_ts = time.time()
        res = parse_junit(junit_path)
        scenarios = parse_allure_steps(allure_dir)
        if res is None and scenarios:
            res = {"total": 0, "passed": 0, "failed": 0, "skipped": 0,
                   "time": job.duration() or 0, "cases": []}
        if res is not None:
            res["scenarios"] = scenarios       # {title: {status, steps:[{name,status}]}}
        job.results = res
        if job.stop_requested:
            job.status = "stopped"
        elif job.results and (job.results["failed"] > 0):
            job.status = "failed"
        elif job.returncode == 0:
            job.status = "passed"
        else:
            job.status = "failed"
        job.logs.append(f"[dashboard] Finished: {job.status} (exit {job.returncode}) in {job.duration()}s")


def start_job(feature_key: str, mode: str, node_ids=None) -> dict:
    feat = next((f for f in load_dashboard_config()["features"] if f["key"] == feature_key), None)
    if not feat:
        return {"ok": False, "error": f"Unknown feature {feature_key}"}
    dev = device_for_feature(feature_key)
    if dev is None:
        return {"ok": False, "error": f"No device mapped for {feature_key}"}
    if not is_connected(dev, connected_devices()):
        return {"ok": False, "error": f"Device {dev['name']} ({dev['udid']}) not connected"}

    mode = "tests" if mode == "tests" else "suite"
    node_ids = list(node_ids or [])
    if mode == "tests" and not node_ids:
        return {"ok": False, "error": f"{feat['name']}: no test cases selected"}

    with jobs_lock:
        existing = jobs.get(feature_key)
        if existing and existing.status in ("pending", "running"):
            return {"ok": False, "error": f"{feat['name']} is already {existing.status}"}
        if mode == "suite":
            title = f"{feat['name']} — Full Suite"
        elif len(node_ids) == 1:
            t = next((t for t in discover_tests(feat["marker"]) if t["node_id"] == node_ids[0]), None)
            title = f"{feat['name']} — {t['title'] if t else node_ids[0].split('::')[-1]}"
        else:
            title = f"{feat['name']} — {len(node_ids)} selected tests"
        job = Job(feature_key, feat["marker"], mode, node_ids, title, dev)
        jobs[feature_key] = job
    threading.Thread(target=_run_job, args=(job,), daemon=True).start()
    return {"ok": True, "feature": feature_key}


# ── routes ──────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return send_file(DASH_DIR / "index.html")


@app.route("/api/state")
def api_state():
    cfg = load_dashboard_config()
    connected = connected_devices()
    devs = devices_config()
    device_list = [{"udid": u, "name": d["name"], "platform": d.get("platform", "Android"),
                    "connected": is_connected(d, connected)}
                   for u, d in devs.items()]
    features = []
    for feat in cfg["features"]:
        udid = cfg.get("feature_device_map", {}).get(feat["key"])
        dev = devs.get(udid)
        with jobs_lock:
            job = jobs.get(feat["key"])
        features.append({
            "key": feat["key"], "name": feat["name"], "icon": feat.get("icon", "🧪"),
            "marker": feat["marker"],
            "device": {"udid": udid, "name": dev["name"] if dev else None,
                       "connected": is_connected(dev, connected) if dev else False} if udid else None,
            "tests": discover_tests(feat["marker"]),
            "job": job.to_dict() if job else None,
        })
    return jsonify({"features": features, "devices": device_list})


@app.route("/api/run", methods=["POST"])
def api_run():
    data = request.get_json(force=True) or {}
    items = data.get("items", [])
    results = [dict(start_job(it.get("feature"), it.get("mode", "suite"), it.get("node_ids")),
                    feature=it.get("feature")) for it in items]
    return jsonify({"results": results})


@app.route("/api/stop/<feature>", methods=["POST"])
def api_stop(feature):
    with jobs_lock:
        job = jobs.get(feature)
    if not job:
        return jsonify({"ok": False, "error": "no job"}), 404
    job.stop_requested = True
    if job.proc and job.proc.poll() is None:
        rp.kill_proc_tree(job.proc)
        job.logs.append("[dashboard] Stop requested — killing test process.")
    return jsonify({"ok": True})


@app.route("/api/logs/<feature>")
def api_logs(feature):
    since = int(request.args.get("since", 0))
    with jobs_lock:
        job = jobs.get(feature)
    if not job:
        return jsonify({"lines": [], "next": 0, "status": None})
    lines = job.logs[since:]
    return jsonify({"lines": lines, "next": since + len(lines),
                    "status": job.status, "results": job.results})


@app.route("/api/map", methods=["POST"])
def api_map():
    data = request.get_json(force=True) or {}
    feature, udid = data.get("feature"), data.get("udid")
    cfg = load_dashboard_config()
    mapping = cfg.get("feature_device_map", {})
    mapping[feature] = udid
    save_feature_device_map(mapping)
    return jsonify({"ok": True, "map": mapping})


@app.route("/api/refresh", methods=["POST"])
def api_refresh():
    with _tests_lock:
        _tests_cache.clear()
    return jsonify({"ok": True})


@app.route("/api/report/<feature>", methods=["POST"])
def api_report(feature):
    allure_dir = OUTPUT / feature / "allure-results"
    if not allure_dir.exists():
        return jsonify({"ok": False, "error": "no results yet"}), 404
    prefix = ["cmd", "/c"] if rp.IS_WINDOWS else []
    try:
        subprocess.Popen(prefix + ["allure", "serve", str(allure_dir)])
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500
    return jsonify({"ok": True})


if __name__ == "__main__":
    OUTPUT.mkdir(parents=True, exist_ok=True)
    print("Luna Automation Dashboard -> http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, threaded=True, debug=False)
