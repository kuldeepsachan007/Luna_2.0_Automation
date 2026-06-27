import re

from pages.base_page import BasePage
from utility.liberaries.decorators import logger


class HeartRatePage(BasePage):
    """Luna 2.0 Heart Rate detail page (Jetpack Compose).

    Reached from the Health page by tapping the Heart Rate card. Locators come
    from heart_rate_page_locators.py (confirmed from uiautomator dumps).

    Note on the graph: the main HR chart (x: 12 AM..12 AM, y: 60..120) is
    Canvas-drawn, so its axis labels are NOT queryable as elements. We confirm
    the graph SECTION rendered (Today's average + numeric value) and capture a
    screenshot for visual axis verification.
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.name = "Heart Rate Page"
        self.locator = self.get_locators().HEART_RATE_PAGE

    # ── internal: Compose-friendly scroll ───────────────────────────────────
    def _scroll_to(self, locator, max_scrolls=8, direction="down"):
        if self.forms.is_element_displayed(self.driver, locator, timeout=2):
            return True
        size = self.driver.get_window_size()
        w, h = int(size["width"]), int(size["height"])
        area = {"left": int(w * 0.1), "top": int(h * 0.2),
                "width": int(w * 0.8), "height": int(h * 0.6)}
        for _ in range(max_scrolls):
            try:
                self.driver.execute_script("mobile: scrollGesture", {
                    **area, "direction": direction, "percent": 0.9,
                })
            except Exception as e:
                logger.debug("scrollGesture failed: %s", e)
                break
            if self.forms.is_element_displayed(self.driver, locator, timeout=1):
                return True
        return self.forms.is_element_displayed(self.driver, locator, timeout=1)

    # ── Step: HR detail page open on the current date ────────────────────────
    def verify_open_on_current_date(self):
        """The page is the Heart Rate detail page AND it is showing the current
        day (date selector reads "Today"). "Today's average" is the HR-detail
        marker (not present on the Health landing page)."""
        self.waits.wait_for_visible(self.driver, self.locator.TODAYS_AVERAGE, timeout=15)
        assert self.forms.is_element_displayed(self.driver, self.locator.DATE_TODAY, timeout=5), \
            "Heart Rate page is not on the current date ('Today' not shown)"
        logger.info("Heart Rate detail page open on current date (Today)")
        self.capture_screenshot("HR_Detail_Current_Date")

    # ── Step: a heart-rate graph is plotted ──────────────────────────────────
    def verify_hr_graph_plotted(self):
        """Confirm the HR graph section rendered: the 'Today's average' label
        and a numeric average are present. The chart's axis labels
        (12 AM..12 AM, 60..120) are Canvas-drawn and cannot be asserted via
        locators, so a screenshot is captured for visual axis confirmation."""
        self.waits.wait_for_visible(self.driver, self.locator.TODAYS_AVERAGE, timeout=10)
        avg = None
        try:
            avg = self.forms.get_value(self.driver, self.locator.TODAYS_AVG_VALUE, timeout=5)
        except Exception:
            pass
        assert avg is not None and re.search(r"\d", str(avg)), \
            f"Heart Rate graph average value missing/not numeric: {avg!r}"
        logger.info("HR graph rendered; today's average = %s bpm", avg)
        logger.info("NOTE: chart axis labels (12 AM..12 AM, 60..120) are Canvas-drawn; "
                    "see screenshot 'HR_Graph' for visual axis verification.")
        self.capture_screenshot("HR_Graph")

    # ── Step: expand the Sleep HR section ────────────────────────────────────
    def expand_sleep_hr(self):
        self.waits.wait_for_visible(self.driver, self.locator.SLEEP_HR, timeout=10)
        self.mouse.click(self.driver, self.locator.SLEEP_HR)
        logger.info("Tapped 'Sleep HR' to expand")
        self.capture_screenshot("Sleep_HR_Expanded")

    # ── Step: scroll until Sleep HR -> Workout HR area is visible ────────────
    def scroll_to_workout_hr(self):
        """Scroll down until 'Workout HR' is visible. 'Sleep HR' sits above it,
        so when 'Workout HR' is on screen the whole Sleep-HR -> Workout-HR area
        is visible."""
        found = self._scroll_to(self.locator.WORKOUT_HR)
        assert found, "Could not scroll the 'Sleep HR -> Workout HR' area into view"
        logger.info("Scrolled so 'Sleep HR' -> 'Workout HR' area is visible")
        self.capture_screenshot("Sleep_To_Workout_Area")

    # ── Step: RHR / AVG SLEEP HR / TIME TO LOW details are shown ─────────────
    def verify_sleep_hr_details(self):
        """Assert the three Sleep HR detail cards are shown. Values are dynamic
        (change daily), so we assert each label is visible AND its value is a
        non-empty reading — never a fixed number."""
        checks = [
            ("RHR", self.locator.RHR_LABEL, self.locator.RHR_VALUE),
            ("AVG SLEEP HR", self.locator.AVG_SLEEP_HR_LABEL, self.locator.AVG_SLEEP_HR_VALUE),
            ("TIME TO LOW", self.locator.TIME_TO_LOW_LABEL, self.locator.TIME_TO_LOW_VALUE),
        ]
        for name, label_loc, value_loc in checks:
            assert self.forms.is_element_displayed(self.driver, label_loc, timeout=5), \
                f"'{name}' label is not shown"
            value = self.forms.get_value(self.driver, value_loc, timeout=5)
            assert value is not None and str(value).strip() != "", \
                f"'{name}' value is missing"
            logger.info("Sleep HR detail OK: %s = %s", name, value)
        self.capture_screenshot("Sleep_HR_Details")
