# python
from typing import Optional, Tuple
import logging
import time

from appium.webdriver.webdriver import WebDriver as AppiumWebDriver
from appium.webdriver.webelement import WebElement as AppiumWebElement

logger = logging.getLogger(__name__)


def _get_window_size(driver: AppiumWebDriver) -> Tuple[int, int]:
    sz = driver.get_window_size()
    return int(sz.get("width", 0)), int(sz.get("height", 0))


def tap(driver: AppiumWebDriver, x: Optional[int] = None, y: Optional[int] = None, element: Optional[AppiumWebElement] = None, duration_ms: Optional[int] = None) -> bool:
    """
    Tap on an element or at absolute coordinates.
    Tries modern 'mobile: tap' then TouchAction fallback.
    """
    try:
        if element is not None:
            try:
                element.click()
                return True
            except Exception:
                pass
        if x is not None and y is not None:
            # try modern script
            try:
                driver.execute_script("mobile: tap", {"x": x, "y": y})
                return True
            except Exception:
                pass
        # TouchAction fallback
        try:
            from appium.webdriver.common.touch_action import TouchAction  # type: ignore
            ta = TouchAction(driver)
            if element is not None:
                if duration_ms:
                    ta.long_press(element, duration=duration_ms).release().perform()
                else:
                    ta.tap(element).perform()
            else:
                if x is None or y is None:
                    return False
                if duration_ms:
                    ta.long_press(None, x, y, duration=duration_ms).release().perform()
                else:
                    ta.tap(None, x, y).perform()
            return True
        except Exception as e:
            logger.debug("TouchAction tap failed: %s", e)
    except Exception as e:
        logger.debug("tap failed: %s", e)
    return False


def double_tap(driver: AppiumWebDriver, element: Optional[AppiumWebElement] = None, x: Optional[int] = None, y: Optional[int] = None, interval_ms: int = 100) -> bool:
    """
    Perform a double tap by sending two quick taps.
    """
    try:
        if element is not None:
            if tap(driver, element=element):
                time.sleep(interval_ms / 1000.0)
                return tap(driver, element=element)
            return False
        if x is not None and y is not None:
            if tap(driver, x=x, y=y):
                time.sleep(interval_ms / 1000.0)
                return tap(driver, x=x, y=y)
            return False
    except Exception as e:
        logger.debug("double_tap failed: %s", e)
    return False


def long_press(driver: AppiumWebDriver, element: Optional[AppiumWebElement] = None, x: Optional[int] = None, y: Optional[int] = None, duration_ms: int = 1000) -> bool:
    """
    Long press an element or coordinates for duration_ms milliseconds.
    """
    try:
        from appium.webdriver.common.touch_action import TouchAction  # type: ignore
        ta = TouchAction(driver)
        if element is not None:
            ta.long_press(element, duration=duration_ms).release().perform()
            return True
        if x is not None and y is not None:
            ta.long_press(None, x, y, duration=duration_ms).release().perform()
            return True
    except Exception as e:
        logger.debug("long_press failed: %s", e)
    return False


def swipe(driver: AppiumWebDriver, start_x: int, start_y: int, end_x: int, end_y: int, duration_ms: int = 800) -> bool:
    """
    Swipe from start to end. Uses TouchAction and accounts for relative offsets.
    """
    try:
        from appium.webdriver.common.touch_action import TouchAction  # type: ignore
        dx = end_x - start_x
        dy = end_y - start_y
        ta = TouchAction(driver)
        # press at absolute start, wait, move by offset, release
        ta.press(x=start_x, y=start_y).wait(ms=duration_ms).move_to(x=dx, y=dy).release().perform()
        return True
    except Exception as e:
        logger.debug("swipe TouchAction failed: %s", e)
        # Try fallback to mobile: swipe if available
    try:
        try:
            driver.execute_script("mobile: swipe", {"startX": start_x, "startY": start_y, "endX": end_x, "endY": end_y, "duration": duration_ms})
            return True
        except Exception as e:
            logger.debug("mobile: swipe failed: %s", e)
    except Exception:
        pass
    return False


def swipe_in_direction(driver: AppiumWebDriver, direction: str = "up", percent: float = 0.5, duration_ms: int = 500) -> bool:
    """
    Swipe in a cardinal direction based on screen size.
    direction: 'up'|'down'|'left'|'right'
    percent: fraction of screen to move (0..1)
    """
    w, h = _get_window_size(driver)
    cx = w // 2
    cy = h // 2
    if direction.lower() == "up":
        start_x, start_y = cx, int(cy + (h * 0.25))
        end_x, end_y = cx, int(cy - h * percent)
    elif direction.lower() == "down":
        start_x, start_y = cx, int(cy - (h * 0.25))
        end_x, end_y = cx, int(cy + h * percent)
    elif direction.lower() == "left":
        start_x, start_y = int(cx + (w * 0.25)), cy
        end_x, end_y = int(cx - w * percent), cy
    elif direction.lower() == "right":
        start_x, start_y = int(cx - (w * 0.25)), cy
        end_x, end_y = int(cx + w * percent), cy
    else:
        raise ValueError("Unknown direction: %s" % direction)
    return swipe(driver, start_x, start_y, end_x, end_y, duration_ms=duration_ms)


