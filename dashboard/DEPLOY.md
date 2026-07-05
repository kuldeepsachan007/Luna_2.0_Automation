# Deploying / running the dashboard elsewhere

Everything dashboard-related lives in this one folder (`dashboard/`). It drives
the same framework, so the **whole repo** must be present on whatever machine
runs the tests (it reuses `../parallel/` + `../features/` + `../pages/` +
`../conftest.py`). The dashboard **backend must run on the machine the devices
are physically connected to** — that's the one hard rule below.

---

## 1. Local (default) — Windows or Mac

```bat
dashboard\run_dashboard.bat        REM Windows
```
```bash
# macOS / Linux
cd <repo> && source myenv/bin/activate && python dashboard/app.py
```
Open http://127.0.0.1:5000.

---

## 2. Mac mini — iPhone (iOS) testing

The runner is already **platform-aware**. To add an iPhone:

**Prerequisites on the Mac mini**
- Xcode + command line tools
- Appium XCUITest driver: `appium driver install xcuitest`
- (device detection) libimobiledevice: `brew install libimobiledevice`
- WebDriverAgent signed once via Xcode for your Apple ID

**Add the device** to [`../parallel/devices.json`](../parallel/devices.json):
```json
{
  "udid": "<iphone-udid>",
  "name": "iPhone-13",
  "platform": "iOS",
  "platform_version": "17.5",
  "automation_name": "XCUITest",
  "appium_port": 4743,
  "wda_local_port": 8100,
  "extra_caps": { "appium:bundleId": "com.noisefit.luna.dev" }
}
```
Then map a feature to it in [`config.json`](config.json), e.g. `"heart_rate": "<iphone-udid>"`.

How it stays no-code: the runner writes `PLATFORM_NAME=iOS` / `AUTOMATION_NAME=XCUITest`
into that device's generated `.env` (which `conftest.py` reads), and injects
`bundleId` / `wdaLocalPort` via the Appium server's `--default-capabilities` — so
**`conftest.py` is not modified**. Android and iOS devices can run in parallel;
each gets its own Appium port + bridge port (systemPort for Android, wdaLocalPort
for iOS).

> The iOS **locators/pages** are a separate effort — the current page objects use
> Android locators. iOS scenarios need iOS locators, but the runner + dashboard
> plumbing is ready.

---

## 3. Global access (host the UI on Vercel)

**Important architectural fact:** the automation runs `pytest` + Appium against
**USB-connected devices**, so the **backend cannot run on Vercel** (Vercel is
cloud serverless — no access to your phones, no long-running processes). What you
*can* do is host the **UI globally** and point it at your local backend:

1. **Deploy the UI** (this folder) to Vercel — `index.html` + `vercel.json` are
   all it needs (static, no build):
   ```bash
   cd dashboard && vercel deploy --prod
   ```
2. **Run the backend** on the machine with the devices (Windows PC / Mac mini):
   `run_dashboard.bat` (→ :5000).
3. **Expose the backend** with a tunnel so the hosted UI can reach it:
   ```bash
   cloudflared tunnel --url http://127.0.0.1:5000      # or: ngrok http 5000
   ```
   You get a public URL like `https://xxxx.trycloudflare.com`.
4. **Point the UI at it** — open your Vercel URL with the backend as a query param
   (remembered in the browser afterwards):
   ```
   https://your-app.vercel.app/?api=https://xxxx.trycloudflare.com
   ```

The backend already sends permissive CORS headers, so the cross-origin UI works.

> If you want the dashboard reachable globally **without** keeping a PC on, you'd
> need a hosted **device farm** (BrowserStack / Sauce Labs) as the Appium target
> instead of local USB devices — a larger change, not required for local/tunnel use.
