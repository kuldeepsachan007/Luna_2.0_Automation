# python
from typing import Any
from appium.webdriver.webdriver import WebDriver as AppiumWebDriver
from selenium.common.exceptions import TimeoutException

from .mouse import find_element, find_elements, Locator  # type: ignore
from . import forms_rfn as fr  # type: ignore
from . import mouse_rfn as mr  # type: ignore


def _resolve_element(driver: AppiumWebDriver, locator: Locator, timeout: int = 10):
    """
    Find a single element or raise the underlying exception (e.g. TimeoutException).
    """
    return find_element(driver, locator, timeout=timeout)


def _resolve_elements(driver: AppiumWebDriver, locator: Locator, timeout: int = 5):
    """
    Return list of elements (may be empty) after waiting briefly.
    """
    return find_elements(driver, locator, timeout=timeout)


def safe_clear(driver: AppiumWebDriver, locator: Locator, timeout: int = 10) -> None:
    el = _resolve_element(driver, locator, timeout=timeout)
    fr.safe_clear(el)


def safe_send_keys(
    driver: AppiumWebDriver,
    locator: Locator,
    text: str,
    timeout: int = 10,
    attempts: int = 3,
    retry_delay: float = 0.2,
) -> None:
    el = _resolve_element(driver, locator, timeout=timeout)
    fr.safe_send_keys(el, text, driver=driver, attempts=attempts, retry_delay=retry_delay)


def set_input_value(
    driver: AppiumWebDriver,
    locator: Locator,
    value: str,
    timeout: int = 10,
    attempts: int = 3,
    retry_delay: float = 0.2,
    use_mobile_fallback: bool = True,
) -> None:
    el = _resolve_element(driver, locator, timeout=timeout)
    fr.set_input_value(el, value, driver=driver, attempts=attempts, retry_delay=retry_delay, use_mobile_fallback=use_mobile_fallback)


def append_input_value(
    driver: AppiumWebDriver,
    locator: Locator,
    text: str,
    timeout: int = 10,
) -> None:
    el = _resolve_element(driver, locator, timeout=timeout)
    fr.append_input_value(el, text, driver=driver)


def select_option_by_value(driver: AppiumWebDriver, locator: Locator, value: str, timeout: int = 10) -> None:
    el = _resolve_element(driver, locator, timeout=timeout)
    fr.select_option_by_value(el, value)


def select_option_by_visible_text(driver: AppiumWebDriver, locator: Locator, text: str, timeout: int = 10) -> None:
    el = _resolve_element(driver, locator, timeout=timeout)
    fr.select_option_by_visible_text(el, text)


def select_option_by_index(driver: AppiumWebDriver, locator: Locator, index: int, timeout: int = 10) -> None:
    el = _resolve_element(driver, locator, timeout=timeout)
    fr.select_option_by_index(el, index)


def is_checked(driver: AppiumWebDriver, locator: Locator, timeout: int = 5) -> bool:
    el = _resolve_element(driver, locator, timeout=timeout)
    return fr.is_checked(el)


def ensure_checked(driver: AppiumWebDriver, locator: Locator, timeout: int = 10) -> None:
    el = _resolve_element(driver, locator, timeout=timeout)
    fr.ensure_checked(el, driver=driver)


def ensure_unchecked(driver: AppiumWebDriver, locator: Locator, timeout: int = 10) -> None:
    el = _resolve_element(driver, locator, timeout=timeout)
    fr.ensure_unchecked(el, driver=driver)


def get_value(driver: AppiumWebDriver, locator: Locator, timeout: int = 10) -> Any:
    el = _resolve_element(driver, locator, timeout=timeout)
    return fr.get_value(el)


def submit_form(driver: AppiumWebDriver, locator: Locator, timeout: int = 10) -> None:
    """
    Submit the form that contains the matched element.
    """
    el = _resolve_element(driver, locator, timeout=timeout)
    fr.submit_form(el)

def is_element_displayed(driver: AppiumWebDriver, locator: Locator, timeout: int = 5) -> bool:
    """
    Check if the element located by `locator` is displayed within the given timeout.
    """
    try:
        el = _resolve_element(driver, locator, timeout=timeout)
        return fr.is_element_displayed(el)
    except TimeoutException:
        return False

def click_option_from_list(
    driver: AppiumWebDriver,
    locator: Locator,
    index: int = 0,
    timeout: int = 5,
    **click_kwargs,
) -> None:
    """
    Helper to click an item from a list of matched elements using the element-based click helper.
    `click_kwargs` are forwarded to mr.click_element if present (kept for compatibility).
    """
    elements = _resolve_elements(driver, locator, timeout=timeout)
    if not elements:
        raise TimeoutException(f"No elements found for {locator}")
    if index < 0 or index >= len(elements):
        raise IndexError("index out of range for elements list")
    mr.click_element(elements[index], driver=driver, **click_kwargs)
