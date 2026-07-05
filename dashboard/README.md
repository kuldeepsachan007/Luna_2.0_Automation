# Luna Automation Dashboard

A local web dashboard to **control the Appium automation** (Sleep / Heart Rate /
Stress) and **see results after each run** — full suite or a single test case,
per-feature on a mapped device, several features at once (parallel across
devices), with live logs and a pass/fail/skip summary.

It reuses the device-isolation engine in [`../parallel/run_parallel.py`](../parallel/run_parallel.py)
(per-device Appium server, per-device `.env`, OnePlus caps). The existing
framework (`conftest.py`, `pytest.ini`, `.env`, pages, features) is **not**
modified.

## Start

```bat
dashboard\run_dashboard.bat
```

Then open **http://127.0.0.1:5000**.

> **Mac mini / iPhone (iOS) testing** and **hosting the UI globally (Vercel + tunnel)**
> are covered in [DEPLOY.md](DEPLOY.md). The runner is already platform-aware
> (Android + iOS); the backend must run on the machine the devices are plugged
> into.

## What you can do

- **Per feature card:** pick the device, pick a test (or *Full Suite*), then
  **Run Full Suite** / **Run Selected Test** / **Stop**. Live logs stream in the
  card; a mini pass/fail/skip summary appears when it finishes.
- **Run Selected Features:** tick the checkbox on multiple cards and click the
  top button — each runs on its own device **in parallel** (two features on the
  *same* device are queued, not clashed).
- **Results:** KPI row (total / passed / failed / skipped / time), a feature-wise
  table, and expandable failed-test details. **Report** opens the rich Allure
  report for that feature.

## Configure device mapping

`config.json` maps each feature to a device `udid` (device details — ports, caps,
name — come from `../parallel/devices.json`). Change it there, or just pick a
device from the card's dropdown (it's saved back to `config.json`).

Default: Sleep → POCO, Heart Rate → OnePlus, Stress → POCO. With a third device,
add it to `parallel/devices.json` and point Stress at it.

## How execution works

| Concern | Handled by |
|---|---|
| Trigger from browser | Flask API (`/api/run`) |
| Run pytest locally | `subprocess` → `pytest -m <marker>` or a specific node id |
| Parallel across devices | one thread per feature + per-device lock |
| Device isolation | reused `parallel/` helpers (Appium port, systemPort, `.env`) |
| Live logs | pytest stdout streamed to the job, polled by the UI |
| Results | `--junitxml` parsed into total/passed/failed/skipped/time |
| Rich report | Allure (`--alluredir`) via the **Report** button |

## API (for reference)

| Method + path | Purpose |
|---|---|
| `GET /api/state` | features (tests, device, latest job), connected devices |
| `POST /api/run` | `{items:[{feature,mode:"suite"|"test",node_id?}]}` |
| `POST /api/stop/<feature>` | stop a running feature |
| `GET /api/logs/<feature>?since=N` | incremental live logs |
| `POST /api/map` | `{feature,udid}` — change device mapping |
| `POST /api/report/<feature>` | open the Allure report |
| `POST /api/refresh` | re-scan test cases from the feature files |

## Note

A test only **passes** when the device + backend deps are reachable (the suites
connect to the Luna MySQL DB on the office network). If you're off that network
the test step fails with a DB connection error — that's environmental, not a
dashboard issue.
