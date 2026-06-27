import re

from pages.base_page import BasePage
from utility.liberaries.decorators import logger


class HeartRatePage(BasePage):
    """Luna 2.0 Heart Rate detail page (Jetpack Compose).

    Reached from the Health page by tapping the Heart Rate card. Locators come
    from heart_rate_page_locators.py (confirmed from uiautomator dumps).

    Note on the graph: the main HR chart (x: 12 AM..12 AM, y: 60..120) is
    Canvas-drawn, so its axis labels are NOT queryable as elements. We confirm
    the graph card rendered ("Today's average" shown) and capture a screenshot
    for visual axis verification.
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.name = "Heart Rate Page"
        self.locator = self.get_locators().HEART_RATE_PAGE

    # ── internal: Compose-friendly scrolling ─────────────────────────────────
    def _scroll_once(self, direction="down", percent=0.7, top_frac=0.2, height_frac=0.6):
        size = self.driver.get_window_size()
        w, h = int(size["width"]), int(size["height"])
        try:
            self.driver.execute_script("mobile: scrollGesture", {
                "left": int(w * 0.1), "top": int(h * top_frac),
                "width": int(w * 0.8), "height": int(h * height_frac),
                "direction": direction, "percent": percent,
            })
            return True
        except Exception as e:
            logger.debug("scrollGesture failed: %s", e)
            return False

    def _scroll_to(self, locator, max_scrolls=8, direction="down", percent=0.7):
        """Scroll in one direction until the element is visible."""
        if self.forms.is_element_displayed(self.driver, locator, timeout=2):
            return True
        for _ in range(max_scrolls):
            if not self._scroll_once(direction, percent):
                break
            if self.forms.is_element_displayed(self.driver, locator, timeout=1):
                return True
        return self.forms.is_element_displayed(self.driver, locator, timeout=1)

    def _ensure_visible(self, locator, max_scrolls=6):
        """Bring an element on-screen regardless of current scroll position:
        try scrolling up first, then down (used by the verify step which runs
        after we've scrolled down to the Workout HR boundary)."""
        if self.forms.is_element_displayed(self.driver, locator, timeout=2):
            return True
        for direction in ("up", "down"):
            for _ in range(max_scrolls):
                if not self._scroll_once(direction, percent=0.5):
                    break
                if self.forms.is_element_displayed(self.driver, locator, timeout=1):
                    return True
        return self.forms.is_element_displayed(self.driver, locator, timeout=1)

    # ── Step: HR detail page open on the current date ────────────────────────
    def verify_open_on_current_date(self):
        """The page is the Heart Rate detail page AND showing the current day
        (date selector reads "Today"). "Today's average" is the HR-detail marker
        (not present on the Health landing page)."""
        self.waits.wait_for_visible(self.driver, self.locator.TODAYS_AVERAGE, timeout=15)
        assert self.forms.is_element_displayed(self.driver, self.locator.DATE_TODAY, timeout=5), \
            "Heart Rate page is not on the current date ('Today' not shown)"
        logger.info("Heart Rate detail page open on current date (Today)")
        self.capture_screenshot("HR_Detail_Current_Date")

    # ── Step: a heart-rate graph is plotted ──────────────────────────────────
    def verify_hr_graph_plotted(self):
        """The HR graph card rendered when "Today's average" is shown. The chart
        itself (x: 12 AM..12 AM, y: 60..120) is Canvas-drawn, so its axis labels
        cannot be asserted via locators — a screenshot is captured for visual
        axis confirmation."""
        self.waits.wait_for_visible(self.driver, self.locator.TODAYS_AVERAGE, timeout=10)
        logger.info("HR graph card rendered ('Today's average' shown)")
        logger.info("NOTE: chart axis labels (12 AM..12 AM, 60..120) are Canvas-drawn; "
                    "see screenshot 'HR_Graph' for visual axis verification.")
        self.capture_screenshot("HR_Graph")

    # ── Step: expand the Sleep HR section ────────────────────────────────────
    def expand_sleep_hr(self):
        """Tap the Sleep HR row to expand it. element.click() did not toggle the
        Compose clickable, so we tap the row's centre by coordinates (a real tap
        gesture) and confirm expansion via the Collapse chevron, retrying once."""
        self.waits.wait_for_visible(self.driver, self.locator.SLEEP_HR, timeout=10)
        for attempt in range(1, 3):
            row = self.mouse.find_element(self.driver, self.locator.SLEEP_HR_ROW, timeout=5)
            rect = row.rect
            cx = int(rect["x"] + rect["width"] / 2)
            cy = int(rect["y"] + rect["height"] / 2)
            logger.info("Tapping 'Sleep HR' row at (%d, %d) [attempt %d]", cx, cy, attempt)
            self.mouse.click_coordinates(self.driver, cx, cy)
            if self.forms.is_element_displayed(self.driver, self.locator.SLEEP_HR_COLLAPSE, timeout=5):
                logger.info("Expanded the 'Sleep HR' section")
                self.capture_screenshot("Sleep_HR_Expanded")
                return
        raise AssertionError(
            "Tapped 'Sleep HR' but the section did not expand (no Collapse chevron)"
        )

    # ── Step: scroll until Sleep HR -> Workout HR area is visible ────────────
    def scroll_to_workout_hr(self):
        """Bring 'Workout HR' on screen in a single large scroll: a tall scroll
        area (top 10% .. 90% of the screen) at full percent covers the whole
        expanded Sleep HR section in one gesture. (A few retries are kept as a
        safety net; the verify step scrolls the Sleep HR cards back into view
        individually, so overshooting past them is fine.)"""
        found = self.forms.is_element_displayed(self.driver, self.locator.WORKOUT_HR, timeout=2)
        for _ in range(4):
            if found:
                break
            self._scroll_once(direction="down", percent=1.0, top_frac=0.1, height_frac=0.8)
            found = self.forms.is_element_displayed(self.driver, self.locator.WORKOUT_HR, timeout=1)
        assert found, "Could not bring 'Workout HR' into view"
        logger.info("Scrolled so the 'Sleep HR' -> 'Workout HR' area is visible")
        self.capture_screenshot("Sleep_To_Workout_Area")

    # ── Step: RHR / AVG SLEEP HR / TIME TO LOW details are shown ─────────────
    def verify_sleep_hr_details(self):
        """Assert the three Sleep HR detail cards are shown. Each card is scrolled
        into view if needed. Values are dynamic (change daily), so we assert each
        label is present AND its value is a non-empty reading — never a fixed
        number."""
        checks = [
            ("RHR", self.locator.RHR_LABEL, self.locator.RHR_VALUE),
            ("AVG SLEEP HR", self.locator.AVG_SLEEP_HR_LABEL, self.locator.AVG_SLEEP_HR_VALUE),
            ("TIME TO LOW", self.locator.TIME_TO_LOW_LABEL, self.locator.TIME_TO_LOW_VALUE),
        ]
        for name, label_loc, value_loc in checks:
            assert self._ensure_visible(label_loc), \
                f"'{name}' is not shown in the Sleep HR breakdown"
            value = self.forms.get_value(self.driver, value_loc, timeout=5)
            assert value is not None and str(value).strip() != "", \
                f"'{name}' value is missing"
            logger.info("Sleep HR detail OK: %s = %s", name, value)
        self.capture_screenshot("Sleep_HR_Details")
