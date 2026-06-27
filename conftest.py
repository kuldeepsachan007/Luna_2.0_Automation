import os
import logging
from pathlib import Path
from typing import Dict, Any, Callable, Optional
import pytest
from dotenv import load_dotenv
import time

from appium import webdriver as appium_webdriver
from appium.webdriver.webdriver import WebDriver as AppiumWebDriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.common.base import AppiumOptions
from pytest_bdd import given, when, then, parsers, step

from test_data import screenshots
import allure
from utility.liberaries.allure_logs import AllureLogger

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

pytest_plugins = [
    "features.steps",
]



DOTENV_PATH = Path(os.getcwd()) / ".env"
if DOTENV_PATH.exists():
    load_dotenv(dotenv_path=DOTENV_PATH, override=True)
    logger.info("Loaded .env from %s", DOTENV_PATH)
else:
    logger.info("No .env found at %s; using environment variables", DOTENV_PATH)


@pytest.fixture(scope="session")
def test_data():
    """
    Load test data from .env or other sources if needed.
    Currently just a placeholder.
    """
    from utility.liberaries.test_data import TestData
    test_data = TestData()
    return test_data

@pytest.fixture(scope="session", autouse=True)
def env() -> Dict[str, Any]:
    """
    Appium-only environment settings. Useful vars:
      - APPIUM_SERVER (e.g. http://localhost:4723/wd/hub)
      - PLATFORM_NAME (Android / iOS)
      - DEVICE_NAME (emulator or device id)
      - PLATFORM_VERSION
      - AUTOMATION_NAME (UiAutomator2 / XCUITest)
      - APP_PACKAGE, APP_ACTIVITY (Android)
      - UDID
    """
    env = {
        "APPIUM_SERVER": os.getenv("APPIUM_SERVER", "http://127.0.0.1:4723"),
        "PLATFORM_NAME": os.getenv("PLATFORM_NAME", "Android"),
        "DEVICE_NAME": os.getenv("DEVICE_NAME", "emulator-5554"),
        "PLATFORM_VERSION": os.getenv("PLATFORM_VERSION"),
        "AUTOMATION_NAME": os.getenv("AUTOMATION_NAME", "UiAutomator2"),
        "APP_PACKAGE": os.getenv("APP_PACKAGE"),
        "APP_ACTIVITY": os.getenv("APP_ACTIVITY"),
        "UDID": os.getenv("UDID"),
        "IMPLICIT_WAIT": float(os.getenv("IMPLICIT_WAIT", "5")),
        "SCREENSHOT_DIR": os.getenv("SCREENSHOT_DIR", screenshots),
    }

    # Write Allure environment properties so they appear in the Allure report
    try:
        # allow overriding the results dir via env var; default matches pytest.ini
        results_dir = os.getenv("ALLURE_RESULTS_DIR", "allure-results")
        ar = Path(os.getcwd()) / results_dir
        ar.mkdir(parents=True, exist_ok=True)
        env_file = ar / "environment.properties"
        with env_file.open("w", encoding="utf-8") as f:
            for k, v in env.items():
                # convert non-str values to str, and avoid None
                val = "" if v is None else str(v)
                f.write(f"{k}={val}\n")
        logger.info("Wrote Allure environment properties to %s", env_file)

        # also write a JSON representation (some viewers/plugins expect environment.json)
        try:
            import json
            env_json = ar / "environment.json"
            with env_json.open("w", encoding="utf-8") as f:
                # convert to Allure expected array of {name, value}
                items = [{"name": k, "value": ("" if v is None else v)} for k, v in env.items()]
                json.dump(items, f, indent=2)
            logger.info("Wrote Allure environment json to %s", env_json)
        except Exception:
            logger.debug("Failed to write environment.json", exc_info=True)

        # write a minimal executor.json so Allure 'Executor' info is available (optional)
        try:
            import json
            executor = {
                "name": os.getenv("ALLURE_EXECUTOR_NAME", "local"),
                "type": os.getenv("ALLURE_EXECUTOR_TYPE", "local"),
                "url": os.getenv("ALLURE_EXECUTOR_URL", ""),
                "buildOrder": os.getenv("ALLURE_EXECUTOR_BUILDORDER", "1"),
            }
            exec_file = ar / "executor.json"
            with exec_file.open("w", encoding="utf-8") as f:
                json.dump(executor, f, indent=2)
            logger.info("Wrote Allure executor json to %s", exec_file)
        except Exception:
            logger.debug("Failed to write executor.json", exc_info=True)
    except Exception:
        logger.exception("Failed to write Allure environment properties")

    return env

