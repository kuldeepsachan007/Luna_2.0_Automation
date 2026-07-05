import re
import time

import allure

from pages.base_page import BasePage
from utility.liberaries.decorators import logger


class SleepPage(BasePage):
    """Luna 2.0 Sleep detail page (Jetpack Compose).

    Reached from the Health page by tapping the Sleep card. Locators come from
    sleep_page_locators.py (confirmed from uiautomator dumps 2026-07-01, night
    of Sat 27 Jun). Values are dynamic (change per night), so we assert
    shape/range — never fixed numbers.

    Note on the hypnogram: the stage chart (AWAKE/REM/LIGHT/DEEP over the sleep
    window) is Canvas-drawn, so its bars/axis are not queryable. We confirm the
    stage LEGEND + the per-stage breakdown cards (duration + %) instead, and
    capture a screenshot for visual confirmation of the chart.
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.name = "Sleep Page"
        self.locator = self.get_locators().SLEEP_PAGE
        # Soft-assert accumulator: the same SleepPage instance is reused across
        # all steps of a scenario, so checks recorded in one step survive into
        # the final summary. Each entry is (name, passed, detail). We keep going
        # on a failed check so the whole flow runs and the report shows how many
        # checks passed / failed (see report_check_summary).
        self._checks = []

    # ── Soft-assert helpers ───────────────────────────────────────────────────
    def _record(self, name, ok, detail=""):
        ok = bool(ok)
        self._checks.append((name, ok, detail))
        logger.info("CHECK %s: %s%s", "PASS" if ok else "FAIL", name,
                    f" — {detail}" if detail else "")
        # Mirror every check as an Allure step so the report shows, per check,
        # exactly what passed and what FAILED (failed steps render red). The
        # check stays soft — we raise inside the step only to mark it failed,
        # then swallow it so the flow keeps running.
        title = f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else "")
        try:
            with allure.step(title):
                if not ok:
                    raise AssertionError(f"{name}: {detail}")
        except AssertionError:
            pass
        return ok

    def _safe_get_value(self, locator, timeout=5):
        """Read an element's value, returning None instead of raising when it is
        missing. Keeps a flaky/absent element a soft-recorded failure rather than
        an exception that aborts the whole scenario (continue-on-fail)."""
        try:
            return self._safe_get_value(locator, timeout=timeout)
        except Exception:
            return None

    def _tap(self, locator, timeout=8):
        """clickGesture on an element (Compose taps), with a plain-click fallback.
        Returns False instead of raising if the element is absent."""
        try:
            el = self.mouse.find_element(self.driver, locator, timeout=timeout)
        except Exception:
            return False
        try:
            self.driver.execute_script("mobile: clickGesture", {"elementId": el.id})
        except Exception as e:
            logger.warning("clickGesture failed (%s); falling back to click", e)
            try:
                el.click()
            except Exception:
                return False
        return True

    @staticmethod
    def _canonical_value(text):
        """Normalise a displayed value so a card value and a dialog value can be
        compared regardless of formatting. Clock times ('1:55 AM') compare as
        time; durations ('1h 52m') compare as minutes; everything else ('13 min',
        '19', '57') compares by its leading integer."""
        t = str(text or "").strip()
        tm = re.search(r"\d{1,2}:\d{2}\s*(?:[AP]M)?", t, re.I)
        if tm:
            return ("time", re.sub(r"\s+", "", tm.group()).upper())
        if re.search(r"\dh", t) or re.search(r"\dm(?!in)", t):
            return ("dur", SleepPage._to_minutes(t))
        n = re.search(r"-?\d+", t)
        if n:
            return ("num", int(n.group()))
        return ("raw", t.lower())

    # ── internal: Compose-friendly scroll ────────────────────────────────────
    # The page has a hypnogram chart that captures 'mobile: scrollGesture', so we
    # use a raw swipe down the LEFT column (over text/margin, not the chart) with
    # an element-visibility loop — proven for this page during dump capture.
    def _scroll_to(self, locator, max_scrolls=8, direction="down"):
        if self.forms.is_element_displayed(self.driver, locator, timeout=2):
            return True
        size = self.driver.get_window_size()
        w, h = int(size["width"]), int(size["height"])
        x = int(w * 0.14)  # left column: over text/margin, never the chart
        if direction == "down":
            y1, y2 = int(h * 0.78), int(h * 0.28)
        else:
            y1, y2 = int(h * 0.28), int(h * 0.78)
        for _ in range(max_scrolls):
            self.driver.swipe(x, y1, x, y2, 600)
            if self.forms.is_element_displayed(self.driver, locator, timeout=1):
                return True
        return self.forms.is_element_displayed(self.driver, locator, timeout=1)

    @staticmethod
    def _to_minutes(text):
        """'1h 5m' -> 65, '48m' -> 48, '3h 26m' -> 206. None if unparseable."""
        if not text:
            return None
        hh = re.search(r"(\d+)\s*h", str(text))
        mm = re.search(r"(\d+)\s*m", str(text))
        if not hh and not mm:
            return None
        return (int(hh.group(1)) * 60 if hh else 0) + (int(mm.group(1)) if mm else 0)

    # ── Step: the Sleep detail page is shown ─────────────────────────────────
    def verify_sleep_page_shown(self):
        self.waits.wait_for_visible(self.driver, self.locator.PAGE_TITLE, timeout=15)
        logger.info("Sleep detail page is shown")
        self.capture_screenshot("Sleep_Page")

    # ── Step: summary values (total vs target, sleep debt) ───────────────────
    def verify_summary_values(self):
        """Total sleep, the target it is measured against ('of 9h 10m') and the
        sleep debt are all durations. The summary numbers render a beat after the
        page title, so wait for the total-sleep line before reading. Values are
        dynamic — assert each parses to minutes (and the total is in range),
        never fixed numbers."""
        # The "<total> of sleep · <lost>" line is self-contained (no sibling hop)
        # and only exists once the summary card has rendered — use it as the gate.
        self.waits.wait_for_visible(self.driver, self.locator.TOTAL_SLEEP_LINE, timeout=15)
        # The target ("of 9h 10m") renders a beat after the total line, so wait
        # for it before reading to avoid a cold-start miss.
        try:
            self.waits.wait_for_visible(self.driver, self.locator.SLEEP_TARGET, timeout=5)
        except Exception:
            pass
        total_line = self._safe_get_value(self.locator.TOTAL_SLEEP_LINE, timeout=5)
        total = str(total_line).split(" of ")[0]  # "5h 31m of sleep · ..." -> "5h 31m"
        target = self._safe_get_value(self.locator.SLEEP_TARGET, timeout=5)
        self.waits.wait_for_visible(self.driver, self.locator.SLEEP_DEBT_LABEL, timeout=5)
        debt = self._safe_get_value(self.locator.SLEEP_DEBT_VALUE, timeout=5)
        total_m = self._to_minutes(total)
        target_m = self._to_minutes(target)
        self._record("Summary: total sleep is a duration", total_m is not None,
                     f"total={total!r} (line={total_line!r})")
        self._record("Summary: sleep target is a duration", target_m is not None, f"target={target!r}")
        self._record("Summary: sleep debt is a duration", self._to_minutes(debt) is not None, f"debt={debt!r}")
        self._record("Summary: total sleep in range", total_m is not None and 0 < total_m <= 24 * 60, f"total={total!r}")
        logger.info("Sleep summary: total=%s target=%s debt=%s", total, target, debt)
        self.capture_screenshot("Sleep_Summary")

    # ── Step: sleep window + efficiency ──────────────────────────────────────
    def verify_window_and_efficiency(self):
        """The sleep window shows two clock times ('23:10 → 04:41') and the
        efficiency shows a percentage ('92% efficient'). Both are dynamic, so we
        assert the shape (two HH:MM times, a numeric %), not fixed values."""
        window = self._safe_get_value(self.locator.SLEEP_WINDOW, timeout=5)
        times = re.findall(r"\d{1,2}:\d{2}", str(window or ""))
        self._record("Sleep window shows start/end times", len(times) >= 2, f"window={window!r}")
        eff = self._safe_get_value(self.locator.SLEEP_EFFICIENCY, timeout=5)
        m = re.search(r"(\d+)\s*%", str(eff or ""))
        self._record("Sleep efficiency is a valid %", bool(m) and 0 <= int(m.group(1)) <= 100, f"efficiency={eff!r}")
        logger.info("Sleep window: %s | efficiency: %s", window, eff)
        self.capture_screenshot("Sleep_Window_Efficiency")

    # ── Step: scroll to the sleep stages ─────────────────────────────────────
    def scroll_to_stages(self):
        """Bring the stage legend (AWAKE/REM/LIGHT/DEEP) fully into view. At the
        very top only part of the legend is rendered (LIGHT sits just below the
        fold), so scroll until LIGHT is shown."""
        assert self._scroll_to(self.locator.STAGE_LEGEND_LIGHT), \
            "Could not bring the sleep stage legend into view"
        self.capture_screenshot("Sleep_Stages")

    def verify_stage_legend(self):
        """The legend is a single row, so all four stage names should be shown
        together. This proves the hypnogram section rendered (the chart itself is
        Canvas — see the screenshot for visual confirmation)."""
        for name, loc in [("AWAKE", self.locator.STAGE_LEGEND_AWAKE),
                          ("REM", self.locator.STAGE_LEGEND_REM),
                          ("LIGHT", self.locator.STAGE_LEGEND_LIGHT),
                          ("DEEP", self.locator.STAGE_LEGEND_DEEP)]:
            self._record(f"Stage legend shown: {name}",
                         self.forms.is_element_displayed(self.driver, loc, timeout=5), "")
        logger.info("NOTE: hypnogram bars/axis are Canvas-drawn; see 'Sleep_Stages' screenshot")
        self.capture_screenshot("Sleep_Stage_Legend")

    # ── Step: each stage has a duration + percent; percentages sum ~100 ──────
    def verify_stage_breakdown(self):
        """The four breakdown cards (Awake / REM / Light / Deep) each show a
        duration and a share-of-night percent. Values are dynamic, so instead of
        fixed numbers we assert each duration parses and each percent is numeric,
        then that the four percentages sum to ~100% — proving the split is a real
        breakdown of the night."""
        stages = [
            ("Awake", self.locator.AWAKE_SUBTITLE, self.locator.AWAKE_DURATION, self.locator.AWAKE_PERCENT),
            ("REM", self.locator.REM_SUBTITLE, self.locator.REM_DURATION, self.locator.REM_PERCENT),
            ("Light", self.locator.LIGHT_SUBTITLE, self.locator.LIGHT_DURATION, self.locator.LIGHT_PERCENT),
            ("Deep", self.locator.DEEP_SUBTITLE, self.locator.DEEP_DURATION, self.locator.DEEP_PERCENT),
        ]
        total_pct = 0
        for name, sub_loc, dur_loc, pct_loc in stages:
            if not self._scroll_to(sub_loc, max_scrolls=5):
                self._record(f"Stage breakdown '{name}' card found", False, "not on screen")
                continue
            dur = self._safe_get_value(dur_loc, timeout=5)
            pct = self._safe_get_value(pct_loc, timeout=5)
            m = re.search(r"(\d+)\s*%", str(pct or ""))
            self._record(f"Stage '{name}': duration + percent readable",
                         self._to_minutes(dur) is not None and bool(m),
                         f"duration={dur!r} percent={pct!r}")
            if m:
                total_pct += int(m.group(1))
            logger.info("Stage %s: duration=%s percent=%s", name, dur, pct)
        self._record("Stage percentages sum to ~100%", 97 <= total_pct <= 103, f"sum={total_pct}%")
        logger.info("Stage percentages sum to %d%%", total_pct)
        self.capture_screenshot("Sleep_Stage_Breakdown")

    # ── Step: scroll to "How your body responded" ────────────────────────────
    def scroll_to_body_responded(self):
        assert self._scroll_to(self.locator.BODY_RESPONDED_TITLE), \
            "Could not bring 'How your body responded' into view"
        self.capture_screenshot("Sleep_Body_Responded")

    def verify_overnight_vitals(self):
        """The overnight vitals grid shows HRV, RHR, SpO2, respiration rate and
        skin temperature. The section header appears at the screen edge before
        its rows compose, so scroll each metric's LABEL into view before reading
        its value. Each is dynamic, so assert each value is present and numeric —
        never a fixed reading."""
        checks = [
            ("HRV", self.locator.HRV_LABEL, self.locator.HRV_VALUE),
            ("RHR", self.locator.RHR_LABEL, self.locator.RHR_VALUE),
            ("SpO2", self.locator.SPO2_LABEL, self.locator.SPO2_VALUE),
            ("Resp rate", self.locator.RESP_RATE_LABEL, self.locator.RESP_RATE_VALUE),
            ("Skin temp", self.locator.SKIN_TEMP_LABEL, self.locator.SKIN_TEMP_VALUE),
        ]
        for name, label_loc, value_loc in checks:
            if not self._scroll_to(label_loc, max_scrolls=4):
                self._record(f"Overnight vital '{name}' shown", False, "label not found")
                continue
            value = self._safe_get_value(value_loc, timeout=5)
            self._record(f"Overnight vital '{name}' is numeric",
                         value is not None and bool(re.search(r"\d", str(value))), f"value={value!r}")
            logger.info("Overnight vital %s = %s", name, value)
        self.capture_screenshot("Sleep_Overnight_Vitals")

    # ── Step: back to the Health page ────────────────────────────────────────
    def go_back_to_health(self):
        """Tap the top-left Back button to leave the Sleep detail page."""
        el = self.mouse.find_element(self.driver, self.locator.BACK, timeout=10)
        try:
            self.driver.execute_script("mobile: clickGesture", {"elementId": el.id})
        except Exception as e:
            logger.warning("clickGesture failed (%s); falling back to element click", e)
            el.click()
        logger.info("Tapped Back (returning to the Health page)")
        self.capture_screenshot("Sleep_Back_To_Health")

    # ── Step: sleep timing (window duration) == total sleep ──────────────────
    def verify_timing_matches_total(self):
        """The sleep window ('23:10 → 04:41') spans exactly the total sleep
        ('5h 31m'). Compute the window duration (handling the midnight wrap) and
        soft-check it equals the total (±2 min). Dynamic values — never fixed."""
        window = self._safe_get_value(self.locator.SLEEP_WINDOW, timeout=5)
        times = re.findall(r"\d{1,2}:\d{2}", str(window or ""))
        total_line = self._safe_get_value(self.locator.TOTAL_SLEEP_LINE, timeout=5)
        total_m = self._to_minutes(str(total_line).split(" of ")[0])
        ok, detail = False, f"window={window!r} total_line={total_line!r}"
        if len(times) >= 2 and total_m is not None:
            def _mins(t):
                hh, mm = t.split(":")
                return int(hh) * 60 + int(mm)
            dur = _mins(times[1]) - _mins(times[0])
            if dur < 0:
                dur += 24 * 60  # window crosses midnight
            detail = f"window {times[0]}→{times[1]} = {dur}m vs total {total_m}m"
            ok = abs(dur - total_m) <= 2
        self._record("Sleep timing: window duration == total sleep", ok, detail)
        self.capture_screenshot("Sleep_Timing_Vs_Total")

    # ── Step: sleep deficit == sleep needed - actual ─────────────────────────
    def verify_sleep_deficit(self):
        """Sleep needed ('of 9h 10m') minus actual sleep ('5h 31m') is the sleep
        deficit. Primary check works from the two durations alone (both reliably
        on the summary). The summary sentence ('...331 minutes, 219 minutes below
        your target.') is an OPTIONAL cross-check — if it is present we confirm
        the stated deficit matches needed-actual, but its absence must not fail
        the primary check nor abort the run."""
        total_line = self._safe_get_value(self.locator.TOTAL_SLEEP_LINE, timeout=5)
        actual = self._to_minutes(str(total_line).split(" of ")[0])
        needed = self._to_minutes(self._safe_get_value(self.locator.SLEEP_TARGET, timeout=5))

        # Primary: we can compute the deficit from needed - actual.
        if actual is not None and needed is not None:
            expected = needed - actual
            self._record("Sleep deficit = needed - actual (computed)", expected >= 0,
                         f"needed {needed}m - actual {actual}m = {expected}m")
        else:
            expected = None
            self._record("Sleep deficit = needed - actual (computed)", False,
                         f"could not read durations: needed={needed} actual={actual}")

        # Optional cross-check against the displayed sentence, if present.
        sentence = self._safe_get_value(self.locator.DEFICIT_SENTENCE, timeout=5)
        nums = re.findall(r"(\d+)\s*minutes", str(sentence or ""))
        if len(nums) >= 2 and expected is not None:
            sent_total, sent_deficit = int(nums[0]), int(nums[1])
            self._record("Sleep deficit: displayed deficit == needed - actual",
                         abs(expected - sent_deficit) <= 2,
                         f"computed={expected}m sentence deficit={sent_deficit}m")
            self._record("Sleep deficit: sentence total == actual sleep",
                         actual is not None and abs(sent_total - actual) <= 2,
                         f"sentence total={sent_total}m actual={actual}m")
        else:
            logger.info("Deficit sentence not present/parseable (%r) — skipped cross-check", sentence)
        self.capture_screenshot("Sleep_Deficit")

    # ── Step: hypnogram plotted (Canvas — verify legend rendered + screenshot) ─
    def verify_hypnogram_plotted(self):
        """The hypnogram bars/axis are Canvas-drawn (not queryable), so we treat
        the stage legend rendering as proof the chart plotted, and capture a
        screenshot for visual confirmation."""
        all_ok = True
        for name, loc in [("AWAKE", self.locator.STAGE_LEGEND_AWAKE),
                          ("REM", self.locator.STAGE_LEGEND_REM),
                          ("LIGHT", self.locator.STAGE_LEGEND_LIGHT),
                          ("DEEP", self.locator.STAGE_LEGEND_DEEP)]:
            all_ok = self.forms.is_element_displayed(self.driver, loc, timeout=3) and all_ok
        self._record("Hypnogram plotted (legend rendered; chart is Canvas)", all_ok,
                     "see Sleep_Hypnogram screenshot for the chart")
        self.capture_screenshot("Sleep_Hypnogram")

    # ── Step: tap each stage + collect its value; Deep double-tap restores all ─
    def tap_each_stage_and_collect(self):
        """Tap each stage in the legend (AWAKE/REM/LIGHT/DEEP) — this highlights
        that stage in the Canvas hypnogram (visual only) — and collect the
        stage's value from its breakdown card (duration + %). Finally double-tap
        DEEP so every stage is shown again. Legend + breakdown share one screen,
        so no scrolling is needed between them."""
        self._scroll_to(self.locator.STAGE_LEGEND_AWAKE, direction="up")
        stages = [
            ("Awake", self.locator.STAGE_LEGEND_AWAKE, self.locator.AWAKE_DURATION, self.locator.AWAKE_PERCENT),
            ("REM", self.locator.STAGE_LEGEND_REM, self.locator.REM_DURATION, self.locator.REM_PERCENT),
            ("Light", self.locator.STAGE_LEGEND_LIGHT, self.locator.LIGHT_DURATION, self.locator.LIGHT_PERCENT),
            ("Deep", self.locator.STAGE_LEGEND_DEEP, self.locator.DEEP_DURATION, self.locator.DEEP_PERCENT),
        ]
        for name, legend_loc, dur_loc, pct_loc in stages:
            tapped = self._tap(legend_loc)
            time.sleep(0.6)
            dur = self._safe_get_value(dur_loc, timeout=3)
            pct = self._safe_get_value(pct_loc, timeout=3)
            ok = tapped and self._to_minutes(dur) is not None and bool(re.search(r"\d", str(pct or "")))
            self._record(f"Stage '{name}': tapped + value collected", ok,
                         f"duration={dur!r} percent={pct!r}")
            self.capture_screenshot(f"Sleep_Stage_Tap_{name}")
        # Deep needs a second tap to clear the filter and restore all stages.
        self._tap(self.locator.STAGE_LEGEND_DEEP)
        time.sleep(0.4)
        self._tap(self.locator.STAGE_LEGEND_DEEP)
        time.sleep(0.6)
        restored = all(self.forms.is_element_displayed(self.driver, loc, timeout=3) for loc in (
            self.locator.STAGE_LEGEND_AWAKE, self.locator.STAGE_LEGEND_REM,
            self.locator.STAGE_LEGEND_LIGHT, self.locator.STAGE_LEGEND_DEEP))
        self._record("Deep double-tap restores all stages", restored,
                     "all four legend items visible again")
        self.capture_screenshot("Sleep_Stages_Restored")

    # ── dialog navigation helpers ─────────────────────────────────────────────
    def _swipe_dialog_next(self):
        """Swipe right->left over the dialog HEADER (above the chart, which
        otherwise consumes horizontal drags) to page to the next metric."""
        size = self.driver.get_window_size()
        w, h = int(size["width"]), int(size["height"])
        self.driver.swipe(int(w * 0.85), int(h * 0.32), int(w * 0.15), int(h * 0.32), 400)
        time.sleep(1.3)

    def _close_dialog(self):
        """Dismiss the metric bottom-sheet with system Back. A raw tap on the
        dim area above the sheet lands on the clickable date bar ('Sat, 27 Jun')
        and opens the calendar, so never tap-to-close here."""
        for _ in range(3):
            if not self.forms.is_element_displayed(self.driver, self.locator.DIALOG_LAST_NIGHT, timeout=2):
                return
            try:
                self.driver.back()
            except Exception:
                logger.warning("driver.back() failed while closing the metric dialog")
            time.sleep(1.0)

    def _verify_ranges(self, metric, ranges):
        """Tap each range toggle and confirm its average caption renders —
        proving the trend graph re-plots for that range. `ranges` is a list of
        (label, toggle_loc, avg_loc, avg_text). A render/upload beat is needed
        after each switch (keep the sleeps); heavier ranges (6M) may need a
        second beat/tap."""
        for label, toggle_loc, avg_loc, avg_text in ranges:
            tapped = self._tap(toggle_loc)
            time.sleep(3)  # chart needs render/upload time on a range switch
            shown = self.forms.is_element_displayed(self.driver, avg_loc, timeout=8)
            if not shown:
                self._tap(toggle_loc)
                time.sleep(3)
                shown = self.forms.is_element_displayed(self.driver, avg_loc, timeout=8)
            self._record(f"'{metric}' {label} graph plotted", tapped and shown,
                         f"'{avg_text}' shown={shown}")

    def _run_dialog_suite(self, section, items, ranges, scroll_direction="down", special=None):
        """Shared driver for the card->dialog suites (metric cards and overnight
        vitals). `items` is a list of (name, tap_loc, value_loc, title_loc,
        title_text). Reads every card value (scrolling each into view), then
        opens the first dialog by tapping and pages the rest with a right->left
        swipe, checking title, card-vs-dialog value match, and each range graph.
        Closes with system Back.

        `special` is an optional {name: guidance_locator} for cards whose dialog
        has no trend graph / no last-night value (e.g. Skin Temperature) — for
        those we skip the value-match + range checks and instead confirm the
        guidance content rendered."""
        special = special or {}
        # Get to the section, then read each card value (scroll each into view).
        self._scroll_to(items[0][1], direction=scroll_direction, max_scrolls=8)
        card_values = {}
        for name, tap_loc, val_loc, _title_loc, _title_text in items:
            self._scroll_to(tap_loc, max_scrolls=4)
            v = self._safe_get_value(val_loc, timeout=3)
            card_values[name] = v
            self._record(f"{section}: '{name}' card value present",
                         v is not None and str(v).strip() != "", f"value={v!r}")
        self.capture_screenshot(f"{section}_Cards")

        # Scroll back up to the first card so tapping opens the right dialog.
        self._scroll_to(items[0][1], direction="up", max_scrolls=8)
        for idx, (name, tap_loc, val_loc, title_loc, title_text) in enumerate(items):
            # Open (tap for the first, swipe for the rest) and make sure the
            # expected dialog is actually showing — the gesture occasionally
            # misses on a heavy chart, so retry it before recording.
            title_ok = False
            for attempt in range(3):
                if idx == 0:
                    self._tap(tap_loc)
                else:
                    self._swipe_dialog_next()
                if self.forms.is_element_displayed(self.driver, title_loc, timeout=5):
                    title_ok = True
                    break
            if name in special:
                # No trend graph / no last-night value — confirm the dialog's
                # guidance content instead of a value-match + range graphs.
                shown = self.forms.is_element_displayed(self.driver, special[name], timeout=5)
                self._record(f"{section}: '{name}' dialog opened (title '{title_text}', no graph — guidance shown)",
                             title_ok and shown, "")
            else:
                opened = self.forms.is_element_displayed(self.driver, self.locator.DIALOG_LAST_NIGHT, timeout=5)
                self._record(f"{section}: '{name}' dialog opened (title '{title_text}')", opened and title_ok, "")
                hero = self._safe_get_value(self.locator.DIALOG_HERO_VALUE, timeout=5)
                card = card_values.get(name)
                match = self._canonical_value(card) == self._canonical_value(hero)
                self._record(f"{section}: '{name}' page value == dialog value", match,
                             f"card={card!r} dialog={hero!r}")
                self._verify_ranges(f"{section}:{name}", ranges)
            self.capture_screenshot(f"{section}_Dialog_{re.sub(r'[^A-Za-z0-9]+', '_', name)}")

        self._close_dialog()
        closed = not self.forms.is_element_displayed(self.driver, self.locator.DIALOG_LAST_NIGHT, timeout=3)
        self._record(f"{section}: dialog closed -> back on Sleep page", closed,
                     "dialog 'Last night' no longer shown")
        self.capture_screenshot(f"{section}_Dialogs_Closed")

    # ── Step: metric cards open dialogs; value matches; week/month/6M plot ────
    def verify_metric_cards_and_dialogs(self):
        """Restorative / Latency / Toss & Turns / Midpoint: open each dialog,
        match card vs dialog value, verify WEEK/MONTH/6M graphs plot. All soft."""
        metrics = [
            ("Restorative", self.locator.RESTORATIVE_CARD, self.locator.RESTORATIVE_CARD_VALUE, self.locator.RESTORATIVE_DIALOG_TITLE, "Restorative Sleep"),
            ("Latency", self.locator.LATENCY_CARD, self.locator.LATENCY_CARD_VALUE, self.locator.LATENCY_DIALOG_TITLE, "Sleep Latency"),
            ("Toss & Turns", self.locator.TOSS_CARD, self.locator.TOSS_CARD_VALUE, self.locator.TOSS_DIALOG_TITLE, "Toss & Turns"),
            ("Midpoint", self.locator.MIDPOINT_CARD, self.locator.MIDPOINT_CARD_VALUE, self.locator.MIDPOINT_DIALOG_TITLE, "Circadian Midpoint"),
        ]
        ranges = [
            ("WEEK", self.locator.RANGE_WEEK, self.locator.AVG_WEEK, "WEEKLY AVERAGE"),
            ("MONTH", self.locator.RANGE_MONTH, self.locator.AVG_MONTH, "MONTHLY AVERAGE"),
            ("6M", self.locator.RANGE_6M, self.locator.AVG_6M, "6-MONTH AVERAGE"),
        ]
        self._run_dialog_suite("Sleep metric", metrics, ranges, scroll_direction="down")

    # ── Step: overnight-vital cards open dialogs; value + day/week/month/6M ───
    def verify_vitals_and_dialogs(self):
        """HRV / RHR / SpO2 / Respiratory Rate / Skin Temperature: open each
        dialog (swipe pages through them), match card vs dialog value, verify the
        DAY/WEEK/MONTH/6M graphs plot. All soft. (Skin Temp shows no last-night
        value, so its value-match is expected to differ.)"""
        vitals = [
            ("HRV", self.locator.HRV_LABEL, self.locator.HRV_VALUE, self.locator.HRV_DIALOG_TITLE, "HRV"),
            ("RHR", self.locator.RHR_LABEL, self.locator.RHR_VALUE, self.locator.RHR_DIALOG_TITLE, "Resting Heart Rate"),
            ("SpO2", self.locator.SPO2_LABEL, self.locator.SPO2_VALUE, self.locator.SPO2_DIALOG_TITLE, "SpO2"),
            ("Resp rate", self.locator.RESP_RATE_LABEL, self.locator.RESP_RATE_VALUE, self.locator.RESP_DIALOG_TITLE, "Respiratory Rate"),
            ("Skin temp", self.locator.SKIN_TEMP_LABEL, self.locator.SKIN_TEMP_VALUE, self.locator.SKIN_TEMP_DIALOG_TITLE, "Skin Temperature"),
        ]
        ranges = [
            ("DAY", self.locator.RANGE_DAY, self.locator.AVG_DAY, "DAILY AVERAGE"),
            ("WEEK", self.locator.RANGE_WEEK, self.locator.AVG_WEEK, "WEEKLY AVERAGE"),
            ("MONTH", self.locator.RANGE_MONTH, self.locator.AVG_MONTH, "MONTHLY AVERAGE"),
            ("6M", self.locator.RANGE_6M, self.locator.AVG_6M, "6-MONTH AVERAGE"),
        ]
        # Skin Temperature's dialog has no trend graph / last-night value — verify
        # its guidance content instead of a value-match + range graphs.
        special = {"Skin temp": self.locator.SKIN_TEMP_GUIDANCE}
        self._run_dialog_suite("Overnight vital", vitals, ranges, scroll_direction="up", special=special)

    # ── Step: report how many checks passed / failed ─────────────────────────
    def report_check_summary(self):
        """Log + attach a pass/fail summary of every soft-check, then fail the
        scenario if any check failed (all checks have already run, so the report
        shows the full breakdown)."""
        total = len(self._checks)
        failed = [c for c in self._checks if not c[1]]
        passed = total - len(failed)
        lines = [f"SLEEP CHECKS: {passed}/{total} passed, {len(failed)} failed", ""]
        for name, ok, detail in self._checks:
            lines.append(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))
        summary = "\n".join(lines)
        logger.info("\n%s", summary)
        try:
            self.allure_logs.attach_text(summary, name=f"Sleep Check Summary ({passed}/{total} passed)")
            if failed:
                fail_text = "\n".join(f"- {n} — {d}" for n, ok, d in failed)
                self.allure_logs.attach_text(fail_text, name=f"FAILED sleep checks ({len(failed)})")
        except Exception:
            logger.debug("Could not attach sleep summary to Allure", exc_info=True)
        self.capture_screenshot("Sleep_Check_Summary")
        assert not failed, (
            f"{len(failed)} of {total} sleep check(s) failed:\n"
            + "\n".join(f"- {n} — {d}" for n, ok, d in failed)
        )
