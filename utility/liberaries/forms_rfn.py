# python
from typing import Optional, Any
import time
import logging

# Use Appium types for mobile automation
from appium.webdriver.webdriver import WebDriver as AppiumWebDriver
from appium.webdriver.webelement import WebElement as AppiumWebElement
from selenium.common.exceptions import (
    StaleElementReferenceException,
    WebDriverException,
)

logger = logging.getLogger(__name__)


def _get_driver_from_element(element: AppiumWebElement) -> Optional[AppiumWebDriver]:
    # Appium WebElement commonly stores a reference to its parent driver
    return getattr(element, "parent", None) or getattr(element, "_parent", None)


def _mobile_set_value(driver: AppiumWebDriver, element: AppiumWebElement, value: str) -> bool:
    """
    Mobile-aware attempt to set value on an input element.
    Tries element.set_value, then driver mobile: setValue script (best-effort),
    otherwise falls back to element.send_keys after clearing.
    Returns True on success, False on failure.
    """
    try:
        # Preferred: WebElement.set_value (Appium-binding may provide this)
        if hasattr(element, "set_value"):
            try:
                element.set_value(value)
                return True
            except Exception:
                # continue to other fallbacks
                pass

        # Some Appium servers expose a mobile: setValue endpoint. Try using it if available.
        try:
            # element._id or element.id may hold the internal id depending on binding
            elem_id = getattr(element, "id", None) or getattr(element, "_id", None)
            if elem_id is not None:
                # command shape may vary; this is a best-effort attempt and may be ignored on some drivers
                driver.execute_script("mobile: setValue", {"elementId": elem_id, "value": [value]})
                return True
        except Exception:
            pass

        # Fallback: clear and send_keys (works for many native inputs)
        try:
            element.clear()
        except Exception:
            pass
        try:
            element.send_keys(value)
            return True
        except Exception:
            pass
    except Exception as e:
        logger.debug("mobile_set_value failed: %s", e)
    return False


def safe_clear(element: AppiumWebElement) -> None:
    """
    Try element.clear() for mobile inputs, fallback to set_value('') if available.
    """
    try:
        element.clear()
        return
    except Exception as e:
        logger.debug("clear() failed: %s", e)

    drv = _get_driver_from_element(element)
    if drv:
        try:
            if hasattr(element, "set_value"):
                element.set_value("")
                return
            # try mobile set value
            if _mobile_set_value(drv, element, ""):
                return
        except Exception as e:
            logger.debug("mobile clear fallback failed: %s", e)
    # If still failing, ignore and allow subsequent attempts to overwrite


def safe_send_keys(
    element: AppiumWebElement,
    text: str,
    driver: Optional[AppiumWebDriver] = None,
    attempts: int = 3,
    retry_delay: float = 0.2,
) -> None:
    """
    Send keys to an already-found mobile element with retries and mobile-specific fallbacks.
    """
    last_exc: Optional[Exception] = None
    drv = driver or _get_driver_from_element(element)

    for attempt in range(1, attempts + 1):
        try:
            element.send_keys(text)
            return
        except StaleElementReferenceException as e:
            last_exc = e
            logger.debug("StaleElementReference in send_keys attempt %s: %s", attempt, e)
        except WebDriverException as e:
            last_exc = e
            logger.debug("send_keys failed attempt %s: %s", attempt, e)
            # Try mobile set value fallback (append)
            try:
                current = None
                try:
                    current = element.get_attribute("text") or element.get_attribute("value") or ""
                except Exception:
                    current = ""
                if drv and _mobile_set_value(drv, element, (current or "") + text):
                    return
            except Exception:
                pass
        except Exception as e:
            last_exc = e
            logger.debug("Unexpected send_keys error: %s", e)

        if attempt < attempts:
            time.sleep(retry_delay)

    if last_exc:
        raise last_exc
    raise RuntimeError("safe_send_keys failed")


def set_input_value(
    element: AppiumWebElement,
    value: str,
    driver: Optional[AppiumWebDriver] = None,
    attempts: int = 3,
    retry_delay: float = 0.2,
    use_mobile_fallback: bool = True,
) -> None:
    """
    Clear and set the value of a mobile input element reliably.
    """
    last_exc: Optional[Exception] = None
    drv = driver or _get_driver_from_element(element)

    for attempt in range(1, attempts + 1):
        try:
            safe_clear(element)
            element.send_keys(value)
            return
        except StaleElementReferenceException as e:
            last_exc = e
            logger.debug("StaleElementReference in set_input_value attempt %s: %s", attempt, e)
        except WebDriverException as e:
            last_exc = e
            logger.debug("set_input_value send_keys failed attempt %s: %s", attempt, e)
            if use_mobile_fallback and drv and _mobile_set_value(drv, element, value):
                return
        except Exception as e:
            last_exc = e
            logger.debug("Unexpected error in set_input_value: %s", e)

        if attempt < attempts:
            time.sleep(retry_delay)

    if last_exc:
        raise last_exc
    raise RuntimeError("set_input_value failed")


