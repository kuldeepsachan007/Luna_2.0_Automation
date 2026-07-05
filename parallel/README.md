# Parallel multi-device runner

Run a different feature on each connected Android device **at the same time** —
e.g. Heart Rate on one phone and Stress on another — with full isolation and a
combined Allure report.

This module is **self-contained**. It does **not** modify `conftest.py`,
`pytest.ini`, or the project `.env`. It works by launching one `pytest` process
per device inside a generated per-device working directory, relying on the fact
that `conftest.py` already loads its `.env` from the current working directory.

## How isolation works

| Concern | Per-device isolation |
|---|---|
| Appium server | Unique `--port` (4741, 4742, …) |
| UiAutomator2 device bridge | Unique `systemPort` + `mjpegServerPort` (via Appium `--default-capabilities`) |
| Target device | Unique `UDID` / `DEVICE_NAME` / `PLATFORM_VERSION` in the generated `.env` |
| Test results | `parallel/_output/allure-results/<udid>` |
| Logs | `parallel/_output/logs/{appium,pytest}_<udid>.log` |

The generated `.env` is the project `.env` copied **verbatim** (so all secrets,
`HEALTH_TARGET_DATE`, `APP_PACKAGE`, etc. carry over) with device-specific
overrides appended at the end. `conftest.py` loads with `override=True`, and
python-dotenv keeps the *last* value of a duplicated key, so the overrides win.

## Configure

Edit [`devices.json`](devices.json). Each device has a default `marker` and its
port assignments. Ports are chosen to avoid a manually-started Appium on `4723`.

## Run

From the project root, with `myenv` activated (or just use the `.bat`):

```bat
REM Default: heart_rate on device 1, stress on device 2 (from devices.json)
run_parallel.bat

REM Assign markers by device order
run_parallel.bat heart_rate stress

REM Assign explicitly (order/count independent)
run_parallel.bat heart_rate@70f31eb6b9fc stress@TWL77DU8U4TKIBYT

REM Sanity-check config without any device (fast)
run_parallel.bat --collect-only

REM Show what would run, then exit
run_parallel.bat --list
```

Or call the script directly:

```bat
python parallel\run_parallel.py heart_rate stress
```

### Options

| Flag | Meaning |
|---|---|
| `--list` | Print resolved device→marker plan and exit |
| `--collect-only` | Only collect tests per device (no Appium / no device needed) |
| `--no-appium` | Assume Appium servers are already up on the configured ports |
| `--keep-appium` | Leave runner-started Appium servers running afterwards |
| `--report` | Generate + open a combined Allure report at the end |

The runner **continues on failure** — one device failing never stops the other.
It starts an Appium server per device only if the port is free (otherwise it
reuses whatever is already there and leaves it running).

## Report

```bat
report.bat
```

Merges every device's results into one Allure report and opens it. (Equivalent
to `python parallel\report.py`.)

## Adding a third device

1. Plug it in, enable USB debugging, `adb devices` should show it authorized.
2. Add an entry to `devices.json` with a fresh `appium_port` / `system_port` /
   `mjpeg_port` and its `platform_version`.
3. `run_parallel.bat marker1 marker2 marker3`.
