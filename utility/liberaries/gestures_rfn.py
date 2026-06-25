# Minimal wrapper functions for gesture operations expected by reusable_functions
from typing import Optional
from appium.webdriver.webdriver import WebDriver as AppiumWebDriver
from . import gesture_control as gc  # type: ignore


def swipe_up(driver: AppiumWebDriver, duration: int = 800) -> bool:
    """Swipe up using gesture_control helpers."""
    try:
        return gc.swipe_in_direction(driver, direction="up", percent=0.5, duration_ms=duration)
    except Exception:
        return False


def scroll_to_element(driver: AppiumWebDriver, locator, max_swipes: int = 5, direction: str = "up"):
    try:
        return gc.swipe_until_element_visible(driver, locator, max_swipes=max_swipes, direction=direction)
    except Exception:
        return None


def drag_and_drop(driver: AppiumWebDriver, source, target, duration_ms: int = 800) -> bool:
    try:
        return gc.drag_and_drop(driver, source, target, duration_ms=duration_ms)
    except Exception:
        return False
