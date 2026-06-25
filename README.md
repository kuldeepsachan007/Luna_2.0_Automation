# lunaPytestBdd

A compact, practical guide to this mobile automation helper repo (Appium + pytest-bdd).

This README explains how the project is organized, what the key fixtures and utilities do, how to create features and step files, how locators are chosen for Android and iOS, and how to run the suite and produce Allure reports.

Table of contents
- Overview
- Quick start (install & run)
- .env / environment variables
- Project layout (high-level)
- Key fixtures (in `conftest.py`) and scopes
- `pytest.ini` and configuration
- Utilities and helper libraries (where to look and examples)
- `test_data` and assets (download/upload/screenshots)
- Page objects (pages/) pattern
- Features and steps (how to write them)
- Locators and platform separation (Android vs iOS)
- Allure reporting and environment information
- Troubleshooting & tips

Overview
--------
This repository contains reusable fixtures and helpers for testing native mobile apps with Appium and pytest-bdd. It provides:
- a standard set of fixtures for creating Appium sessions and passing an `app` object into BDD steps
- page object helpers under `pages/`
- reusable low-level helpers under `utility/liberaries/`
- example BDD features under `features/` and step registration
- Allure integration hooks and helpful attachments (screenshots, environment info)

Appium Server and devices find/setup are outside the scope of this repo. You need to have an Appium server running and a device or emulator available to run tests.
-----------

Prerequisites / quick environment setup
--------------------------------------

1. Appium server
   - Install:
     ```bash
     npm install -g appium
     ```
   - Start:
     ```bash
     appium
     ```
2. Device / emulator ready
   - Android (AVD or physical device)
     - List connected devices:
       ```bash
       adb devices
       ```
     - List available emulators:
       ```bash
       emulator -list-avds
       ```
     - Start an emulator:
       ```bash
       emulator -avd <emulator_name>
       ```
     - Ensure the emulator is running before tests.
   - iOS
     - Use Xcode's `Simulator` app to launch a simulator.
3. Configure capabilities
   - Provide device/app capabilities via a `.env` file or environment variables (see the `.env` section).
4. Run tests
   - Produce Allure results:
     ```bash
     pytest --alluredir=allure-results
     ```
   - Run without starting Appium sessions (local experimentation):
     ```bash
     SKIP_APPIUM=1 pytest --alluredir=allure-results
     ```
5. View Allure report
   - Serve results locally (requires Allure CLI):
     ```bash
     allure serve allure-results
     ```

Quick start
-----------
1. Create a Python virtualenv and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
2. Create a `.env` file in the repo root (see the `.env` section below) or set environment variables.

3. Run tests and create an Allure results directory:

```bash
# run tests and produce allure results
pytest --alluredir=allure-results
# serve the result in the browser (requires Allure CLI installed)
allure serve allure-results
```

If you want to run without starting Appium sessions (useful locally):
```bash
SKIP_APPIUM=1 pytest --alluredir=allure-results
```

