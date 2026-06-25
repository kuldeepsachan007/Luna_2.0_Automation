# python
from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, Optional, List
from appium.webdriver.webdriver import WebDriver as AppiumWebDriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


@dataclass(frozen=True)
class Locator:
    """
    Simple data container for mobile locators.
    strategy: one of the keys handled in `to_by` (e.g. 'id', 'xpath', 'accessibility_id', ...)
    selector: the selector string
    """
    strategy: str
    selector: str

    def to_by(self) -> Tuple[str, str]:
        """Map the logical strategy to AppiumBy constant and return (by, selector)."""
        s = self.strategy.lower()
        if s in ("id", "resource_id", "android_resource_id"):
            return (AppiumBy.ID, self.selector)
        if s in ("xpath",):
            return (AppiumBy.XPATH, self.selector)
        if s in ("accessibility_id", "accessibilityid", "acc_id"):
            return (AppiumBy.ACCESSIBILITY_ID, self.selector)
        if s in ("class_name", "class"):
            return (AppiumBy.CLASS_NAME, self.selector)
        if s in ("android_uiautomator", "android_ui_automator", "ui_automator"):
            return (AppiumBy.ANDROID_UIAUTOMATOR, self.selector)
        if s in ("ios_predicate", "ios_pred"):
            return (AppiumBy.IOS_PREDICATE, self.selector)
        if s in ("ios_class_chain", "ios_chain"):
            return (AppiumBy.IOS_CLASS_CHAIN, self.selector)
        # Fallback to xpath if unknown looks like xpath, otherwise use ID as last resort
        return (AppiumBy.XPATH if self.selector.strip().startswith("/") else AppiumBy.ID, self.selector)


# Factory helpers for common mobile locator strategies
def by_id(selector: str) -> Locator:
    return Locator("id", selector)


def by_xpath(selector: str) -> Locator:
    return Locator("xpath", selector)


def by_accessibility_id(selector: str) -> Locator:
    return Locator("accessibility_id", selector)


def by_class_name(selector: str) -> Locator:
    return Locator("class_name", selector)


def by_android_uiautomator(selector: str) -> Locator:
    return Locator("android_uiautomator", selector)


def by_ios_predicate(selector: str) -> Locator:
    return Locator("ios_predicate", selector)


def by_ios_class_chain(selector: str) -> Locator:
    return Locator("ios_class_chain", selector)


# Lightweight find wrappers that wait for presence (mobile\-focused)
def find_element(driver: AppiumWebDriver, locator: Locator, timeout: int = 10):
    """
    Wait until a single element is present and return it.
    Raises TimeoutException on timeout.
    """
    by, sel = locator.to_by()
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, sel)))


def find_elements(driver: AppiumWebDriver, locator: Locator, timeout: int = 5) -> List:
    """
    Wait up to `timeout` seconds for at least zero elements to be retrievable.
    Returns a list (may be empty). Does not raise on zero results; only on internal errors.
    """
    by, sel = locator.to_by()
    try:
        WebDriverWait(driver, timeout).until(lambda d: d.find_elements(by, sel) is not None)
    except TimeoutException:
        return []
    return driver.find_elements(by, sel)


__all__ = [
    "Locator",
    "by_id",
    "by_xpath",
    "by_accessibility_id",
    "by_class_name",
    "by_android_uiautomator",
    "by_ios_predicate",
    "by_ios_class_chain",
    "find_element",
    "find_elements",
]
