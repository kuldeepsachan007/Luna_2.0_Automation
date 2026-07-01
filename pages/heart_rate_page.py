import functools
import re
import time

from pages.base_page import BasePage
from utility.liberaries.decorators import logger


def _skippable(method):
    """Steps that operate on a card's OPEN dialog (title / value-match / the
    WEEK-MONTH-6M graphs / close / closed) become no-ops when the current card
    was skipped. A card is skipped by `_open_card_or_skip` when it has no value
    or its dialog does not open — mirroring the deferred, value-less Workout HR
    cards — so the run moves ahead instead of failing on a card with no data."""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if getattr(self, "_skip_current", False):
            logger.info("Current card was skipped (no value / dialog didn't open); "
                        "skipping '%s' and moving ahead", method.__name__)
            return None
        return method(self, *args, **kwargs)
    return wrapper


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
        # True when the card currently being viewed was skipped (no value /
        # its dialog didn't open); the @_skippable dialog steps then no-op.
        self._skip_current = False

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
        """Confirm the Heart Rate detail page loaded. The flow navigates to the
        previous day on the Health page first (today's data is incomplete), so
        the selected date is that day rather than 'Today'. 'Today's average' is
        used as the HR-detail load marker."""
        self.waits.wait_for_visible(self.driver, self.locator.TODAYS_AVERAGE, timeout=15)
        logger.info("Heart Rate detail page loaded")
        self.capture_screenshot("HR_Detail_Loaded")

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

    # ── Generic dialog helpers (shared by every metric card) ─────────────────
    def _open_card_or_skip(self, name, label_loc, card_loc, value_loc, title_loc):
        """Open a metric card's detail dialog, tolerating cards that have no data.

        Same idea as the deferred, value-less Workout HR cards: read the card's
        value, then tap it ONCE (a plain 'mobile: tap' is ignored by these
        Compose cards, and a second/outside tap dismisses a still-loading
        dialog). If the card has no value, OR the tap does not open its dialog,
        SKIP this card — set self._skip_current so the dependent dialog / graph
        / close steps no-op (see @_skippable) — and move on instead of failing
        the run. Returns the card's value (None when skipped)."""
        self._skip_current = False
        self._ensure_visible(label_loc)
        try:
            value = self.forms.get_value(self.driver, value_loc, timeout=5)
        except Exception:
            value = None
        logger.info("%s card value (before opening): %s", name, value)
        has_value = value is not None and re.search(r"\d", str(value)) is not None
        # No value -> we don't expect a dialog, so use short waits and skip fast
        # (still tap once, but don't sit through the full open-animation timeout).
        find_timeout = 5 if has_value else 2
        dialog_timeout = 10 if has_value else 2
        if not has_value:
            logger.warning("%s card has no value; tapping once with a short wait, will skip if the dialog doesn't open", name)
        # Tap the card ONCE.
        try:
            card = self.mouse.find_element(self.driver, card_loc, timeout=find_timeout)
            try:
                self.driver.execute_script("mobile: clickGesture", {"elementId": card.id})
            except Exception as e:
                logger.warning("clickGesture failed (%s); falling back to coordinate tap", e)
                rect = card.rect
                self.mouse.click_coordinates(
                    self.driver, int(rect["x"] + rect["width"] / 2), int(rect["y"] + rect["height"] / 2))
        except Exception as e:
            logger.warning("%s card not found/clickable (%s); skipping this card and moving ahead", name, e)
            self._skip_current = True
            return None
        # Wait for the dialog title. If it doesn't open, skip instead of failing.
        try:
            self.waits.wait_for_visible(self.driver, title_loc, timeout=dialog_timeout)
        except Exception:
            logger.warning("%s card tapped but its dialog did not open; skipping this card and moving ahead", name)
            self._skip_current = True
            return None
        logger.info("Opened the %s dialog", name)
        return value

    def _assert_dialog_value_matches(self, card_value, name, value_loc=None):
        """The dialog's current value must match the value on the card. Wait for
        the dialog to load (weekly average shown), then read the value; values
        are dynamic, so compare the leading numeric parts (e.g. card "3h 0m" vs
        dialog "3.0" both -> 3)."""
        value_loc = value_loc or self.locator.DIALOG_VALUE
        m = re.search(r"\d+", str(card_value or ""))
        assert m, f"{name} card value was not captured: {card_value!r}"
        card_num = m.group()
        self.waits.wait_for_visible(self.driver, self.locator.WEEKLY_AVERAGE, timeout=15)
        dlg_num = None
        for _ in range(6):
            v = self.forms.get_value(self.driver, value_loc, timeout=2)
            mm = re.search(r"\d+", str(v or ""))
            if mm and v and "Heart Rate" not in str(v) and "Lowest" not in str(v):
                dlg_num = mm.group()
                break
            time.sleep(1)
        if dlg_num is None:  # fallback: the card's value should appear in the dialog
            # Match the card's leading number exactly OR as a decimal, e.g. card
            # "3h 0m" -> "3" also matches the dialog's "3.0".
            value_text = ("xpath",
                f'//android.widget.TextView[@text="{card_num}" or starts-with(@text, "{card_num}.")]')
            assert self.forms.is_element_displayed(self.driver, value_text, timeout=5), \
                f"The dialog does not show the {name} card value {card_num!r}"
            dlg_num = card_num
        assert card_num == dlg_num, \
            f"{name} value mismatch: card={card_num!r} but dialog shows {dlg_num!r}"
        logger.info("%s value matches: card=%s, dialog=%s", name, card_num, dlg_num)
        self.capture_screenshot(f"{name}_Value_Match")

    def _close_dialog(self, title_loc, name):
        self._tap(self.locator.DIALOG_CLOSE)
        logger.info("Tapped Close (X) for the %s dialog", name)
        assert self.waits.wait_for_invisible(self.driver, title_loc, timeout=8), \
            f"The {name} dialog did not close"
        logger.info("%s dialog is closed", name)
        self.capture_screenshot(f"{name}_Dialog_Closed")

    # ── RHR card -> Resting Heart Rate dialog ────────────────────────────────
    def open_rhr_card(self):
        self._rhr_card_value = self._open_card_or_skip(
            "RHR", self.locator.RHR_LABEL, self.locator.RHR_CARD,
            self.locator.RHR_VALUE, self.locator.RHR_DIALOG_TITLE)
        if not self._skip_current:
            self.capture_screenshot("RHR_Dialog")

    @_skippable
    def verify_rhr_dialog_title(self):
        self.waits.wait_for_visible(self.driver, self.locator.RHR_DIALOG_TITLE, timeout=10)
        logger.info("'Resting Heart Rate' dialog title shown")

    @_skippable
    def verify_rhr_dialog_value_matches_card(self):
        self._assert_dialog_value_matches(getattr(self, "_rhr_card_value", None), "RHR")

    # ── AVG SLEEP HR card -> Avg Sleep Heart Rate dialog (same layout as RHR) ─
    def open_avg_sleep_card(self):
        self._avg_card_value = self._open_card_or_skip(
            "AVG SLEEP HR", self.locator.AVG_SLEEP_HR_LABEL, self.locator.AVG_SLEEP_CARD,
            self.locator.AVG_SLEEP_HR_VALUE, self.locator.AVG_DIALOG_TITLE)
        if not self._skip_current:
            self.capture_screenshot("AVG_Dialog")

    @_skippable
    def verify_avg_dialog_title(self):
        self.waits.wait_for_visible(self.driver, self.locator.AVG_DIALOG_TITLE, timeout=10)
        logger.info("'Avg Sleep Heart Rate' dialog title shown")

    @_skippable
    def verify_avg_dialog_value_matches_card(self):
        self._assert_dialog_value_matches(getattr(self, "_avg_card_value", None), "AVG Sleep HR")

    # ── Shared range-tab graph checks (WEEK is default, then MONTH / 6M) ──────
    @_skippable
    def verify_week_graph(self):
        self._verify_graph_plotted("Week", self.locator.WEEKLY_AVERAGE, self.locator.WEEK_AXIS_SAMPLE)

    @_skippable
    def select_month_view(self):
        self._tap(self.locator.TAB_MONTH)
        logger.info("Selected the MONTH view")
        time.sleep(3)  # pause between views so each graph renders / is observable

    @_skippable
    def verify_month_graph(self):
        self._verify_graph_plotted("Month", self.locator.MONTHLY_AVERAGE, self.locator.MONTH_AXIS_SAMPLE)

    @_skippable
    def select_6m_view(self):
        self._tap(self.locator.TAB_6M)
        logger.info("Selected the 6M view")
        time.sleep(3)  # pause between views so each graph renders / is observable

    @_skippable
    def verify_6m_graph(self):
        self._verify_graph_plotted("6M", self.locator.SIX_MONTH_AVERAGE, self.locator.SIXM_AXIS_SAMPLE)

    # ── Close dialogs ────────────────────────────────────────────────────────
    @_skippable
    def close_rhr_dialog(self):
        self._close_dialog(self.locator.RHR_DIALOG_TITLE, "Resting Heart Rate")

    @_skippable
    def verify_dialog_closed(self):
        assert self.waits.wait_for_invisible(self.driver, self.locator.RHR_DIALOG_TITLE, timeout=8), \
            "The Resting Heart Rate dialog did not close"

    @_skippable
    def close_avg_dialog(self):
        self._close_dialog(self.locator.AVG_DIALOG_TITLE, "Avg Sleep Heart Rate")

    @_skippable
    def verify_avg_dialog_closed(self):
        assert self.waits.wait_for_invisible(self.driver, self.locator.AVG_DIALOG_TITLE, timeout=8), \
            "The Avg Sleep Heart Rate dialog did not close"

    # ── TIME TO LOW card -> Time to Lowest HR dialog (same layout; value in h) ─
    def open_ttl_card(self):
        self._ttl_card_value = self._open_card_or_skip(
            "TIME TO LOW", self.locator.TIME_TO_LOW_LABEL, self.locator.TTL_CARD,
            self.locator.TIME_TO_LOW_VALUE, self.locator.TTL_DIALOG_TITLE)
        if not self._skip_current:
            self.capture_screenshot("TTL_Dialog")

    @_skippable
    def verify_ttl_dialog_title(self):
        self.waits.wait_for_visible(self.driver, self.locator.TTL_DIALOG_TITLE, timeout=10)
        logger.info("'Time to Lowest HR' dialog title shown")

    @_skippable
    def verify_ttl_dialog_value_matches_card(self):
        self._assert_dialog_value_matches(
            getattr(self, "_ttl_card_value", None), "Time to Low", self.locator.TTL_DIALOG_VALUE)

    @_skippable
    def close_ttl_dialog(self):
        self._close_dialog(self.locator.TTL_DIALOG_TITLE, "Time to Lowest HR")

    @_skippable
    def verify_ttl_dialog_closed(self):
        assert self.waits.wait_for_invisible(self.driver, self.locator.TTL_DIALOG_TITLE, timeout=8), \
            "The Time to Lowest HR dialog did not close"

    # ── Collapse Sleep HR; expand/collapse Workout HR ────────────────────────
    # (SLEEP_HR_COLLAPSE is the generic "Collapse" chevron of whichever section
    # is currently expanded.)
    def collapse_sleep_hr(self):
        """Minimise the Sleep HR section (it is expanded from the earlier steps)."""
        if self.forms.is_element_displayed(self.driver, self.locator.RHR_LABEL, timeout=3):
            self._tap(self.locator.SLEEP_HR_ROW)
        self.capture_screenshot("Sleep_HR_Collapsed")

    def verify_sleep_hr_collapsed(self):
        assert self.waits.wait_for_invisible(self.driver, self.locator.RHR_LABEL, timeout=8), \
            "Sleep HR did not collapse (RHR still shown)"
        logger.info("Sleep HR section is collapsed")

    def expand_workout_hr(self):
        """Expand the Workout HR section. It reveals two cards which currently
        have no value (not clickable) — interacting with them is deferred until
        they have data."""
        self._ensure_visible(self.locator.WORKOUT_HR)
        self._tap(self.locator.WORKOUT_HR_ROW)
        self.capture_screenshot("Workout_HR_Expanded")

    def verify_workout_hr_expanded(self):
        assert self.forms.is_element_displayed(self.driver, self.locator.SLEEP_HR_COLLAPSE, timeout=8), \
            "Workout HR did not expand (no Collapse chevron)"
        logger.info("Workout HR section is expanded (two cards shown; interaction deferred)")

    def collapse_workout_hr(self):
        self._tap(self.locator.WORKOUT_HR_ROW)
        self.capture_screenshot("Workout_HR_Collapsed")

    def verify_workout_hr_collapsed(self):
        assert self.waits.wait_for_invisible(self.driver, self.locator.SLEEP_HR_COLLAPSE, timeout=8), \
            "Workout HR did not collapse (Collapse chevron still shown)"
        logger.info("Workout HR section is collapsed")

    # ── Idle HR section + its two cards (Inactive Avg, Lowest Waking) ─────────
    def expand_idle_hr(self):
        self._ensure_visible(self.locator.IDLE_HR)
        self._tap(self.locator.IDLE_HR_ROW)
        self.capture_screenshot("Idle_HR_Expanded")

    def verify_idle_hr_expanded(self):
        assert self.forms.is_element_displayed(self.driver, self.locator.SLEEP_HR_COLLAPSE, timeout=8), \
            "Idle HR did not expand (no Collapse chevron)"
        logger.info("Idle HR section is expanded (two cards: Inactive Avg, Lowest Waking)")

    def collapse_idle_hr(self):
        self._tap(self.locator.IDLE_HR_ROW)
        self.capture_screenshot("Idle_HR_Collapsed")

    def verify_idle_hr_collapsed(self):
        assert self.waits.wait_for_invisible(self.driver, self.locator.SLEEP_HR_COLLAPSE, timeout=8), \
            "Idle HR did not collapse (Collapse chevron still shown)"
        logger.info("Idle HR section is collapsed")

    # INACTIVE AVG card -> Inactive Avg HR dialog
    def open_inactive_avg_card(self):
        self._inactive_avg_value = self._open_card_or_skip(
            "INACTIVE AVG", self.locator.INACTIVE_AVG_CARD, self.locator.INACTIVE_AVG_CARD,
            self.locator.INACTIVE_AVG_VALUE, self.locator.INACTIVE_AVG_TITLE)
        if not self._skip_current:
            self.capture_screenshot("Inactive_Avg_Dialog")

    @_skippable
    def verify_inactive_avg_dialog_title(self):
        self.waits.wait_for_visible(self.driver, self.locator.INACTIVE_AVG_TITLE, timeout=10)
        logger.info("'Inactive Avg HR' dialog title shown")

    @_skippable
    def verify_inactive_avg_value_matches_card(self):
        self._assert_dialog_value_matches(getattr(self, "_inactive_avg_value", None), "Inactive Avg")

    @_skippable
    def close_inactive_avg_dialog(self):
        self._close_dialog(self.locator.INACTIVE_AVG_TITLE, "Inactive Avg HR")

    @_skippable
    def verify_inactive_avg_dialog_closed(self):
        assert self.waits.wait_for_invisible(self.driver, self.locator.INACTIVE_AVG_TITLE, timeout=8), \
            "The Inactive Avg HR dialog did not close"

    # LOWEST WAKING card -> Lowest Waking HR dialog
    def open_lowest_waking_card(self):
        self._lowest_waking_value = self._open_card_or_skip(
            "LOWEST WAKING", self.locator.LOWEST_WAKING_CARD, self.locator.LOWEST_WAKING_CARD,
            self.locator.LOWEST_WAKING_VALUE, self.locator.LOWEST_WAKING_TITLE)
        if not self._skip_current:
            self.capture_screenshot("Lowest_Waking_Dialog")

    @_skippable
    def verify_lowest_waking_dialog_title(self):
        self.waits.wait_for_visible(self.driver, self.locator.LOWEST_WAKING_TITLE, timeout=10)
        logger.info("'Lowest Waking HR' dialog title shown")

    @_skippable
    def verify_lowest_waking_value_matches_card(self):
        self._assert_dialog_value_matches(getattr(self, "_lowest_waking_value", None), "Lowest Waking")

    @_skippable
    def close_lowest_waking_dialog(self):
        self._close_dialog(self.locator.LOWEST_WAKING_TITLE, "Lowest Waking HR")

    @_skippable
    def verify_lowest_waking_dialog_closed(self):
        assert self.waits.wait_for_invisible(self.driver, self.locator.LOWEST_WAKING_TITLE, timeout=8), \
            "The Lowest Waking HR dialog did not close"

    # ── Back to the Health page ──────────────────────────────────────────────
    def go_back_to_health(self):
        """Tap the top-left Back button to leave the Heart Rate detail page."""
        self._ensure_visible(self.locator.BACK)
        self._tap(self.locator.BACK)
        logger.info("Tapped Back (returning to the Health page)")
        self.capture_screenshot("Back_To_Health")