def swipe_until_element_visible(driver: AppiumWebDriver, locator, max_swipes: int = 5, direction: str = "up", percent: float = 0.5, timeout_between: float = 0.5):
    """
    Repeatedly swipe in `direction` until `locator` is found or max_swipes exhausted.
    `locator` should be compatible with the project's locator helpers (e.g., Locator or tuple).
    Returns the found element or raises the last exception.
    """
    from utility.liberaries.mouse import find_element

    last_exc = None
    for i in range(max_swipes):
        try:
            el = find_element(driver, locator, timeout=1)
            return el
        except Exception as e:
            last_exc = e
            swipe_in_direction(driver, direction=direction, percent=percent)
            time.sleep(timeout_between)
    raise last_exc


def drag_and_drop(driver: AppiumWebDriver, source: AppiumWebElement, target: AppiumWebElement, duration_ms: int = 800) -> bool:
    """
    Drag from source element to target element.
    """
    try:
        from appium.webdriver.common.touch_action import TouchAction  # type: ignore
        ta = TouchAction(driver)
        ta.long_press(source, duration=200).move_to(target).wait(ms=duration_ms).release().perform()
        return True
    except Exception as e:
        logger.debug("drag_and_drop TouchAction failed: %s", e)
    # fallback: try W3C actions or coordinate drag
    try:
        src_rect = source.rect
        tgt_rect = target.rect
        sx = int(src_rect.get('x', 0) + src_rect.get('width', 0) / 2)
        sy = int(src_rect.get('y', 0) + src_rect.get('height', 0) / 2)
        tx = int(tgt_rect.get('x', 0) + tgt_rect.get('width', 0) / 2)
        ty = int(tgt_rect.get('y', 0) + tgt_rect.get('height', 0) / 2)
        return swipe(driver, sx, sy, tx, ty, duration_ms=duration_ms)
    except Exception as e:
        logger.debug("drag_and_drop coordinate fallback failed: %s", e)
    return False


def pinch(driver: AppiumWebDriver, element: Optional[AppiumWebElement] = None) -> bool:
    """
    Pinch (zoom out) gesture on an element if supported.
    Tries driver.pinch(element) or mobile: pinch, otherwise NotImplementedError.
    """
    try:
        # Some clients expose pinch directly
        if element is not None and hasattr(driver, 'pinch'):
            try:
                driver.pinch(element)
                return True
            except Exception:
                pass
        # Try Appium mobile command
        if element is not None:
            elem_id = getattr(element, 'id', None) or getattr(element, '_id', None)
            if elem_id is not None:
                try:
                    driver.execute_script('mobile: pinch', {'element': elem_id})
                    return True
                except Exception:
                    pass
    except Exception as e:
        logger.debug('pinch failed: %s', e)
    raise NotImplementedError('pinch not implemented for this driver/platform')


def zoom(driver: AppiumWebDriver, element: Optional[AppiumWebElement] = None) -> bool:
    """
    Zoom (pinch-out) gesture on an element if supported.
    Tries driver.zoom(element) or mobile: zoom, otherwise NotImplementedError.
    """
    try:
        if element is not None and hasattr(driver, 'zoom'):
            try:
                driver.zoom(element)
                return True
            except Exception:
                pass
        if element is not None:
            elem_id = getattr(element, 'id', None) or getattr(element, '_id', None)
            if elem_id is not None:
                try:
                    driver.execute_script('mobile: zoom', {'element': elem_id})
                    return True
                except Exception:
                    pass
    except Exception as e:
        logger.debug('zoom failed: %s', e)
    raise NotImplementedError('zoom not implemented for this driver/platform')


def scroll_to_element(driver: AppiumWebDriver, locator, max_swipes: int = 5, direction: str = 'up') -> Optional[AppiumWebElement]:
    """
    Scroll until the element is visible using swipe_until_element_visible.
    Returns the found element or None.
    """
    try:
        el = swipe_until_element_visible(driver, locator, max_swipes=max_swipes, direction=direction)
        return el
    except Exception as e:
        logger.debug('scroll_to_element failed: %s', e)
        return None


__all__ = [
    'tap',
    'double_tap',
    'long_press',
    'swipe',
    'swipe_in_direction',
    'swipe_until_element_visible',
    'drag_and_drop',
    'pinch',
    'zoom',
    'scroll_to_element',
]
