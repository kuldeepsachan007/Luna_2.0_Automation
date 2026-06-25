# Minimal alert handling for mobile
from appium.webdriver.webdriver import WebDriver as AppiumWebDriver


def handle_alert(driver: AppiumWebDriver, accept: bool = True, timeout: int = 5) -> None:
    try:
        # attempt to accept/dismiss native alert if present
        alert = driver.switch_to.alert
        if accept:
            alert.accept()
        else:
            alert.dismiss()
    except Exception:
        # ignore if no alert or not supported
        pass


def handle_modal_dialog(driver: AppiumWebDriver, accept: bool = True, timeout: int = 5) -> None:
    # same as handle_alert for now
    handle_alert(driver, accept=accept, timeout=timeout)
