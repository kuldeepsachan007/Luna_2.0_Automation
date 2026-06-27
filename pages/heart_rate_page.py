import re
import time

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

    # ── internal: reliable Compose tap ──────────────────────────────────────
    # UiAutomator2's clickGesture on the element triggers Compose click handlers
    # reliably (a plain coordinate 'mobile: tap' was ignored by some controls).
    def _tap(self, locator, timeout=5):
        el = self.mouse.find_element(self.driver, locator, timeout=timeout)
        try:
            self.driver.execute_script("mobile: clickGesture", {"elementId": el.id})
        except Exception as e:
            logger.warning("clickGesture failed (%s); falling back to coordinate tap", e)
            rect = el.rect
            cx = int(rect["x"] + rect["width"] / 2)
            cy = int(rect["y"] + rect["height"] / 2)
            self.mouse.click_coordinates(self.driver, cx, cy)

    def _verify_graph_plotted(self, name, avg_loc, axis_loc):
        """A period graph is 'plotted' when its period-average label and one of
        its X-axis labels are shown. The bars + Y-axis are Canvas-drawn (not
        queryable), so a screenshot is captured too."""
        self.waits.wait_for_visible(self.driver, avg_loc, timeout=10)
        assert self.forms.is_element_displayed(self.driver, axis_loc, timeout=5), \
            f"{name} heart-rate graph X-axis labels not shown"
        logger.info("%s heart-rate graph plotted", name)
        self.capture_screenshot(f"HR_Graph_{name}")

    # ── RHR card -> Resting Heart Rate dialog ────────────────────────────────
    def open_rhr_card(self):
        """Capture the RHR card value (for later comparison), then tap the card
        EXACTLY ONCE to open the Resting Heart Rate dialog.

        Important: tap only once. The dialog takes a moment to load its data, and
        a second tap would land outside the still-opening dialog and dismiss it —
        so we tap once and then wait patiently for the dialog title."""
        self._ensure_visible(self.locator.RHR_LABEL)
        self._rhr_card_value = self.forms.get_value(self.driver, self.locator.RHR_VALUE, timeout=5)
        logger.info("RHR card value (before opening): %s", self._rhr_card_value)
        card = self.mouse.find_element(self.driver, self.locator.RHR_CARD, timeout=5)
        # Click the card element ONCE via UiAutomator2's clickGesture (a proper
        # click that triggers the Compose handler; a plain coordinate 'mobile: tap'
        # did not open this card). Fall back to a coordinate tap if unsupported.
        logger.info("Clicking the RHR card element (clickGesture)")
        try:
            self.driver.execute_script("mobile: clickGesture", {"elementId": card.id})
        except Exception as e:
            logger.warning("clickGesture failed (%s); falling back to coordinate tap", e)
            rect = card.rect
            cx = int(rect["x"] + rect["width"] / 2)
            cy = int(rect["y"] + rect["height"] / 2)
            self.mouse.click_coordinates(self.driver, cx, cy)
        assert self.forms.is_element_displayed(self.driver, self.locator.RHR_DIALOG_TITLE, timeout=15), \
            "Tapped the RHR card but the Resting Heart Rate dialog did not open"
        logger.info("Opened the Resting Heart Rate dialog")
        self.capture_screenshot("RHR_Dialog")

    def verify_rhr_dialog_title(self):
        self.waits.wait_for_visible(self.driver, self.locator.RHR_DIALOG_TITLE, timeout=10)
        logger.info("'Resting Heart Rate' dialog title shown")
        self.capture_screenshot("RHR_Dialog_Title")

    def verify_rhr_dialog_value_matches_card(self):
        """The value shown in the dialog must match the value that was on the
        RHR card. The dialog loads its data after opening, so poll until the
        dialog value renders as a number, then compare the numeric parts
        (values are dynamic)."""
        card_val = getattr(self, "_rhr_card_value", None)
        m = re.search(r"\d+", str(card_val or ""))
        assert m, f"RHR card value was not captured: {card_val!r}"
        card_num = m.group()
        # Wait for the dialog to finish loading its data (the weekly average and
        # chart appear) before reading the value.
        self.waits.wait_for_visible(self.driver, self.locator.WEEKLY_AVERAGE, timeout=15)
        # Primary: read the big current value (the number next to "bpm").
        dlg_num = None
        for _ in range(6):
            v = self.forms.get_value(self.driver, self.locator.RHR_DIALOG_VALUE, timeout=2)
            mm = re.search(r"\d+", str(v or ""))
            if mm and v and "Resting" not in str(v):
                dlg_num = mm.group()
                break
            time.sleep(1)
        # Fallback: the card's value should be shown somewhere in the dialog.
        if dlg_num is None:
            value_text = ("xpath", f'//android.widget.TextView[@text="{card_num}"]')
            assert self.forms.is_element_displayed(self.driver, value_text, timeout=5), \
                f"The dialog does not show the RHR card value {card_num!r}"
            dlg_num = card_num
        assert card_num == dlg_num, \
            f"RHR value mismatch: card={card_num!r} but dialog shows {dlg_num!r}"
        logger.info("RHR value matches: card=%s, dialog=%s", card_num, dlg_num)
        self.capture_screenshot("RHR_Value_Match")

    def verify_week_graph(self):
        # WEEK is selected by default when the dialog opens.
        self._verify_graph_plotted("Week", self.locator.WEEKLY_AVERAGE, self.locator.WEEK_AXIS_SAMPLE)

    def select_month_view(self):
        self._tap(self.locator.TAB_MONTH)
        logger.info("Selected the MONTH view")
        time.sleep(3)  # pause between views so each graph renders / is observable

    def verify_month_graph(self):
        self._verify_graph_plotted("Month", self.locator.MONTHLY_AVERAGE, self.locator.MONTH_AXIS_SAMPLE)

    def select_6m_view(self):
        self._tap(self.locator.TAB_6M)
        logger.info("Selected the 6M view")
        time.sleep(3)  # pause between views so each graph renders / is observable

    def verify_6m_graph(self):
        self._verify_graph_plotted("6M", self.locator.SIX_MONTH_AVERAGE, self.locator.SIXM_AXIS_SAMPLE)

    def close_rhr_dialog(self):
        self._tap(self.locator.DIALOG_CLOSE)
        logger.info("Tapped the dialog Close (X)")
        self.capture_screenshot("RHR_Dialog_Closed")

    def verify_dialog_closed(self):
        assert self.waits.wait_for_invisible(self.driver, self.locator.RHR_DIALOG_TITLE, timeout=8), \
            "The Resting Heart Rate dialog did not close"
        logger.info("Resting Heart Rate dialog is closed")
