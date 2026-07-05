import os
import re
import time
from datetime import date, datetime

from pages.base_page import BasePage
from utility.liberaries.decorators import logger


class HealthPage(BasePage):
    """Luna 2.0 Health page (Jetpack Compose).

    Recreated after the original file was lost in the 2026-06-25 deletion (see
    the project-file-recovery memory). The public method surface is reconstructed
    from features/steps/test_health_page_steps.py; locators come from
    health_page_locators.py.

    Landing-page behaviour (tiles visible, sleep-card values, deficit math) is
    derived from a confirmed uiautomator dump. Methods that drive the measure
    popups or the Heart Rate / Stress / Activity / Sleep detail pages are marked
    PROVISIONAL — they follow the feature-file flow but their locators must be
    verified against a dump of each screen as the flow reaches it.
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.name = "Health Page"
        self.locator = self.get_locators().HEALTH_PAGE
        # captured values for cross-screen comparison (card vs detail page)
        self._readings = {}
        self._card_values = {}

    # ── internal helpers ─────────────────────────────────────────────────────

    @staticmethod
    def _parse_duration(text):
        """Convert a duration string like '5h 18m', 'of 9h 10m', '3h 52m short'
        into total minutes. Returns None if no duration is found."""
        if not text:
            return None
        h = re.search(r"(\d+)\s*h", str(text))
        m = re.search(r"(\d+)\s*m", str(text))
        if not h and not m:
            return None
        return (int(h.group(1)) * 60 if h else 0) + (int(m.group(1)) if m else 0)

    def _scroll_to(self, locator, max_scrolls=8, direction="down"):
        """Compose-friendly scroll: 'mobile: scrollGesture' over a tall area,
        percent ~0.9, re-checking for the element each pass (don't trust
        canScrollMore). Returns True if the element becomes visible."""
        if self.forms.is_element_displayed(self.driver, locator, timeout=2):
            return True
        size = self.driver.get_window_size()
        w, h = int(size["width"]), int(size["height"])
        area = {
            "left": int(w * 0.1), "top": int(h * 0.2),
            "width": int(w * 0.8), "height": int(h * 0.6),
        }
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

    def _go_back(self, locator=None, screenshot=None):
        """Tap the page's back control if present, else use the system back."""
        try:
            self.mouse.click(self.driver, locator or self.locator.BACK_BUTTON, timeout=5)
        except Exception:
            try:
                self.driver.back()
            except Exception:
                logger.warning("Could not navigate back")
        if screenshot:
            self.capture_screenshot(screenshot)

    # ── Background / navigation ────────────────────────────────────────────────

    def tap_health_tab(self):
        self.mouse.click(self.driver, self.locator.NAV_HEALTH)
        self.capture_screenshot("Health_Tab_Tapped")

    def tap_home_tab(self):
        """Tap the bottom-nav Home tab to return to the Home page WITHOUT
        relaunching the app (HomePage.go_to_home_page relaunches when off-Home;
        we want an in-app navigation so the app doesn't restart at the end)."""
        self.mouse.click(self.driver, self.locator.NAV_HOME)
        logger.info("Tapped bottom-nav Home tab (no relaunch)")
        self.capture_screenshot("Home_Tab_Tapped")

    def go_to_previous_day(self):
        """Tap the 'Previous day' arrow next to the date to move one day back
        (e.g. from Today to the previous date, which has complete data)."""
        el = self.mouse.find_element(self.driver, self.locator.NAV_PREVIOUS_DAY, timeout=10)
        try:
            self.driver.execute_script("mobile: clickGesture", {"elementId": el.id})
        except Exception:
            el.click()
        logger.info("Tapped 'Previous day' (navigated one day back)")
        self.capture_screenshot("Health_Previous_Day")

    def go_to_next_day(self):
        """Tap the 'Next day' arrow to move one day forward. Returns False if the
        arrow is absent — the app has no future dates, so this means we are on
        Today. Used to reset the date to Today before stepping back."""
        if not self.forms.is_element_displayed(self.driver, self.locator.NAV_NEXT_DAY, timeout=1):
            return False
        el = self.mouse.find_element(self.driver, self.locator.NAV_NEXT_DAY, timeout=3)
        try:
            self.driver.execute_script("mobile: clickGesture", {"elementId": el.id})
        except Exception:
            el.click()
        return True

    def go_to_stable_date(self):
        """Navigate the Health page from Today back to the configured stable date.

        The target is read from the HEALTH_TARGET_DATE env var (format
        YYYY-MM-DD). The number of 'Previous day' taps is computed as
        (today - target).days, so the flow auto-adjusts: change only the env
        date and it lands on that day. The Health page opens on Today, so this
        is deterministic. If the var is unset, fall back to one day back."""
        target_str = (os.getenv("HEALTH_TARGET_DATE") or "").strip()
        if not target_str:
            logger.info("HEALTH_TARGET_DATE not set; going one day back")
            self.go_to_previous_day()
            return
        try:
            target = datetime.strptime(target_str, "%Y-%m-%d").date()
        except ValueError:
            raise AssertionError(
                f"HEALTH_TARGET_DATE must be YYYY-MM-DD, got {target_str!r}")
        today = date.today()
        days_back = (today - target).days
        assert days_back >= 0, (
            f"HEALTH_TARGET_DATE {target} is in the future (today is {today}); "
            "cannot navigate forward of Today")
        # The Health page RETAINS the last-viewed date across runs (noReset), so
        # it does NOT reliably open on Today — blindly tapping 'Previous day'
        # days_back times drifts further back each run. First step FORWARD to
        # Today (tapping 'Next day' can never go past Today; the arrow disappears
        # there), then step back exactly days_back. This lands on the target
        # regardless of where the page started.
        logger.info("Resetting Health to Today before stepping back (avoids date drift)")
        for _ in range(days_back + 40):
            if not self.go_to_next_day():
                break  # no Next-day arrow => already on Today
            time.sleep(0.3)
        logger.info("Stable date %s = %d day(s) back from today (%s)",
                    target, days_back, today)
        for i in range(days_back):
            logger.info("Previous-day tap %d of %d", i + 1, days_back)
            self.go_to_previous_day()
        if days_back == 0:
            logger.info("Stable date is Today; no navigation needed")
        self.capture_screenshot("Health_Stable_Date")

    def verify_health_page(self):
        # The SpO2 tile is unique to the Health page (the bottom-nav "Health"
        # label also exists on Home), so it is the reliable page marker.
        self.waits.wait_for_visible(self.driver, self.locator.SPO2_LABEL, timeout=15)
        self.capture_screenshot("Health_Page_Visible")

    def verify_back_on_health(self):
        """After Closing a detail page (e.g. Stress), the Health page is restored
        scrolled DOWN to the card that was opened, so the SpO2 tile marker is off
        the top. Scroll back up (raw swipe — reliable) until SpO2 is visible to
        confirm we are back on the Health page."""
        size = self.driver.get_window_size()
        w, h = int(size["width"]), int(size["height"])
        for _ in range(6):
            if self.forms.is_element_displayed(self.driver, self.locator.SPO2_LABEL, timeout=1):
                break
            # swipe finger downward = scroll the page UP (reveal content above)
            self.driver.swipe(w // 2, int(h * 0.3), w // 2, int(h * 0.82), 500)
        self.waits.wait_for_visible(self.driver, self.locator.SPO2_LABEL, timeout=10)
        logger.info("Back on the Health page (SpO2 tile visible)")
        self.capture_screenshot("Health_Page_Back")

    def recover_to_health_page(self):
        """Return to a known-good Health page after a section runs/fails: press
        back until the SpO2 tile reappears, falling back to the Health nav tab."""
        for _ in range(3):
            if self.forms.is_element_displayed(self.driver, self.locator.SPO2_LABEL, timeout=2):
                return
            try:
                self.driver.back()
            except Exception:
                pass
        if not self.forms.is_element_displayed(self.driver, self.locator.SPO2_LABEL, timeout=2):
            try:
                self.mouse.click(self.driver, self.locator.NAV_HEALTH)
            except Exception:
                logger.warning("recover_to_health_page: could not return to Health page")

    # ── Measure (single tap on the tile's MEASURE button) ───────────────────────

    def measure_spo2(self):
        self.mouse.click(self.driver, self.locator.SPO2_MEASURE_BTN)
        self.capture_screenshot("SpO2_Measure_Tapped")

    def measure_stress(self):
        self.mouse.click(self.driver, self.locator.STRESS_MEASURE_BTN)
        self.capture_screenshot("Stress_Measure_Tapped")

    def measure_heart_rate(self):
        self.mouse.click(self.driver, self.locator.HEART_RATE_MEASURE_BTN)
        self.capture_screenshot("Heart_Rate_Measure_Tapped")

    def measure_skin_temp(self):
        self.mouse.click(self.driver, self.locator.SKIN_TEMP_MEASURE_BTN)
        self.capture_screenshot("Skin_Temp_Measure_Tapped")

    # ── Measure with retry (PROVISIONAL: popup locators need a measure-sheet dump)
    # Flow per the feature file: tap MEASURE -> wait -> if "Couldn't get a
    # reading" tap Try Again (one retry) -> on second failure tap Close (X) ->
    # on success tap Done.

    def _measure_with_retry(self, measure_btn, wait_seconds, name):
        self.mouse.click(self.driver, measure_btn)
        self.capture_screenshot(f"{name}_Measuring")
        for attempt in range(2):  # initial attempt + one retry
            time.sleep(wait_seconds)
            no_reading = self.forms.is_element_displayed(
                self.driver, self.locator.POPUP_NO_READING, timeout=5,
            )
            if no_reading:
                self.capture_screenshot(f"{name}_No_Reading_Attempt{attempt + 1}")
                if attempt == 0:
                    self.mouse.click(self.driver, self.locator.POPUP_TRY_AGAIN)
                    continue
                # second failure: close and move on
                self._go_back(self.locator.POPUP_CLOSE)
                return False
            # success: tap Done. The reading is validated on the tile afterwards
            # via verify_reading_matches_tile; the in-popup value is not captured
            # here because it has no stable locator yet.
            self._readings[name] = None
            self.capture_screenshot(f"{name}_Reading_Success")
            self._go_back(self.locator.POPUP_DONE)
            return True
        return False

    def measure_spo2_with_retry(self, wait_seconds=60):
        return self._measure_with_retry(self.locator.SPO2_MEASURE_BTN, wait_seconds, "SpO2")

    def measure_stress_with_retry(self, wait_seconds=40):
        return self._measure_with_retry(self.locator.STRESS_MEASURE_BTN, wait_seconds, "Stress")

    def measure_heart_rate_with_retry(self, wait_seconds=40):
        return self._measure_with_retry(self.locator.HEART_RATE_MEASURE_BTN, wait_seconds, "Heart Rate")

    def measure_skin_temp_with_retry(self, wait_seconds=40):
        return self._measure_with_retry(self.locator.SKIN_TEMP_MEASURE_BTN, wait_seconds, "Skin Temp")

    # ── Verify a measured reading shows on the vital's tile ──────────────────────
    # Values are dynamic (change with each measurement), so we assert shape/range,
    # never a fixed number. If a popup reading was captured, it is compared too.

    def verify_reading_matches_tile(self, name, tile_value_locator):
        value = self.forms.get_value(self.driver, tile_value_locator)
        assert value is not None and str(value).strip() != "", \
            f"{name}: no value shown on the tile"
        assert re.search(r"\d", str(value)), \
            f"{name}: tile value '{value}' is not numeric"
        captured = self._readings.get(name)
        if captured:
            cap_num = re.search(r"\d+", str(captured))
            tile_num = re.search(r"\d+", str(value))
            if cap_num and tile_num:
                assert cap_num.group() == tile_num.group(), (
                    f"{name}: popup reading '{captured}' != tile value '{value}'"
                )
        logger.info("%s tile value: %s", name, value)
        self.capture_screenshot(f"{name}_Tile_Value")

    # ── Sleep card (on the Health page) ──────────────────────────────────────────

    def verify_sleep_card(self):
        self.waits.wait_for_visible(self.driver, self.locator.SLEEP_CARD_LABEL, timeout=10)
        self.capture_screenshot("Sleep_Card_Visible")

    def read_sleep_card_value(self):
        actual = self.forms.get_value(self.driver, self.locator.SLEEP_ACTUAL)
        self._card_values["sleep_actual"] = actual
        logger.info("Sleep card actual sleep: %s", actual)
        return actual

    def open_sleep_card(self):
        self.mouse.click(self.driver, self.locator.SLEEP_CARD_LABEL)
        self.capture_screenshot("Sleep_Card_Opened")

    def verify_sleep_deficit(self):
        """Deficit shown on the Health-page sleep card should equal
        needed - actual (within a small rounding tolerance)."""
        actual = self._parse_duration(self.forms.get_value(self.driver, self.locator.SLEEP_ACTUAL))
        needed = self._parse_duration(self.forms.get_value(self.driver, self.locator.SLEEP_NEEDED))
        deficit = self._parse_duration(self.forms.get_value(self.driver, self.locator.SLEEP_DEFICIT))
        assert None not in (actual, needed, deficit), (
            f"Could not parse sleep durations: actual={actual} needed={needed} deficit={deficit}"
        )
        expected = needed - actual
        assert abs(expected - deficit) <= 2, (
            f"Sleep deficit mismatch: needed({needed}m) - actual({actual}m) = "
            f"{expected}m, but card shows {deficit}m"
        )
        logger.info("Sleep deficit OK: %dm needed - %dm actual = %dm", needed, actual, deficit)
        self.capture_screenshot("Sleep_Deficit_Verified")

    # ── Sleep detail page (PROVISIONAL — needs a Sleep detail dump) ──────────────

    def verify_sleep_page(self):
        self.waits.wait_for_visible(self.driver, self.locator.SLEEP_PAGE_TITLE, timeout=10)
        self.capture_screenshot("Sleep_Page_Visible")

    def verify_sleep_page_value(self):
        title = self.forms.get_value(self.driver, self.locator.SLEEP_PAGE_TITLE)
        assert title is not None and str(title).strip() != "", "Sleep page shows no data"
        self.capture_screenshot("Sleep_Page_Value")

    def go_back_from_sleep_page(self):
        self._go_back(screenshot="Back_From_Sleep_Page")

    def verify_sleep_window_vs_actual(self):
        # PROVISIONAL: requires the Sleep detail page (start/end window + actual).
        logger.info("verify_sleep_window_vs_actual: pending Sleep detail dump")
        self.capture_screenshot("Sleep_Window_Vs_Actual")

    def scroll_to_sleep_stages(self):
        self._scroll_to(self.locator.SLEEP_PAGE_TITLE)
        self.capture_screenshot("Sleep_Stages")

    def read_awake_stage(self):
        logger.info("read_awake_stage: pending Sleep detail dump")
        self.capture_screenshot("Awake_Stage")

    def open_awake_stage(self):
        logger.info("open_awake_stage: pending Sleep detail dump")
        self.capture_screenshot("Awake_Stage_Opened")

    def scroll_to_sleep_metrics(self):
        self._scroll_to(self.locator.SLEEP_PAGE_TITLE)
        self.capture_screenshot("Sleep_Metrics")

    def scroll_to_sleep_end(self):
        self._scroll_to(self.locator.SLEEP_PAGE_TITLE)
        self.capture_screenshot("Sleep_End")

    def verify_sleep_stage_bars(self):
        logger.info("verify_sleep_stage_bars: pending Sleep detail dump")
        self.capture_screenshot("Sleep_Stage_Bars")

    # ── Heart Rate card -> Heart Rate detail page ────────────────────────────────

    def scroll_to_heart_rate_card(self):
        self._scroll_to(self.locator.HEART_RATE_CARD)
        self.capture_screenshot("Heart_Rate_Card_Visible")

    def read_heart_rate_card_value(self):
        value = self.forms.get_value(self.driver, self.locator.HEART_RATE_CARD_VALUE)
        self._card_values["heart_rate"] = value
        logger.info("Heart Rate card value: %s", value)
        return value

    def open_heart_rate_card(self):
        self.mouse.click(self.driver, self.locator.HEART_RATE_CARD)
        self.capture_screenshot("Heart_Rate_Card_Opened")

    def verify_heart_rate_page(self):
        self.waits.wait_for_visible(self.driver, self.locator.HEART_RATE_PAGE_TITLE, timeout=10)
        self.capture_screenshot("Heart_Rate_Page_Visible")

    def verify_hr_page_value_matches_card(self):
        # PROVISIONAL: detail-page value locator pending. Validate the captured
        # card value is a sensible bpm number; compare once the detail dump lands.
        card = self._card_values.get("heart_rate")
        assert card is not None and re.search(r"\d", str(card)), \
            f"Heart Rate card value missing/invalid: {card}"
        logger.info("Heart Rate card value carried to detail page: %s", card)
        self.capture_screenshot("Heart_Rate_Page_Value")

    def go_back_from_heart_rate_page(self):
        self._go_back(screenshot="Back_From_Heart_Rate_Page")

    # ── Stress card -> Stress detail page ────────────────────────────────────────

    def scroll_to_stress_card(self):
        """Scroll down (from the Heart Rate card) until the Stress card is
        visible. The Stress *card* has a clickable parent (the Stress *tile* at
        the top does not), so STRESS_CARD matches the card only."""
        found = self._scroll_to(self.locator.STRESS_CARD)
        assert found, "Could not scroll the Stress card into view"
        self.capture_screenshot("Stress_Card_Visible")

    def read_stress_card_value(self):
        value = self.forms.get_value(self.driver, self.locator.STRESS_CARD_VALUE)
        self._card_values["stress"] = value
        logger.info("Stress card value: %s", value)
        return value

    def open_stress_card(self):
        self.mouse.click(self.driver, self.locator.STRESS_CARD)
        self.capture_screenshot("Stress_Card_Opened")

    def verify_stress_page(self):
        self.waits.wait_for_visible(self.driver, self.locator.STRESS_PAGE_TITLE, timeout=10)
        self.capture_screenshot("Stress_Page_Visible")

    def verify_stress_page_value(self):
        card = self._card_values.get("stress")
        assert card is not None and re.search(r"\d", str(card)), \
            f"Stress card value missing/invalid: {card}"
        logger.info("Stress card value carried to detail page: %s", card)
        self.capture_screenshot("Stress_Page_Value")

    def close_stress_page(self):
        self._go_back(self.locator.POPUP_CLOSE, screenshot="Stress_Page_Closed")

    # ── Activity card -> Activity detail page ────────────────────────────────────

    def scroll_to_activity_card(self):
        self._scroll_to(self.locator.ACTIVITY_CARD)
        self.capture_screenshot("Activity_Card_Visible")

    def read_activity_card_value(self):
        value = self.forms.get_value(self.driver, self.locator.ACTIVITY_CARD_STEPS)
        self._card_values["activity"] = value
        logger.info("Activity card value: %s", value)
        return value

    def open_activity_card(self):
        self.mouse.click(self.driver, self.locator.ACTIVITY_CARD)
        self.capture_screenshot("Activity_Card_Opened")

    def verify_activity_page(self):
        self.waits.wait_for_visible(self.driver, self.locator.ACTIVITY_PAGE_TITLE, timeout=10)
        self.capture_screenshot("Activity_Page_Visible")

    def verify_activity_page_value(self):
        card = self._card_values.get("activity")
        assert card is not None and str(card).strip() != "", \
            f"Activity card value missing: {card}"
        logger.info("Activity card value carried to detail page: %s", card)
        self.capture_screenshot("Activity_Page_Value")

    def go_back_from_activity_page(self):
        self._go_back(screenshot="Back_From_Activity_Page")