def append_input_value(element: AppiumWebElement, text: str, driver: Optional[AppiumWebDriver] = None) -> None:
    """
    Append text to an input using send_keys or a mobile set_value fallback.
    """
    drv = driver or _get_driver_from_element(element)
    try:
        element.send_keys(text)
        return
    except Exception as e:
        logger.debug("append send_keys failed: %s", e)
    # fallback: try to read current and set new value
    try:
        current = element.get_attribute("text") or element.get_attribute("value") or ""
    except Exception:
        current = ""
    if drv and _mobile_set_value(drv, element, (current or "") + text):
        return
    raise RuntimeError("append_input_value failed")


# The HTML <select> element doesn't directly map to native mobile controls.
# Provide informative errors for these operations so callers know to implement
# platform-specific picker handling instead.
def select_option_by_value(element: AppiumWebElement, value: str) -> None:
    raise NotImplementedError("select_option_by_value is not supported for native mobile elements; implement picker interactions instead")


def select_option_by_visible_text(element: AppiumWebElement, text: str) -> None:
    raise NotImplementedError("select_option_by_visible_text is not supported for native mobile elements; implement picker interactions instead")


def select_option_by_index(element: AppiumWebElement, index: int) -> None:
    raise NotImplementedError("select_option_by_index is not supported for native mobile elements; implement picker interactions instead")


def is_checked(element: AppiumWebElement) -> bool:
    """
    Returns True if checkbox/radio-like control appears checked/selected.
    Checks several common attributes used on mobile platforms.
    """
    try:
        for attr in ("checked", "selected", "value", "checkedValue"):
            try:
                val = element.get_attribute(attr)
            except Exception:
                val = None
            if val is None:
                continue
            if isinstance(val, bool):
                return bool(val)
            s = str(val).lower()
            if s in ("true", "1", "yes", "checked", "selected"):
                return True
        return False
    except Exception as e:
        logger.debug("is_checked check failed: %s", e)
        return False


def _tap_via_touchaction(driver: Optional[AppiumWebDriver], element: Optional[AppiumWebElement] = None, x: Optional[int] = None, y: Optional[int] = None) -> bool:
    if driver is None:
        return False
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
        logger.debug("TouchAction tap failed in _tap_via_touchaction: %s", e)
        return False


def ensure_checked(element: AppiumWebElement, driver: Optional[AppiumWebDriver] = None) -> None:
    """
    Ensure the checkbox/radio-like control is checked. Click/tap if needed.
    """
    if is_checked(element):
        return
    try:
        element.click()
        if is_checked(element):
            return
    except Exception as e:
        logger.debug("click to check failed: %s", e)

    drv = driver or _get_driver_from_element(element)
    # Try touch action tap as fallback
    if _tap_via_touchaction(drv, element=element):
        if is_checked(element):
            return
    raise RuntimeError("Unable to ensure element is checked")


def ensure_unchecked(element: AppiumWebElement, driver: Optional[AppiumWebDriver] = None) -> None:
    """
    Ensure the checkbox/radio-like control is unchecked.
    """
    if not is_checked(element):
        return
    try:
        element.click()
        if not is_checked(element):
            return
    except Exception as e:
        logger.debug("click to uncheck failed: %s", e)

    drv = driver or _get_driver_from_element(element)
    if _tap_via_touchaction(drv, element=element):
        if not is_checked(element):
            return
    raise RuntimeError("Unable to ensure element is unchecked")


def get_value(element: AppiumWebElement) -> Any:
    """
    Return a sensible value or text for a mobile element.
    """
    try:
        for attr in ("text", "value", "content-desc", "name"):
            try:
                val = element.get_attribute(attr)
            except Exception:
                val = None
            if val is not None and val != "":
                return val
        # last resort: use element.text or attribute access
        try:
            return getattr(element, "text", None)
        except Exception:
            return None
    except Exception as e:
        logger.debug("get_value failed: %s", e)
        return None

def is_element_displayed(el) -> bool:
    """
    Check if the mobile element is displayed/visible.
    """
    try:
        return el.is_displayed()
    except Exception as e:
        logger.debug("is_element_displayed check failed: %s", e)
        return False


def submit_form(element: AppiumWebElement) -> None:
    """
    Submitting a form is not a native mobile concept. Try a click on the element
    (for example a submit button). If that doesn't work raise a clear error.
    """
    try:
        element.click()
        return
    except Exception as e:
        logger.debug("element.click() failed in submit_form: %s", e)
    raise NotImplementedError("submit_form is not generally applicable for native mobile apps; perform a tap or platform-specific action instead")

