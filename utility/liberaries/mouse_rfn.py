# python
from typing import Optional, List
import time
import logging

# Use Appium types for mobile automation
from appium.webdriver.webdriver import WebDriver as AppiumWebDriver
from appium.webdriver.webelement import WebElement as AppiumWebElement
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    StaleElementReferenceException,
    WebDriverException,
)

logger = logging.getLogger(__name__)


def _get_driver_from_element(element: AppiumWebElement) -> Optional[AppiumWebDriver]:
    # Try common internal references to obtain driver from an Appium WebElement
    return getattr(element, "parent", None) or getattr(element, "_parent", None)


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
        logger.debug("TouchAction tap failed or not available: %s", e)
        return False


def click_coordinates(driver: AppiumWebDriver, x: int, y: int) -> bool:
    """
    Tap at absolute screen coordinates using Appium-first strategies.
    Returns True on success, False on failure.
    """
    try:
        # Try modern mobile: tap (preferred)
        try:
            driver.execute_script("mobile: tap", {"x": x, "y": y})
            return True
        except Exception as e:
            logger.debug("mobile: tap not available or failed: %s", e)

        # TouchAction fallback
        try:
            if _touchaction_tap(driver, x=x, y=y):
                return True
        except Exception:
            pass

    except Exception as e:
        logger.debug("click_coordinates failed: %s", e)
    return False


def click_element(
    element: AppiumWebElement,
    driver: Optional[AppiumWebDriver] = None,
    attempts: int = 3,
    retry_delay: float = 0.5,
    ensure_visible: bool = True,
) -> None:
    """
    Robustly click an already found AppiumWebElement.
    - element: an AppiumWebElement instance
    - driver: optional AppiumWebDriver; if omitted it is inferred from the element
    - attempts: number of attempts before giving up
    - retry_delay: seconds between attempts
    - ensure_visible: if True, checks is_displayed() and is_enabled() before clicking
    Raises the last encountered exception on failure.
    """
    last_exception: Optional[Exception] = None
    drv = driver or _get_driver_from_element(element)

    for attempt in range(1, attempts + 1):
        try:
            # Basic visibility/enabled check
            try:
                if ensure_visible:
                    displayed = getattr(element, "is_displayed", lambda: True)()
                    enabled = getattr(element, "is_enabled", lambda: True)()
                    if not displayed or not enabled:
                        raise WebDriverException("Element not visible/enabled")
            except StaleElementReferenceException as e:
                # Element became stale — re-raise to be handled below
                raise e

            try:
                element.click()
                return
            except (ElementClickInterceptedException, StaleElementReferenceException, WebDriverException) as e:
                logger.debug("Direct click failed (attempt %s): %s", attempt, e)
                last_exception = e
                # try TouchAction (Appium)
                if drv and _touchaction_tap(drv, element=element):
                    return
                # try center coordinate click
                try:
                    rect = element.rect
                    cx = int(rect.get("x", 0) + rect.get("width", 0) / 2)
                    cy = int(rect.get("y", 0) + rect.get("height", 0) / 2)
                    if drv and click_coordinates(drv, cx, cy):
                        return
                except Exception as e2:
                    logger.debug("coordinate click fallback failed: %s", e2)
                # continue to next attempt
            except Exception as e:
                # Unexpected error while clicking
                last_exception = e
                logger.debug("Unexpected click exception: %s", e)
                raise
        except StaleElementReferenceException as e:
            # Stale element: caller should re-find element; treat as transient
            last_exception = e
            logger.debug("StaleElementReference on attempt %s: %s", attempt, e)
        except Exception as e:
            last_exception = e
            logger.debug("Error before clicking on attempt %s: %s", attempt, e)

        if attempt < attempts:
            time.sleep(retry_delay)

    if last_exception:
        raise last_exception
    raise RuntimeError("Unable to click provided element")


def click_elements(
    elements: List[AppiumWebElement],
    driver: Optional[AppiumWebDriver] = None,
    index: int = 0,
    **kwargs,
) -> None:
    """
    Helper to click one element from a list of already-found elements.
    - elements: list of AppiumWebElement
    - index: which element to click (default 0)
    - other kwargs forwarded to click_element
    """
    if not elements:
        raise ValueError("elements list is empty")
    if index < 0 or index >= len(elements):
        raise IndexError("index out of range for elements list")
    click_element(elements[index], driver=driver or _get_driver_from_element(elements[index]), **kwargs)