@pytest.fixture(scope="session")
def driver_factory(env: Dict[str, Any]):
    """
    Factory to create Appium WebDriver sessions for native mobile automation.
    Returns a callable so tests can create additional sessions if needed.
    """

    def _create() -> AppiumWebDriver:
        server = env["APPIUM_SERVER"]
        platform = (env["PLATFORM_NAME"] or "Android").strip()

        legacy_caps: Dict[str, Any] = {}
        w3c_caps: Dict[str, Any] = {}

        # Standard W3C field
        w3c_caps["platformName"] = platform
        # device name (both forms)
        legacy_caps["deviceName"] = env["DEVICE_NAME"]
        w3c_caps["appium:deviceName"] = env["DEVICE_NAME"]

        # platform version (standard W3C key)
        if env.get("PLATFORM_VERSION"):
            legacy_caps["platformVersion"] = env["PLATFORM_VERSION"]
            w3c_caps["platformVersion"] = env["PLATFORM_VERSION"]

        # automationName (Appium-specific)
        if env.get("AUTOMATION_NAME"):
            legacy_caps["automationName"] = env["AUTOMATION_NAME"]
            w3c_caps["appium:automationName"] = env["AUTOMATION_NAME"]

        # udid (if specified)
        if env.get("UDID"):
            legacy_caps["udid"] = env["UDID"]
            w3c_caps["appium:udid"] = env["UDID"]

        # If APP_PATH (local apk) is provided and exists, include as 'app' / 'appium:app'
        app_path = os.getenv("APP_PATH") or env.get("APP_PATH")
        if app_path:
            if os.path.exists(app_path):
                abs_app_path = os.path.abspath(app_path)
                legacy_caps["app"] = abs_app_path
                w3c_caps["appium:app"] = abs_app_path
                # Try to install the APK on the device/emulator before starting session
                try:
                    import subprocess
                    logger.info("Attempting to install APK %s via adb", app_path)
                    res = subprocess.run(["adb", "install", "-r", app_path], capture_output=True, text=True, timeout=60)
                    if res.returncode == 0:
                        logger.info("APK installed successfully: %s", app_path)
                    else:
                        logger.warning("adb install returned non-zero exit status %s. stdout=%s stderr=%s", res.returncode, res.stdout, res.stderr)
                except Exception as e:
                    logger.exception("Failed to run adb install for %s: %s", app_path, e)
            else:
                logger.warning("APP_PATH is set in .env but file not found at: %s; skipping app capability", app_path)
                # If no app, then set package/activity
                if platform.lower() == "android":
                    if env.get("APP_PACKAGE"):
                        legacy_caps["appPackage"] = env["APP_PACKAGE"]
                        w3c_caps["appium:appPackage"] = env["APP_PACKAGE"]
                    if env.get("APP_ACTIVITY"):
                        legacy_caps["appActivity"] = env["APP_ACTIVITY"]
                        w3c_caps["appium:appActivity"] = env["APP_ACTIVITY"]
        else:
            # No app path, so set package/activity
            if platform.lower() == "android":
                if env.get("APP_PACKAGE"):
                    legacy_caps["appPackage"] = env["APP_PACKAGE"]
                    w3c_caps["appium:appPackage"] = env["APP_PACKAGE"]
                if env.get("APP_ACTIVITY"):
                    legacy_caps["appActivity"] = env["APP_ACTIVITY"]
                    w3c_caps["appium:appActivity"] = env["APP_ACTIVITY"]

        # Add additional capabilities from the working code
        w3c_caps["appium:ensureWebviewsHavePages"] = True
        w3c_caps["appium:nativeWebScreenshot"] = True
        w3c_caps["appium:newCommandTimeout"] = 3600
        w3c_caps["appium:connectHardwareKeyboard"] = True
        # Preserve the signed-in app state between sessions (do NOT clear data /
        # relaunch fresh) so the Health tests start from the already-paired,
        # logged-in app. Restored after recovery dropped this cap.
        w3c_caps["appium:noReset"] = True

        logger.info("Creating Appium session on %s with caps: %s", server, {k: v for k, v in w3c_caps.items() if k != "appium:udid"})
        # Use AppiumOptions as in the working code
        options = AppiumOptions()
        options.load_capabilities(w3c_caps)
        drv = appium_webdriver.Remote(command_executor=server, options=options)

        drv.implicitly_wait(env["IMPLICIT_WAIT"])
        return drv

    return _create
