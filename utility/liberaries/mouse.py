# python
from typing import Union, Tuple, List, Optional
import time
import logging

from appium.webdriver.webdriver import WebDriver as AppiumWebDriver
from appium.webdriver.webelement import WebElement as AppiumWebElement
from appium.webdriver.common.appiumby import AppiumBy


from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
    WebDriverException,
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utility.liberaries.locators import Locator as MobileLocator

logger = logging.getLogger(__name__)

# Accept tuple, string or MobileLocator
Locator = Union[Tuple[str, str], str, MobileLocator]


def resolve_locator(locator: Locator) -> Tuple[str, str]:
    """
    Normalize locator into (by, value).
    Accepts:
      - MobileLocator instances (preferred for mobile)
      - tuple (by, value)
      - string like "id=foo", "xpath=//..", "accessibility_id=foo"
    Returns AppiumBy constants or tuples Appium understands.
    """
    # MobileLocator instance -> use its mapping
    if isinstance(locator, MobileLocator):
        return locator.to_by()

    if isinstance(locator, tuple):
        return locator  # type: ignore

    if not isinstance(locator, str):
        raise ValueError("locator must be a MobileLocator, tuple or string")

    # allow separators '=' or ':'
    for sep in ("=", ":"):
        if sep in locator:
            strategy, value = locator.split(sep, 1)
            strategy = strategy.strip().lower()
            value = value.strip()
            if strategy in ("id", "resource_id", "android_resource_id"):
                return (AppiumBy.ID, value)
            if strategy in ("xpath",):
                return (AppiumBy.XPATH, value)
            if strategy in ("accessibility_id", "accessibilityid", "aid"):
                return (AppiumBy.ACCESSIBILITY_ID, value)
            if strategy in ("class", "class_name", "classname"):
                return (AppiumBy.CLASS_NAME, value)
            if strategy in ("android_uiautomator", "android_ui_automator", "ui_automator", "uiautomator"):
                return (AppiumBy.ANDROID_UIAUTOMATOR, value)
            if strategy in ("ios_predicate", "ios_pred"):
                return (AppiumBy.IOS_PREDICATE, value)
            if strategy in ("ios_class_chain", "ios_chain"):
                return (AppiumBy.IOS_CLASS_CHAIN, value)
            # unknown strategy -> treat remainder as xpath if looks like one
            break

    # fallback: if looks like xpath
    s = locator.strip()
    if s.startswith("/") or s.startswith("(") or s.startswith(".//") or s.startswith("//"):
        return (AppiumBy.XPATH, s)
    # else treat as ID
    return (AppiumBy.ID, s)


def find_element(driver: AppiumWebDriver, locator: Locator, timeout: int = 10) -> AppiumWebElement:
    """
    Wait for presence of element and return it.
    Raises TimeoutException if not found.
    """
    by, value = resolve_locator(locator)
    wait = WebDriverWait(driver, timeout)
    try:
        return wait.until(EC.presence_of_element_located((by, value)))
    except Exception as e:
        logger.debug("find_element(%s) failed: %s", locator, e)
        raise


def find_elements(driver: AppiumWebDriver, locator: Locator, timeout: int = 5) -> List[AppiumWebElement]:
    """
    Wait up to `timeout` seconds and return list (may be empty).
    """
    by, value = resolve_locator(locator)
    wait = WebDriverWait(driver, timeout)
    try:
        wait.until(lambda d: d.find_elements(by, value) is not None)
    except Exception:
        logger.debug("find_elements wait finished for %s", locator)
    try:
        return driver.find_elements(by, value)
    except Exception as e:
        logger.debug("find_elements(%s) exception: %s", locator, e)
        return []


def _wait_for_interactable(driver: AppiumWebDriver, by: str, value: str, timeout: int = 10) -> AppiumWebElement:
    """
    Mobile-friendly wait: presence then ensure displayed/enabled when possible.
    """
    end = time.time() + timeout
    el = find_element(driver, (by, value), timeout=timeout)
    while time.time() < end:
        try:
            if getattr(el, "is_displayed", lambda: True)() and getattr(el, "is_enabled", lambda: True)():
                return el
        except StaleElementReferenceException:
            el = find_element(driver, (by, value), timeout=timeout)
        time.sleep(0.2)
    return el


def _touchaction_tap(driver: AppiumWebDriver, element: Optional[AppiumWebElement] = None, x: Optional[int] = None, y: Optional[int] = None) -> bool:
    try:
        from appium.webdriver.common.touch_action import TouchAction  # type: ignore
        ta = TouchAction(driver)
        if element is not None:
            ta.tap(element).perform()
        else:
            if x is None or y is None:
                return False
            ta.tap(None, x, y).perform()
        return True
    except Exception as e:
        logger.debug("TouchAction tap failed: %s", e)
        return False


def click(
    driver: AppiumWebDriver,
    locator: Locator,
    timeout: int = 10,
    attempts: int = 3,
    retry_delay: float = 0.5,
) -> None:
    """
    Robust mobile click/tap:
    - waits for element presence and basic interactability
    - prefers native .click() then TouchAction tap then 'mobile: tap' by coordinates
    - retries on common transient errors
    """
    by, value = resolve_locator(locator)
    last_exception: Optional[Exception] = None

    for attempt in range(1, attempts + 1):
        try:
            el = _wait_for_interactable(driver, by, value, timeout=timeout)
            try:
                el.click()
                return
            except (ElementClickInterceptedException, StaleElementReferenceException, WebDriverException) as e:
                logger.debug("Direct click failed (attempt %s): %s", attempt, e)
                last_exception = e
                # TouchAction on element
                if _touchaction_tap(driver, element=el):
                    return
                # Tap by coordinates (center)
                try:
                    rect = el.rect
                    cx = int(rect.get("x", 0) + rect.get("width", 0) / 2)
                    cy = int(rect.get("y", 0) + rect.get("height", 0) / 2)
                    # try 'mobile: tap' first (modern Appium)
                    try:
                        driver.execute_script("mobile: tap", {"x": cx, "y": cy})
                        return
                    except Exception:
                        pass
                    if _touchaction_tap(driver, x=cx, y=cy):
                        return
                except Exception as e2:
                    logger.debug("coordinate click fallback failed: %s", e2)
                # continue retry loop
            except Exception as e:
                last_exception = e
                logger.debug("Unexpected click exception: %s", e)
                raise
        except TimeoutException as e:
            last_exception = e
            logger.debug("Timeout waiting for interactable %s: %s", locator, e)
        except Exception as e:
            last_exception = e
            logger.debug("Error finding/clicking %s: %s", locator, e)

        if attempt < attempts:
            time.sleep(retry_delay)

    if last_exception:
        raise last_exception
    raise RuntimeError(f"Unable to click {locator}")


def click_coordinates(driver: AppiumWebDriver, x: int, y: int) -> bool:
    """
    Click or tap at absolute screen coordinates using Appium-first strategies.
    """
    try:
        # Try modern mobile: tap
        try:
            driver.execute_script("mobile: tap", {"x": x, "y": y})
            return True
        except Exception:
            pass

        # TouchAction fallback
        if _touchaction_tap(driver, x=x, y=y):
            return True

    except Exception as e:
        logger.debug("click_coordinates failed: %s", e)
    return False



