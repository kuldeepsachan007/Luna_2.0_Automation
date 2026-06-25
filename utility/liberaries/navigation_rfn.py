# Minimal navigation helpers for reusable functions
from appium.webdriver.webdriver import WebDriver as AppiumWebDriver


def go_back(driver: AppiumWebDriver) -> None:
    try:
        driver.back()
    except Exception:
        pass


def refresh_page(driver: AppiumWebDriver) -> None:
    try:
        driver.refresh()
    except Exception:
        pass