@pytest.fixture(scope="function")
def driver(driver_factory) -> AppiumWebDriver:

    if os.getenv("SKIP_APPIUM", "").strip().lower() in ("1", "true", "yes"):
        pytest.skip("SKIP_APPIUM is set; skipping Appium-dependent test")
    retries = int(os.getenv("APPIUM_CONNECT_RETRIES", "3"))
    delay = float(os.getenv("APPIUM_CONNECT_DELAY", "2"))
    attempt = 0
    while True:
        try:
            drv = driver_factory()
            break
        except Exception as e:
            attempt += 1
            logger.error("Failed to create Appium session (attempt %d/%d): %s", attempt, retries, e)
            if attempt >= retries:
                # Log full exception then re-raise to fail test setup loudly
                logger.exception("Exceeded Appium connection retries; giving up")
                raise
            logger.info("Retrying Appium connection in %s seconds...", delay)
            time.sleep(delay)
    yield drv
    try:
        drv.quit()
    except Exception:
        logger.exception("Error quitting driver")

@pytest.fixture(scope="function")
def app(driver: AppiumWebDriver) -> AppiumWebDriver:
    """
    For native apps this returns the active Appium session. There is no
    navigation to URLs because this suite is native/mobile-only.
    """
    logger.info("App session ready (native app).")
    return driver

# Fixture to set environment variables during a test and restore afterwards
@pytest.fixture
def set_env_var() -> Callable[[str, Optional[str]], None]:
    original: Dict[str, Optional[str]] = {}
    def _set(key: str, value: Optional[str]) -> None:
        if key not in original:
            original[key] = os.environ.get(key)
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[str(key)] = str(value)
    yield _set
    for k, v in original.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v

def add_env_to_dotenv(key: str, value: str, dotenv_path: Optional[Path] = None) -> None:
    path = dotenv_path or DOTENV_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = {}
    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                if "=" in line and not line.strip().startswith("#"):
                    k, _, v = line.partition("=")
                    existing[k.strip()] = v.strip()
    if key in existing:
        lines = []
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith(f"{key}="):
                    lines.append(f"{key}={value}\n")
                else:
                    lines.append(line)
        with path.open("w", encoding="utf-8") as f:
            f.writelines(lines)
    else:
        with path.open("a", encoding="utf-8") as f:
            if not path.exists() or path.stat().st_size > 0:
                f.write("\n")
            f.write(f"{key}={value}\n")
    load_dotenv(dotenv_path=path, override=True)
    logger.info("Wrote %s to %s and reloaded .env", key, path)

# ---------- pytest-bdd hooks ----------
def _ensure_screenshot_dir(path: str):
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p

def pytest_bdd_before_scenario(request, feature, scenario):
    logger.info("BDD START - feature: %s scenario: %s", getattr(feature, "name", feature), getattr(scenario, "name", scenario))
    # Make feature and scenario visible to Allure at the test level so the report groups
    # scenarios under the feature in the Allure UI.
    try:
        feat_name = getattr(feature, "name", feature)
        scen_name = getattr(scenario, "name", scenario)
        # Set dynamic feature/story/title for Allure. This helps show the feature as a top-level group.
        try:
            allure.dynamic.feature(feat_name)
        except Exception:
            # Older allure versions might not have dynamic; ignore safely
            pass
        try:
            allure.dynamic.title(scen_name)
        except Exception:
            pass
    except Exception:
        logger.debug("Failed to set Allure dynamic labels for scenario", exc_info=True)

