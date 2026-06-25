# Minimal device helpers
from appium.webdriver.webdriver import WebDriver as AppiumWebDriver


def take_screenshot(driver: AppiumWebDriver, file_path: str) -> None:
    try:
        driver.save_screenshot(file_path)
    except Exception:
        pass


def send_app_to_background(driver: AppiumWebDriver, seconds: int) -> None:
    try:
        driver.background_app(seconds)
    except Exception:
        try:
            driver.background_app(seconds)
        except Exception:
            pass


def bring_app_to_foreground(driver: AppiumWebDriver) -> None:
    try:
        # no generic cross-platform action; try launching current package if available
        driver.activate_app(driver.capabilities.get('appPackage') or '')
    except Exception:
        pass
