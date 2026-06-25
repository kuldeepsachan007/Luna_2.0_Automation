import logging
from typing import List

from appium.webdriver.webdriver import WebDriver as AppiumWebDriver
from appium.webdriver.webelement import WebElement as AppiumWebElement
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    NoSuchElementException,
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utility.liberaries.mouse import Locator, resolve_locator

logger = logging.getLogger(__name__)
explicit_waits = 10000
implicit_waits = 5000
polling_time = 500

DEFAULT_TIMEOUT = 10
DEFAULT_POLL_FREQUENCY = 0.5
IGNORED_EXCEPTIONS = (StaleElementReferenceException, NoSuchElementException)


def _build_wait(driver: AppiumWebDriver, timeout: int = DEFAULT_TIMEOUT, poll: float = DEFAULT_POLL_FREQUENCY) -> WebDriverWait:
    return WebDriverWait(driver, timeout, poll_frequency=poll, ignored_exceptions=IGNORED_EXCEPTIONS)


def wait_for_presence(driver: AppiumWebDriver, locator: Locator, timeout: int = DEFAULT_TIMEOUT) -> AppiumWebElement:
    by, value = resolve_locator(locator)
    logger.info(f"Waiting for presence of element: ({by}, {value})")
    return _build_wait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )


def wait_for_all_present(driver: AppiumWebDriver, locator: Locator, timeout: int = DEFAULT_TIMEOUT) -> List[AppiumWebElement]:
    by, value = resolve_locator(locator)
    logger.info(f"Waiting for all elements present: ({by}, {value})")
    return _build_wait(driver, timeout).until(
        EC.presence_of_all_elements_located((by, value))
    )


def wait_for_visible(driver: AppiumWebDriver, locator: Locator, timeout: int = DEFAULT_TIMEOUT) -> AppiumWebElement:
    by, value = resolve_locator(locator)
    logger.info(f"Waiting for visibility of element: ({by}, {value})")
    return _build_wait(driver, timeout).until(
        EC.visibility_of_element_located((by, value))
    )


def wait_for_all_visible(driver: AppiumWebDriver, locator: Locator, timeout: int = DEFAULT_TIMEOUT) -> List[AppiumWebElement]:
    by, value = resolve_locator(locator)
    logger.info(f"Waiting for all elements visible: ({by}, {value})")
    return _build_wait(driver, timeout).until(
        EC.visibility_of_any_elements_located((by, value))
    )


def wait_for_clickable(driver: AppiumWebDriver, locator: Locator, timeout: int = DEFAULT_TIMEOUT) -> AppiumWebElement:
    by, value = resolve_locator(locator)
    logger.info(f"Waiting for element to be clickable: ({by}, {value})")
    return _build_wait(driver, timeout).until(
        EC.element_to_be_clickable((by, value))
    )


def wait_for_invisible(driver: AppiumWebDriver, locator: Locator, timeout: int = DEFAULT_TIMEOUT) -> bool:
    by, value = resolve_locator(locator)
    logger.info(f"Waiting for element to disappear: ({by}, {value})")
    return _build_wait(driver, timeout).until(
        EC.invisibility_of_element_located((by, value))
    )


def wait_for_text_present(driver: AppiumWebDriver, locator: Locator, text: str, timeout: int = DEFAULT_TIMEOUT) -> bool:
    by, value = resolve_locator(locator)
    logger.info(f"Waiting for text '{text}' in element: ({by}, {value})")
    return _build_wait(driver, timeout).until(
        EC.text_to_be_present_in_element((by, value), text)
    )


def wait_and_click(driver: AppiumWebDriver, locator: Locator, timeout: int = DEFAULT_TIMEOUT) -> None:
    element = wait_for_clickable(driver, locator, timeout)
    element.click()
    logger.info(f"Clicked element: {locator}")


def wait_and_send_keys(driver: AppiumWebDriver, locator: Locator, text: str, timeout: int = DEFAULT_TIMEOUT, clear_first: bool = True) -> None:
    element = wait_for_clickable(driver, locator, timeout)
    if clear_first:
        element.clear()
    element.send_keys(text)
    logger.info(f"Sent keys to element: {locator}")


def wait_and_get_text(driver: AppiumWebDriver, locator: Locator, timeout: int = DEFAULT_TIMEOUT) -> str:
    element = wait_for_visible(driver, locator, timeout)
    text = element.text or element.get_attribute("content-desc") or ""
    logger.info(f"Got text '{text}' from element: {locator}")
    return text


def is_element_present(driver: AppiumWebDriver, locator: Locator, timeout: int = 3) -> bool:
    try:
        wait_for_presence(driver, locator, timeout)
        return True
    except TimeoutException:
        return False


def wait_for_element_attribute(
    driver: AppiumWebDriver,
    locator: Locator,
    attribute: str,
    value: str,
    timeout: int = DEFAULT_TIMEOUT,
) -> bool:
    by, loc_value = resolve_locator(locator)
    logger.info(f"Waiting for attribute '{attribute}'='{value}' on element: ({by}, {loc_value})")

    def _check(d):
        el = d.find_element(by, loc_value)
        return el.get_attribute(attribute) == value

    return _build_wait(driver, timeout).until(_check)