def pytest_bdd_after_scenario(request, feature, scenario):
    logger.info("BDD END - feature: %s scenario: %s", getattr(feature, "name", feature), getattr(scenario, "name", scenario))
    # Attach teardown/reporting info at the scenario (top) level in Allure so it appears
    # under the feature in Allure's tree. We attach a short summary and a screenshot (if available).
    try:
        node = request.node
        rep = getattr(node, "rep_call", None)
        status = getattr(rep, "outcome", "unknown")
        feat_name = getattr(feature, "name", feature)
        scen_name = getattr(scenario, "name", scenario)
        summary = f"Feature: {feat_name}\nScenario: {scen_name}\nStatus: {status}"
        # attach a simple text summary to the scenario's Allure entry
        try:
            AllureLogger.attach_text(summary, name="scenario_summary.txt")
        except Exception:
            # fallback to direct allure.attach if helper fails
            try:
                allure.attach(summary, name="scenario_summary", attachment_type=allure.attachment_type.TEXT)
            except Exception:
                logger.debug("Failed to attach scenario summary to Allure", exc_info=True)

        # Attach a screenshot for visibility at the scenario level (preferred for teardown reporting)
        if "driver" in request.fixturenames:
            try:
                drv = request.getfixturevalue("driver")
                if drv:
                    try:
                        # prefer PNG bytes (driver.get_screenshot_as_png)
                        png = drv.get_screenshot_as_png()
                        if png:
                            AllureLogger.attach_bytes(png, name=f"screenshot-{scen_name}", mime_type="image/png")
                    except Exception:
                        # fallback to base64 if available
                        try:
                            b64 = drv.get_screenshot_as_base64()
                            AllureLogger.attach_screenshot_from_base64(b64, name=f"screenshot-{scen_name}")
                        except Exception:
                            logger.exception("Failed to capture/attach scenario screenshot")
            except Exception:
                logger.debug("Unable to get driver fixture for scenario-level screenshot", exc_info=True)
    except Exception:
        logger.debug("After-scenario Allure attachments failed", exc_info=True)

# MODIFICATION: Use Allure context managers to capture each BDD step as an Allure step and record timing.
def pytest_bdd_before_step(request, feature, scenario, step):
    # code for logging step name to cli
    logger.info("STEP START - %s", getattr(step, "name", step))
    try:
        node = request.node
        # ensure map exists on the node to track open Allure steps
        if not hasattr(node, "_bdd_allure_steps"):
            node._bdd_allure_steps = {}
        # start an allure step context for this BDD step and record start time
        try:
            step_ctx = allure.step(getattr(step, "name", str(step)))
            step_ctx.__enter__()
            node._bdd_allure_steps[id(step)] = (step_ctx, time.time())
        except Exception:
            logger.debug("Failed to start Allure step context for %s", getattr(step, "name", step), exc_info=True)
    except Exception:
        logger.debug("Before-step hook encountered an error", exc_info=True)

def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    step_name = getattr(step, "name", "Unknown Step")
    logger.error("STEP ERROR in Scenario '%s' - Step '%s': %s", scenario.name, step_name, exception)
    try:
        node = request.node
        if hasattr(node, "_bdd_allure_steps") and id(step) in node._bdd_allure_steps:
            step_ctx, start = node._bdd_allure_steps.pop(id(step))
            try:
                # pass exception info to the context manager so Allure marks the step failed with traceback
                step_ctx.__exit__(type(exception), exception, exception.__traceback__)
            except Exception:
                logger.debug("Failed to close Allure step context on error for %s", step_name, exc_info=True)
        # existing failure handling: capture screenshot and attach
        drv = request.getfixturevalue("driver") if "driver" in request.fixturenames else None
        if drv:
            sd = _ensure_screenshot_dir(request.getfixturevalue("env")["SCREENSHOT_DIR"])
            fname = sd / f"fail-{scenario.name.replace(' ', '_')}-{step.name.replace(' ', '_')}.png"
            try:
                drv.save_screenshot(str(fname))
                logger.info("Saved failure screenshot to %s", fname)
                try:
                    AllureLogger.attach_file(fname, name=f"step_fail_{step.name}")
                except Exception:
                    try:
                        with open(fname, "rb") as f:
                            allure.attach(f.read(), name=f"step_fail_{step.name}", attachment_type=allure.attachment_type.PNG)
                    except Exception:
                        logger.debug("Failed to attach step-level screenshot to Allure", exc_info=True)
            except Exception:
                logger.exception("Failed to save screenshot")
    except Exception:
        logger.debug("Step-error hook encountered an error", exc_info=True)

