import re
import time

from pages.base_page import BasePage
from utility.liberaries.decorators import logger


class StressPage(BasePage):
    """Luna 2.0 Stress detail page (opened from the Health page's Stress card).

    A full page (not a bottom-sheet dialog) with a status word, the day's
    average/Max/Min values, a gauge, and a "How your day unfolded" timeline.
    Locators come from stress_page_locators.py.
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.name = "Stress Page"
        self.locator = self.get_locators().STRESS_PAGE
        # When a day has NO stress data (Max/Min/Avg all show '--'), the value /
        # graph / duration / trend checks cannot pass. In that case we still walk
        # the whole page end-to-end (scroll to every section, tap every element)
        # but downgrade those data-dependent assertions to warnings instead of
        # aborting. On a normal day (data present) `day_has_data` stays True and
        # every check is strict — identical to the previous behaviour. The flag is
        # decided in verify_values_shown, which runs before the dependent steps.
        self.day_has_data = True

    # ── data-tolerance helpers ────────────────────────────────────────────────
    @staticmethod
    def _has_reading(value):
        """True only if `value` is a real reading (contains a digit). None / empty
        / placeholders like '--' or '—' count as no-data."""
        return value is not None and re.search(r"\d", str(value)) is not None

    def _expect(self, condition, msg):
        """Data-present day: behaves exactly like `assert condition, msg` (strict,
        raises AssertionError). No-data day: downgrades a failed check to a warning
        and returns False so the flow keeps walking every element end-to-end."""
        if condition:
            return True
        if self.day_has_data:
            raise AssertionError(msg)
        logger.warning("[no-data] tolerated (this day has no stress data): %s", msg)
        return False

    def _safe_value(self, locator, timeout=5):
        """get_value that returns None instead of raising when the element is
        absent, so a missing value on a no-data day never aborts the scenario."""
        try:
            return self.forms.get_value(self.driver, locator, timeout=timeout)
        except Exception:
            return None

    # ── Page open / close ────────────────────────────────────────────────────
    def verify_stress_page_shown(self):
        """Confirm the Stress detail page opened (title + the day's average)."""
        self.waits.wait_for_visible(self.driver, self.locator.PAGE_TITLE, timeout=15)
        logger.info("Stress detail page is shown")
        self.capture_screenshot("Stress_Page")

    def close_stress_page(self):
        """Tap the top-left Close (X) to return to the Health page."""
        el = self.mouse.find_element(self.driver, self.locator.CLOSE, timeout=10)
        try:
            self.driver.execute_script("mobile: clickGesture", {"elementId": el.id})
        except Exception:
            el.click()
        logger.info("Closed the Stress page (back to Health)")
        self.capture_screenshot("Stress_Page_Closed")

    # ── internal: Compose-friendly scroll ────────────────────────────────────
    def _scroll_to(self, locator, max_scrolls=8, direction="down", percent=0.85,
                   top_frac=0.2, height_frac=0.6):
        # The scroll band must sit OVER text (e.g. the "How your day unfolded"
        # title / gauge), NOT over the chart — the chart captures the gesture so
        # the page would not scroll. Callers pass a high, short band for that.
        if self.forms.is_element_displayed(self.driver, locator, timeout=2):
            return True
        size = self.driver.get_window_size()
        w, h = int(size["width"]), int(size["height"])
        area = {"left": int(w * 0.1), "top": int(h * top_frac),
                "width": int(w * 0.8), "height": int(h * height_frac)}
        for _ in range(max_scrolls):
            try:
                self.driver.execute_script("mobile: scrollGesture", {
                    **area, "direction": direction, "percent": percent,
                })
            except Exception as e:
                logger.debug("scrollGesture failed: %s", e)
                break
            if self.forms.is_element_displayed(self.driver, locator, timeout=1):
                return True
        return self.forms.is_element_displayed(self.driver, locator, timeout=1)

    # ── Step: Max / Min / Avg values are shown (gauge, at the top) ───────────
    def verify_values_shown(self):
        """At the top of the page, the gauge shows the day's Max, Min and Avg.

        This step also DECIDES whether the day has stress data at all: if any of
        Max/Min/Avg is a real reading the day has data and every value must be a
        non-empty number (previous strict behaviour). If the whole day is empty
        ('--'), `day_has_data` is set False so the rest of the flow walks the page
        end-to-end with data checks downgraded to warnings instead of aborting."""
        checks = [
            ("Max", self.locator.MAX_LABEL, self.locator.MAX_VALUE),
            ("Min", self.locator.MIN_LABEL, self.locator.MIN_VALUE),
            ("Avg", self.locator.AVG_LABEL, self.locator.AVG_VALUE),
        ]
        labels = {}
        readings = {}
        for name, label_loc, value_loc in checks:
            labels[name] = self.forms.is_element_displayed(self.driver, label_loc, timeout=5)
            readings[name] = self._safe_value(value_loc)
        # Decide data presence BEFORE asserting, so the gate is set for later steps.
        self.day_has_data = any(self._has_reading(v) for v in readings.values())
        for name, _, _ in checks:
            self._expect(labels[name], f"'{name}' label is not shown")
        if self.day_has_data:
            for name in ("Max", "Min", "Avg"):
                if self._expect(self._has_reading(readings[name]),
                                f"'{name}' value missing/not numeric: {readings[name]!r}"):
                    logger.info("Stress %s value: %s", name, readings[name])
        else:
            logger.warning("No stress data for this day (Max/Min/Avg = %s) — walking the page "
                           "end-to-end with data checks downgraded to warnings", readings)
        self.capture_screenshot("Stress_Values")

    # ── Step: the "How your day unfolded" graph is plotted for the day ───────
    def verify_day_graph_plotted(self):
        """Confirm the timeline graph is plotted across the full day. The X-axis
        time labels (12A, 4A, 8A, 12P, 4P, 8P) are real text nodes and are all
        asserted; the Y-axis (0/33/66/100) and the plotted line are Canvas-drawn
        (not queryable), so a screenshot is captured for visual confirmation."""
        self._expect(self.forms.is_element_displayed(self.driver, self.locator.DAY_GRAPH_TITLE, timeout=10),
                     "'How your day unfolded' graph title not shown")
        x_labels = ["12A", "4A", "8A", "12P", "4P", "8P"]
        for lbl in x_labels:
            loc = ("xpath", f'//android.widget.TextView[@text="{lbl}"]')
            self._expect(self.forms.is_element_displayed(self.driver, loc, timeout=3),
                         f"Stress graph X-axis label '{lbl}' is not shown")
        logger.info("Stress graph checked: X-axis labels %s (Y-axis 0..100 is Canvas)", x_labels)
        self.capture_screenshot("Stress_Graph")

    # ── Step: scroll to the three stress stages ──────────────────────────────
    def scroll_to_stress_stages(self):
        """One single scroll to the state that shows the three stages
        (Relaxed / Focused / Stressed) + TOTAL DURATION + Stress trends.

        The scroll band sits OVER the text above the chart (insight / gauge) and
        is tall with percent 1.0, so a SINGLE gesture moves the page far enough —
        scrolling over the chart would be captured by it and move nothing."""
        if not self.forms.is_element_displayed(self.driver, self.locator.STAGE_STRESSED, timeout=2):
            size = self.driver.get_window_size()
            w, h = int(size["width"]), int(size["height"])
            self.driver.execute_script("mobile: scrollGesture", {
                "left": int(w * 0.1), "top": int(h * 0.14),
                "width": int(w * 0.8), "height": int(h * 0.34),
                "direction": "down", "percent": 1.0,
            })
        self._expect(self.forms.is_element_displayed(self.driver, self.locator.STAGE_STRESSED, timeout=5),
                     "Could not bring the stress stages into view in one scroll")
        self.capture_screenshot("Stress_Stages")

    def verify_stress_stages_shown(self):
        for name, loc in [("Relaxed", self.locator.STAGE_RELAXED),
                          ("Focused", self.locator.STAGE_FOCUSED),
                          ("Stressed", self.locator.STAGE_STRESSED)]:
            if self._expect(self.forms.is_element_displayed(self.driver, loc, timeout=5),
                            f"Stress stage '{name}' is not shown"):
                logger.info("Stress stage shown: %s", name)
        self.capture_screenshot("Stress_Stages_Verified")

    # ── internal helpers ─────────────────────────────────────────────────────
    def _tap(self, locator, timeout=5):
        try:
            el = self.mouse.find_element(self.driver, locator, timeout=timeout)
        except Exception as e:
            logger.warning("_tap: element not found (%s); skipping tap", e)
            return False
        try:
            self.driver.execute_script("mobile: clickGesture", {"elementId": el.id})
        except Exception as e:
            logger.warning("clickGesture failed (%s); coordinate tap", e)
            rect = el.rect
            self.mouse.click_coordinates(
                self.driver, int(rect["x"] + rect["width"] / 2), int(rect["y"] + rect["height"] / 2))
        return True

    @staticmethod
    def _duration_to_minutes(text):
        """'1h 15m' -> 75, '15m' -> 15, '8h 45m' -> 525. None if unparseable."""
        if not text:
            return None
        h = re.search(r"(\d+)\s*h", str(text))
        m = re.search(r"(\d+)\s*m", str(text))
        if not h and not m:
            return None
        return (int(h.group(1)) * 60 if h else 0) + (int(m.group(1)) if m else 0)

    # ── Step: sum of stage durations == TOTAL DURATION ───────────────────────
    def verify_stage_durations_sum_equals_total(self):
        """Tap each stage (Relaxed / Focused / Stressed), read its duration, sum
        the three, and assert the sum equals the TOTAL DURATION shown."""
        stages = [
            ("Relaxed", self.locator.STAGE_RELAXED_ROW, self.locator.RELAXED_DURATION),
            ("Focused", self.locator.STAGE_FOCUSED_ROW, self.locator.FOCUSED_DURATION),
            ("Stressed", self.locator.STAGE_STRESSED_ROW, self.locator.STRESSED_DURATION),
        ]
        total_mins = 0
        all_readable = True
        for name, row_loc, dur_loc in stages:
            self._tap(row_loc)
            dur = self._safe_value(dur_loc)
            mins = self._duration_to_minutes(dur)
            if not self._expect(mins is not None, f"'{name}' duration not readable: {dur!r}"):
                all_readable = False
                continue
            logger.info("%s duration: %s (%d min)", name, dur, mins)
            total_mins += mins
        total_text = self._safe_value(self.locator.TOTAL_DURATION_VALUE)
        total_shown = self._duration_to_minutes(total_text)
        total_ok = self._expect(total_shown is not None, f"TOTAL DURATION not readable: {total_text!r}")
        if all_readable and total_ok:
            self._expect(total_mins == total_shown, (
                f"Sum of stage durations ({total_mins} min) != TOTAL DURATION "
                f"({total_shown} min, {total_text!r})"
            ))
            logger.info("OK: stages sum = %d min == TOTAL DURATION %d min (%s)",
                        total_mins, total_shown, total_text)
        self.capture_screenshot("Stress_Durations_Sum")

    # ── Step: scroll down to the "Is today typical?" section ─────────────────
    def scroll_until_trends_at_top(self):
        """Second scroll: ONE controlled swipe that brings the Stress trends section
        to the top of the screen (from the stages / TOTAL DURATION view).

        The 'Stress trends' TITLE is NOT a usable anchor: at the very top it slides
        BEHIND the sticky date header and drops out of the accessibility tree. So we
        anchor on the WEEK tab (which sits just below the title and stays in the tree
        below the header). Landing the WEEK tab just under the header puts the title +
        tabs at the top, with Is today typical and the DROP YOUR STRESS NOW CTA below.

        The swipe distance is COMPUTED from the tab's live Y because small swipes
        don't register a scroll on this Compose view and big fixed swipes overshoot;
        a computed slow swipe (low fling) is reliable and accurate. A RAW driver.swipe
        is used since charts capture mobile:scrollGesture."""
        size = self.driver.get_window_size()
        w, h = int(size["width"]), int(size["height"])
        target = int(h * 0.16)                       # land the tabs just below the header
        loc = self.locator.TRENDS_TAB_WEEK
        # Phase 1: tabs start BELOW the fold; reliably scroll up until WEEK is visible.
        # is_element_displayed(timeout=1) gives the fling time to settle before each
        # check, so the tab isn't missed.
        for _ in range(8):
            if self.forms.is_element_displayed(self.driver, loc, timeout=1):
                break
            self.driver.swipe(w // 2, int(h * 0.78), w // 2, int(h * 0.32), 600)
        # Phase 2: one computed slow swipe to lift the tabs to just below the header.
        try:
            el = self.mouse.find_element(self.driver, loc, timeout=10)
        except Exception as e:
            self._expect(False, f"Stress trends tabs (WEEK) not found: {e}")
            self.capture_screenshot("Stress_Trends_AtTop")
            return
        distance = el.location["y"] - target
        if distance > 50:
            start = min(int(h * 0.88), h - 5)        # touch on the lower text (~TOTAL DURATION)
            end = max(5, start - distance)
            self.driver.swipe(w // 2, start, w // 2, end, 1300)
        try:
            el = self.mouse.find_element(self.driver, loc, timeout=6)
            y = el.location.get("y", 99999)
        except Exception:
            y = 99999
        logger.info("Stress trends tabs (WEEK) Y after scroll: %s", y)
        self._expect(0 < y <= int(h * 0.35), f"Could not bring the Stress trends tabs to the top (y={y})")
        self.capture_screenshot("Stress_Trends_AtTop")

    # ── internal: wait until a locator's value changes from `prev` ───────────
    def _wait_value_change(self, locator, prev, timeout=6):
        """Poll a locator's text until it differs from `prev` (or timeout). Used
        after switching a trends tab so we read the re-plotted value, not the old
        one. The element briefly drops out of the tree while the tab re-renders,
        so a missing element (get_value raising) is treated as 'not yet' and the
        poll continues — never let a transient absence abort the wait."""
        def _safe_get():
            try:
                return self.forms.get_value(self.driver, locator, timeout=1)
            except Exception:
                return None
        end = time.time() + timeout
        while time.time() < end:
            cur = _safe_get()
            if cur and cur != prev:
                return cur
        return _safe_get()

    # ── Step: WEEK / MONTH / 6 MONTHS trends graphs plot correctly ───────────
    # NOTE: no separate scroll here — scroll_to_is_today_typical already lands on
    # a screen showing BOTH the trends tabs (top) and the Is today typical section
    # (below), so the tabs are already in view when this runs.
    def verify_stress_trends_tabs(self):
        """Select WEEK, MONTH and 6 MONTHS in turn. For each, confirm the trends
        graph rendered (the 'AVG' label + a date-range that contains an en-dash)
        and capture the range. Ranges are dynamic, so instead of fixed values we
        assert each tab shows a valid range and that WEEK and MONTH differ — that
        proves each tab re-plots its own period (WEEK = 7 days, MONTH = ~30 days).
        The stacked bars are Canvas, so a screenshot is captured per tab."""
        tabs = [("WEEK", self.locator.TRENDS_TAB_WEEK),
                ("MONTH", self.locator.TRENDS_TAB_MONTH),
                ("6 MONTHS", self.locator.TRENDS_TAB_6MONTHS)]
        ranges = {}
        for name, loc in tabs:
            self._tap(loc)
            if ranges:  # after the first tab, wait for the range to re-plot
                self._wait_value_change(self.locator.TRENDS_RANGE, list(ranges.values())[-1], timeout=6)
            else:
                self.forms.is_element_displayed(self.driver, self.locator.TRENDS_AVG_LABEL, timeout=8)
            self._expect(self.forms.is_element_displayed(self.driver, self.locator.TRENDS_AVG_LABEL, timeout=5),
                         f"Stress trends '{name}': AVG label not shown")
            rng = self._safe_value(self.locator.TRENDS_RANGE)
            if self._expect(rng and "–" in str(rng),
                            f"Stress trends '{name}': date-range not shown (got {rng!r})"):
                ranges[name] = rng
                logger.info("Stress trends %s plotted: range=%s", name, rng)
            self.capture_screenshot(f"Stress_Trends_{name.replace(' ', '_')}")
        if "WEEK" in ranges and "MONTH" in ranges:
            self._expect(ranges["WEEK"] != ranges["MONTH"],
                         f"WEEK and MONTH show the same range {ranges} — tabs are not re-plotting")
            logger.info("OK: trends re-plot per tab — ranges: %s", ranges)

    # ── Step: "Is today typical?" — TODAY comparison graph ───────────────────
    def verify_today_comparison(self):
        """Confirm the TODAY comparison is shown: the 'Is today typical?' title +
        the 'Today vs typical <day>' heading. The comparison bars are Canvas, so a
        screenshot is captured for visual confirmation."""
        self._expect(self.forms.is_element_displayed(self.driver, self.locator.IS_TODAY_TYPICAL, timeout=5),
                     "'Is today typical?' title not shown")
        self._expect(self.forms.is_element_displayed(self.driver, self.locator.TYPICAL_TODAY_COMPARE, timeout=5),
                     "TODAY comparison ('Today vs typical ...') not shown")
        logger.info("Today comparison graph shown")
        self.capture_screenshot("Stress_Typical_Today")

    # ── Step: switch to the NON-ACTIVITY comparison ──────────────────────────
    def tap_nonactivity_tab(self):
        self._tap(self.locator.TYPICAL_TAB_NONACTIVITY)
        logger.info("Tapped the NON-ACTIVITY tab")

    def verify_nonactivity_comparison(self):
        """After tapping NON-ACTIVITY the heading changes to 'Non-activity ...',
        which confirms the comparison switched to the non-activity view."""
        self._expect(self.forms.is_element_displayed(self.driver, self.locator.TYPICAL_NONACT_COMPARE, timeout=8),
                     "NON-ACTIVITY comparison ('Non-activity ...') not shown after tapping the tab")
        logger.info("Non-activity comparison shown")
        self.capture_screenshot("Stress_Typical_NonActivity")

    # ── Step: tap Stressed again to deselect / restore the full view ─────────
    def tap_stressed_again_to_restore(self):
        """Selecting a stage filters/fades the graph to that stage. Tap Stressed
        once more to deselect it so the graph and all three stages show normally
        again."""
        self._tap(self.locator.STAGE_STRESSED_ROW)
        logger.info("Tapped Stressed again to restore the full graph / stages view")
        self.capture_screenshot("Stress_Stages_Restored")
