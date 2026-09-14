# Luna Framework — Cross-platform Setup (Windows + macOS)

Same code dono OS par chalta hai. Sirf **machine-level setup** (venv, Appium, adb,
cloudflared) har machine par ek baar karna hota hai. Launcher ab **Python** me hai
(`start_global.py`) jo dono OS par same chalta hai — bas wrapper alag:
Windows `start_global.bat`, macOS `start_global.sh`.

---

## Dono OS par common (concept)
- **Code**: GitHub se `git clone` — same.
- **Vercel UI**: cloud par — same URL, koi change nahi.
- **Launcher logic**: `start_global.py` — same.

---

## 🪟 Windows — ek baar setup
```powershell
# 1. venv + libraries
python -m venv myenv
myenv\Scripts\activate
pip install -r requirements.txt

# 2. Appium + Android driver (Node zaroori)
npm install -g appium
appium driver install uiautomator2

# 3. adb (Android platform-tools PATH me ho)
adb devices

# (cloudflared khud download ho jaata hai start_global.py se)
```
**Chalao:** `start_global.bat` double-click.

---

## 🍎 macOS (Mac mini) — ek baar setup
```bash
# 1. venv + libraries
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Appium + drivers
npm install -g appium
appium driver install uiautomator2      # Android
appium driver install xcuitest          # iOS (iPhone testing)

# 3. Tools (Homebrew se)
brew install android-platform-tools     # adb (Android)
brew install cloudflared                # tunnel
# iOS ke liye: Xcode install + WebDriverAgent ek baar sign karo

# 4. launcher scripts executable banao
chmod +x start_global.sh dashboard/run_dashboard.sh
```
**Chalao:** `./start_global.sh`

---

## Dono par chalane ke tarike

| Kaam | Windows | macOS |
|---|---|---|
| Sab ek shot (backend+tunnel+browser) | `start_global.bat` | `./start_global.sh` |
| Sirf dashboard backend | `dashboard\run_dashboard.bat` | `./dashboard/run_dashboard.sh` |
| Tests (CLI) | `pytest -m sleep` | `pytest -m sleep` |

---

## 📱 iOS (sirf Mac par)
Runner platform-aware hai. `parallel/devices.json` me iOS device add karo:
```json
{
  "udid": "<iphone-udid>", "name": "iPhone-13", "platform": "iOS",
  "platform_version": "17.5", "automation_name": "XCUITest",
  "appium_port": 4743, "wda_local_port": 8100,
  "extra_caps": { "appium:bundleId": "com.noisefit.luna.dev" }
}
```
> Note: iOS ke liye **alag locators/pages** chahiye (abhi Android-only). Plumbing ready hai.

---

## ⚠️ Machine-specific (transfer nahi hota)
- `myenv/` / `venv/` (Python binaries) — har machine par naya banao
- `cloudflared` binary — Windows `.exe`, Mac alag (brew)
- `.env` — copy kar sakte ho, par andar koi absolute path ho to update karo
- Hardcoded paths — script relative hain, phir bhi check kar lena

---

## Ek line me
> **Code + GitHub + Vercel = same dono par.** Har machine par ek baar: venv + `pip install -r requirements.txt` + Appium + adb (+ Mac par cloudflared/Xcode). Phir Windows `start_global.bat`, Mac `./start_global.sh`.