def pytest_bdd_after_step(request, feature, scenario, step, step_func):
    logger.info("STEP END - %s", getattr(step, "name", step))
    try:
        node = request.node
        # if an allure step context was opened for this BDD step, close it here and attach duration
        if hasattr(node, "_bdd_allure_steps") and id(step) in node._bdd_allure_steps:
            step_ctx, start = node._bdd_allure_steps.pop(id(step))
            try:
                # close successful step
                step_ctx.__exit__(None, None, None)
            except Exception:
                logger.debug("Failed to close Allure step context for %s", getattr(step, "name", step), exc_info=True)
            try:
                duration = time.time() - start
                # attach duration as a simple text attachment so it shows in Allure
                try:
                    AllureLogger.attach_text(f"{duration:.4f} seconds", name=f"step_duration_{step.name}")
                except Exception:
                    try:
                        allure.attach(f"{duration:.4f} seconds", name=f"step_duration_{step.name}", attachment_type=allure.attachment_type.TEXT)
                    except Exception:
                        logger.debug("Failed to attach step duration to Allure", exc_info=True)
            except Exception:
                logger.debug("Failed to compute/attach duration for step %s", getattr(step, "name", step), exc_info=True)

        # keep existing behavior: if the overall test call failed, attach screenshot at step level
        rep = getattr(node, "rep_call", None)
        if rep and rep.failed:
            drv = request.getfixturevalue("driver") if "driver" in request.fixturenames else None
            if drv:
                sd = _ensure_screenshot_dir(request.getfixturevalue("env")["SCREENSHOT_DIR"])
                fname = sd / f"fail-{scenario.name.replace(' ', '_')}-{step.name.replace(' ', '_')}.png"
                try:
                    drv.save_screenshot(str(fname))
                    logger.info("Saved failure screenshot to %s", fname)
                    try:
                        AllureLogger.attach_file(fname, name=f"step_fail_{step.name}")
                    except Exception:
                        try:
                            with open(fname, "rb") as f:
                                allure.attach(f.read(), name=f"step_fail_{step.name}", attachment_type=allure.attachment_type.PNG)
                        except Exception:
                            logger.debug("Failed to attach step-level screenshot to Allure", exc_info=True)
                except Exception:
                    logger.exception("Failed to save screenshot")
    except Exception:
        logger.debug("After step hook encountered an error", exc_info=True)

# ---------- Reusable BDD steps ----------
@given("the app is open")
def given_app_open(app: AppiumWebDriver, env: Dict[str, Any]):
    # For native apps just ensure session exists
    assert app.session_id, "No active app session"

@when(parsers.parse('I click the element with {by} "{selector}"'))
def when_click_selector(app: AppiumWebDriver, by: str, selector: str):
    """
    Generic mobile click step. Supported `by` values (case-insensitive):
      - xpath
      - id (resource-id / id)
      - accessibility_id
      - class_name
    """
    by_key = by.strip().lower()
    try:
        if by_key in ("id", "resource-id"):
            el = app.find_element(AppiumBy.ID, selector)
        elif by_key in ("xpath",):
            el = app.find_element(AppiumBy.XPATH, selector)
        elif by_key in ("accessibility_id", "accessibilityid", "accessibility-id"):
            el = app.find_element(AppiumBy.ACCESSIBILITY_ID, selector)
        elif by_key in ("class_name", "class", "classname"):
            el = app.find_element(AppiumBy.CLASS_NAME, selector)
        else:
            # default to xpath if unknown
            el = app.find_element(AppiumBy.XPATH, selector)
        el.click()
    except Exception:
        logger.exception("Failed to click element (%s: %s)", by, selector)
        raise

@then(parsers.parse('I should see text "{text}" on the page'))
def then_see_text(app: AppiumWebDriver, text: str):
    # For native apps, page_source often contains view text
    assert text in app.page_source, f"Expected text '{text}' not found on page"


@step('the user accepts the notifications pop-up')
def accept_notifications_popup(driver: AppiumWebDriver):
    try:
        TERM_CONDITIONS = (AppiumBy.XPATH, '//android.widget.Button[contains(@resource-id,"btnAgree")]')
        driver.find_element(*TERM_CONDITIONS).click()
    except Exception:
        pass


    try:
        alert = driver.switch_to.alert
        alert.accept()
    except Exception:
        pass