.env / environment variables
----------------------------
Place a `.env` file in the repository root or set environment variables in your environment. Typical keys this project expects:
- APPIUM_SERVER      - URL of the Appium server (default http://127.0.0.1:4723)
- PLATFORM_NAME      - Android or iOS
- DEVICE_NAME        - device id or emulator name
- PLATFORM_VERSION   - OS version string
- AUTOMATION_NAME    - UiAutomator2 (Android) or XCUITest (iOS)
- APP_PACKAGE        - Android package name (if not using an `app` file)
- APP_ACTIVITY       - Android activity (if not using an `app` file)
- UDID               - device UDID (if needed)
- IMPLICIT_WAIT      - default implicit wait (seconds)
- SCREENSHOT_DIR     - path to save step-level screenshots (defaults to project screenshot helper)

Example `.env`:

```
APPIUM_SERVER=http://localhost:4723/wd/hub
PLATFORM_NAME=Android
DEVICE_NAME=emulator-5554
PLATFORM_VERSION=12
AUTOMATION_NAME=UiAutomator2
APP_PACKAGE=com.example.app
APP_ACTIVITY=.MainActivity
IMPLICIT_WAIT=5
```

Project layout (high-level)
---------------------------
Important folders and files:
- `conftest.py` — fixtures and pytest-bdd hooks (Allure integration, screenshot on failure, env fixture)
- `pytest.ini` — pytest configuration and `--alluredir` default
- `features/` — `.feature` files and the `steps/` package that implements step functions
- `pages/` — page object classes (e.g., `base_page.py`, `login_page.py`)
- `utility/liberaries/` — helper modules (Allure logger, forms, locators, waits, gestures, etc.)
- `test_data/` — test assets (upload/download directories, screenshots)

Key fixtures in `conftest.py`
-----------------------------
The following fixtures are provided and used across the BDD steps. Understanding their scopes is important.

- `env` (session, autouse)
  - Returns a dict of environment values (APPIUM_SERVER, PLATFORM_NAME, DEVICE_NAME, etc.).
  - Autouse and session-scoped so it's created once per test session and available to all tests/steps.
  - Writes Allure environment files (`environment.properties`, `environment.json`) into the Allure results folder so environment info appears in the Allure UI.

- `driver_factory` (session)
  - A callable factory that creates Appium WebDriver sessions with configured capabilities.
  - Returns a function which, when called, will create a new Appium session (useful if a test wants to create extra sessions).

- `driver` (function)
  - Uses `driver_factory()` to create and yield a WebDriver for the test; after the test, `drv.quit()` is called.
  - Honors `SKIP_APPIUM` env var (if set to true/1 it will skip tests relying on Appium).

- `app` (function)
  - Convenience wrapper around `driver` used in BDD steps. For native testing this typically returns the active Appium session.

- `set_env_var` (function)
  - A small utility fixture that lets a test temporarily modify environment variables and restores them after the test.

- `add_env_to_dotenv(key, value)`
  - Helper that writes or updates a `.env` file and reloads it.

Fixture scopes explained
- session: created once for the whole test run (good for `env`, `driver_factory`).
- function: created for each test function (good for `driver` since each test typically needs a fresh session).
- autouse: automatically included without explicitly requesting it in a test or fixture.

`pytest_bdd` hooks in `conftest.py`
---------------------------------
The project uses pytest-bdd hooks to enhance reporting and debugging:
- `pytest_bdd_before_scenario` — sets Allure dynamic labels (feature/title) so scenarios are grouped nicely in Allure.
- `pytest_bdd_before_step` / `pytest_bdd_after_step` / `pytest_bdd_step_error` — start and stop Allure step contexts so each BDD step is visible in Allure with timing and screenshots on failure.
- `pytest_bdd_after_scenario` — attaches a scenario summary and a screenshot to the scenario-level Allure entry.

`pytest.ini` and configuration
-----------------------------
Open `pytest.ini` to see defaults — typical useful settings in the repo include:
- `addopts = --clean-alluredir --alluredir=allure-results`
  - This tells pytest to clear the Allure results folder and write new results there on each run.
- `testpaths` — directories pytest should look in for tests (configured to `features.steps` in this project).
- Logging: `log_cli`, `log_cli_level`, `log_format` to enable live logging in the console.

Utilities and helper libraries (`utility/liberaries/`)
----------------------------------------------------
This folder contains helper modules used across pages and steps. Common helpers include:
- `allure_logs.py` — small wrapper helpers for attachments and step contexts
- `forms.py` / `forms_rfn.py` — functions for reliably interacting with inputs and forms
- `mouse.py` / `mouse_rfn.py` — click/tap helpers with fallbacks
- `waits.py` — explicit wait helpers
- `locators.py` / `platform_locators/` — helpers/factories that build locator tuples or objects
- `decorators.py` — retry/time decorators used across helpers

Examples
- Attach text in Allure: `AllureLogger.attach_text("some text", name="info")`
- Use a retry decorator around fragile functions: `@retry_on_exception(...)`

test_data/ and test assets
--------------------------
- `test_data/download/`, `test_data/upload/`, `test_data/screenshots/` provide central places for test files, captured screenshots, and uploads. Use the `test_data` fixture or the `pages` helpers to access these.

Page objects (`pages/`)
-----------------------
Pages implement a thin wrapper around an Appium WebDriver instance and provide a place for:
- element locators
- actions (methods that interact with elements)
- composition of small operations into higher-level flows

Example pattern (`pages/base_page.py`):
- Each page gets constructed with a `driver`.
- The page exposes helpers and references to utility modules (forms, waits, gestures).

Locator pattern and platform separation
---------------------------------------
This repo separates platform-specific locators (Android vs iOS) to make steps and pages portable.
- Platform-specific locators are typically under `utility/liberaries/platform_locators/` (or similar).
- Pages may expose both `android_locators` and `ios_locators` (see `base_page.py`) and choose the correct set at runtime:
  - Example: `page.get_platform_name()` reads `driver.capabilities.get("platformName")` and returns `'android'` or `'ios'`.
  - When a page method needs a locator, it chooses `self.android_locators` or `self.ios_locators` depending on the platform.

Locators and Appium best-practices
- Prefer accessibility id when available for robustness: `AppiumBy.ACCESSIBILITY_ID`.
- Use resource-id (Android) or name/accessibility id (iOS) when stable.
- Fallback to XPath only when necessary.
- Locator helper functions in `utility/liberaries/locators.py` may return a small `Locator` object or a tuple accepted by helper functions.

How to write a new `.feature` file
---------------------------------
1. Create a new feature file under `features/`, for example `features/login.feature`.
2. Basic structure (Gherkin):

```
Feature: Login
  As a user I want to log in so I can use the app

  Scenario: Successful login
    Given the app is open
    When I click the element with xpath "//button[@text='Login']"
    Then I should see text "Welcome"
```

3. Keep scenarios focused and small. Reuse existing steps where possible.

How to create a step file for a feature
--------------------------------------
1. Place step functions under `features/steps/` (this project registers steps via `scenarios(...)` in each steps module).
2. Use pytest-bdd decorators: `@given`, `@when`, `@then`, `@step`.

Example step function in `features/steps/test_login_steps.py`:

```python
from pytest_bdd import given, when, then, parsers
from appium.webdriver.common.appiumby import AppiumBy

@given('the app is open')
def app_open(app):
    assert app.session_id

@when(parsers.parse('I click the element with {by} "{selector}"'))
def click_element(app, by, selector):
    # Map friendly 'by' values to AppiumBy constants and find the element
    if by.lower() in ("id", "resource-id"):
        el = app.find_element(AppiumBy.ID, selector)
    elif by.lower() == 'xpath':
        el = app.find_element(AppiumBy.XPATH, selector)
    elif by.lower() in ("accessibility_id",):
        el = app.find_element(AppiumBy.ACCESSIBILITY_ID, selector)
    else:
        el = app.find_element(AppiumBy.XPATH, selector)
    el.click()

@then(parsers.parse('I should see text "{text}" on the page'))
def should_see_text(app, text):
    assert text in app.page_source
```

How steps pick locators (Android vs iOS)
----------------------------------------
- Simple step helpers (like the generic click step above) accept a `by` string and `selector` and map them to `AppiumBy` constants.
- For richer, page-oriented steps, pages will expose platform-locators; a step can call into a page object which chooses the correct locator for the current platform.

Example in a page object:
```python
class LoginPage(BasePage):
    def login_button(self):
        if self.get_platform_name() == 'android':
            return (AppiumBy.ID, 'com.example:id/login_button')
        else:
            return (AppiumBy.ACCESSIBILITY_ID, 'login_button')

    def tap_login(self):
        by, sel = self.login_button()
        self.driver.find_element(by, sel).click()
```

Allure integration and environment info
--------------------------------------
- The project writes `environment.properties` and `environment.json` into the `allure-results` directory so the Allure UI can show environment info.
- Per-step timing and step-level attachments (screenshots) are provided via pytest-bdd hooks in `conftest.py`.
- To view the results:
  1. `pytest --alluredir=allure-results`
  2. `allure serve allure-results`

Troubleshooting & tips
----------------------
- If steps are not visible in Allure: ensure you have a recent `allure-pytest` and Allure CLI installed. The conftest code uses `allure.step` context managers — older/allure combinations can behave differently.
- If environment info doesn't show: ensure you run pytest from the repository root or pass a matching `--alluredir` path. The repo writes env files into the results directory configured by `--alluredir` or `ALLURE_RESULTS_DIR` env var.
- To avoid Appium launches while experimenting: set `SKIP_APPIUM=1` in your environment.
- For CI: make sure the CI runner saves/publishes the `allure-results` directory as an artifact before serving or publishing the report.

Contributing tips
-----------------
- Keep BDD steps small and reusable. Prefer composing page object methods instead of duplicating element-finding logic in steps.
- Add unit tests for utility helpers where possible (mock the Appium driver using a simple stub or a mocking library).
- When adding new locators, group them under platform-specific blocks so both Android and iOS remain supported.