def _write_allure_env_files(env_dict: Dict[str, Any], results_dir: Optional[str] = None) -> None:
    """Write environment.properties, environment.json and executor.json into results_dir.
    This is a helper used by the env fixture and by pytest_configure so files are present
    early in the pytest run (useful when Allure UI expects files to exist in the results dir).
    """
    try:
        rd = Path(results_dir) if results_dir else (Path(os.getenv("ALLURE_RESULTS_DIR", "allure-results")))
        # if pytest passed a relative path (like 'allure-results'), ensure it's rooted at cwd
        if not rd.is_absolute():
            rd = Path(os.getcwd()) / rd
        rd.mkdir(parents=True, exist_ok=True)

        # environment.properties (Allure's standard simple key=value file)
        env_props = rd / "environment.properties"
        with env_props.open("w", encoding="utf-8") as f:
            for k, v in env_dict.items():
                val = "" if v is None else str(v)
                f.write(f"{k}={val}\n")
        logger.info("Wrote Allure environment properties to %s", env_props)

        # environment.json (some tools/plugins expect JSON)
        try:
            import json
            env_json = rd / "environment.json"
            items = [{"name": k, "value": ("" if v is None else v)} for k, v in env_dict.items()]
            with env_json.open("w", encoding="utf-8") as f:
                json.dump(items, f, indent=2)
            logger.info("Wrote Allure environment json to %s", env_json)
        except Exception:
            logger.debug("Failed to write environment.json", exc_info=True)

        # executor.json (optional metadata for Allure)
        try:
            import json
            executor = {
                "name": os.getenv("ALLURE_EXECUTOR_NAME", "local"),
                "type": os.getenv("ALLURE_EXECUTOR_TYPE", "local"),
                "url": os.getenv("ALLURE_EXECUTOR_URL", ""),
                "buildOrder": os.getenv("ALLURE_EXECUTOR_BUILDORDER", "1"),
            }
            exec_file = rd / "executor.json"
            with exec_file.open("w", encoding="utf-8") as f:
                json.dump(executor, f, indent=2)
            logger.info("Wrote Allure executor json to %s", exec_file)
        except Exception:
            logger.debug("Failed to write executor.json", exc_info=True)
    except Exception:
        logger.exception("Failed to write Allure environment files to %s", results_dir)


def pytest_configure(config):
    """Pytest hook: runs early during pytest startup. Write Allure environment files to the
    configured --alluredir so the Allure UI shows the environment information.
    """
    try:
        alluredir = None
        try:
            # pytest may expose the alluredir option if allure plugin is active
            alluredir = config.getoption("alluredir")
        except Exception:
            # fallback to env var or default
            alluredir = os.getenv("ALLURE_RESULTS_DIR", "allure-results")

        # Build a minimal env dict from environment variables (same keys as env fixture)
        env_dict = {
            "APPIUM_SERVER": os.getenv("APPIUM_SERVER", "http://127.0.0.1:4723"),
            "PLATFORM_NAME": os.getenv("PLATFORM_NAME", "Android"),
            "DEVICE_NAME": os.getenv("DEVICE_NAME", "emulator-5554"),
            "PLATFORM_VERSION": os.getenv("PLATFORM_VERSION", ""),
            "AUTOMATION_NAME": os.getenv("AUTOMATION_NAME", "UiAutomator2"),
            "APP_PACKAGE": os.getenv("APP_PACKAGE", ""),
            "APP_ACTIVITY": os.getenv("APP_ACTIVITY", ""),
            "UDID": os.getenv("UDID", ""),
            "IMPLICIT_WAIT": os.getenv("IMPLICIT_WAIT", "5"),
        }
        _write_allure_env_files(env_dict, alluredir)
    except Exception:
        logger.debug("pytest_configure failed to write Allure environment files", exc_info=True)

def pytest_sessionstart(session):
    """Pytest hook: called after the Session object has been created and before performing collection.
    Writing the Allure environment files here ensures they are present after any cleaning that
    the allure plugin may perform at test startup (e.g., --clean-alluredir).
    """
    try:
        config = session.config
        alluredir = None
        try:
            alluredir = config.getoption("alluredir")
        except Exception:
            alluredir = os.getenv("ALLURE_RESULTS_DIR", "allure-results")

        env_dict = {
            "APPIUM_SERVER": os.getenv("APPIUM_SERVER", "http://127.0.0.1:4723"),
            "PLATFORM_NAME": os.getenv("PLATFORM_NAME", "Android"),
            "DEVICE_NAME": os.getenv("DEVICE_NAME", "emulator-5554"),
            "PLATFORM_VERSION": os.getenv("PLATFORM_VERSION", ""),
            "AUTOMATION_NAME": os.getenv("AUTOMATION_NAME", "UiAutomator2"),
            "APP_PACKAGE": os.getenv("APP_PACKAGE", ""),
            "APP_ACTIVITY": os.getenv("APP_ACTIVITY", ""),
            "UDID": os.getenv("UDID", ""),
            "IMPLICIT_WAIT": os.getenv("IMPLICIT_WAIT", "5"),
        }
        _write_allure_env_files(env_dict, alluredir)
    except Exception:
        logger.debug("pytest_sessionstart failed to write Allure environment files", exc_info=True)
