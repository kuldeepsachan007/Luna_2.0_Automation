import time

import pytest
from pytest_bdd import step, scenarios

from pages.health_page import HealthPage
from pages.login_page import LoginPage
from pages.ring_connect_page import RingConnectPage
from utility.liberaries.decorators import logger


DEFAULT_LOGIN_EMAIL = "kuldeep.sachan@nexxbase.com"
DEFAULT_RING_SERIAL = "R2N08250600302"

# How long to wait after tapping "MEASURE NOW" before checking the result.
# Each vital takes a different physical measurement duration on the ring.
MEASURE_WAIT_SECONDS = {
    "spo2":      60,
    "stress":    40,
    "heart_rate":40,
    "skin_temp": 40,
}


# ── Resilient full-flow plumbing ─────────────────────────────────────────────
# The full flow treats each vital / card as an independent "test case": if a
# section fails, we record it, recover back to the Health page, and carry on
# with the next section instead of aborting the whole scenario. A summary step
# at the end reports how many sections passed/failed and fails the test if any
# section failed.

@pytest.fixture
def flow_results():
    """Fresh per-scenario list of (section_name, status, detail) tuples."""
    return []


def _run_section(health_page: HealthPage, flow_results, name: str, action) -> None:
    """Run one flow section. Record PASS/FAIL (never raise), then recover to the
    Health page so the next section starts clean."""
    try:
        action()
        flow_results.append((name, "PASS", ""))
        logger.info("SECTION PASS - %s", name)
    except Exception as exc:  # noqa: BLE001 - intentional: keep the flow going
        detail = (str(exc).splitlines() or [""])[0] or type(exc).__name__
        flow_results.append((name, "FAIL", detail))
        logger.error("SECTION FAIL - %s -- %s", name, detail)
    finally:
        # Always return to a known-good state for the next section.
        try:
            health_page.recover_to_health_page()
        except Exception:
            logger.warning("Could not recover to Health page after %s", name)


# ── Background: assume already logged in — just navigate to Health tab ──────

@step('the user has signed in and paired the Luna ring')
def already_signed_in(health_page: HealthPage, test_data):
    """
    Assume the user is ALREADY logged in and the ring is paired
    (typically done manually beforehand). Only taps the Health tab if the
    Health page is not already visible.

    Login + ring pairing wiring will be re-enabled later. For now we start
    automation from wherever the app currently is.
    """
    test_data.email = DEFAULT_LOGIN_EMAIL
    test_data.ring_serial = DEFAULT_RING_SERIAL

    # Detect the Health page by the SpO2 tile, which only exists on the Health
    # page. HEALTH_PAGE_TITLE (text="Health") cannot be used here because the
    # Home page also shows a "Health" label in the bottom nav, so it would
    # always look like we are "already on Health".
    if health_page.forms.is_element_displayed(
        health_page.driver, health_page.locator.SPO2_LABEL, timeout=3,
    ):
        logger.info("Background: already on Health page")
        return

    if health_page.forms.is_element_displayed(
        health_page.driver, health_page.locator.NAV_HEALTH, timeout=3,
    ):
        logger.info("Background: tapping Health tab from bottom nav")
        health_page.tap_health_tab()


@step('the user lands on the Health page')
def land_on_health_page(health_page: HealthPage):
    logger.info("Verifying Health page is displayed")
    health_page.verify_health_page()


# ── Smoke: assert main sections are rendered ─────────────────────────────────

@step('the Health page title should be visible')
def health_title_visible(health_page: HealthPage):
    health_page.waits.wait_for_visible(
        health_page.driver, health_page.locator.HEALTH_PAGE_TITLE,
    )


@step('the SpO2 tile should be visible')
def spo2_tile_visible(health_page: HealthPage):
    logger.info("Asserting SpO2 tile is visible")
    health_page.waits.wait_for_visible(
        health_page.driver, health_page.locator.SPO2_LABEL,
    )


@step('the Stress tile should be visible')
def stress_tile_visible(health_page: HealthPage):
    logger.info("Asserting Stress tile is visible")
    health_page.waits.wait_for_visible(
        health_page.driver, health_page.locator.STRESS_LABEL,
    )


@step('the Heart Rate tile should be visible')
def heart_rate_tile_visible(health_page: HealthPage):
    logger.info("Asserting Heart Rate tile is visible")
    health_page.waits.wait_for_visible(
        health_page.driver, health_page.locator.HEART_RATE_LABEL,
    )


@step('the Skin Temp tile should be visible')
def skin_temp_tile_visible(health_page: HealthPage):
    logger.info("Asserting Skin Temp tile is visible")
    health_page.waits.wait_for_visible(
        health_page.driver, health_page.locator.SKIN_TEMP_LABEL,
    )


@step('the Sleep card should be visible')
def sleep_card_visible(health_page: HealthPage):
    logger.info("Asserting Sleep card is visible")
    health_page.waits.wait_for_visible(
        health_page.driver, health_page.locator.SLEEP_CARD_LABEL,
    )


# ── Measure flow ─────────────────────────────────────────────────────────────

@step('the user taps Measure Now on the Heart Rate tile')
def tap_measure_heart_rate(health_page: HealthPage):
    logger.info("Tapping Measure Now on Heart Rate tile")
    health_page.measure_heart_rate()


@step('the user taps Measure Now on the Stress tile')
def tap_measure_stress(health_page: HealthPage):
    logger.info("Tapping Measure Now on Stress tile")
    health_page.measure_stress()


@step('the user taps Measure Now on the SpO2 tile')
def tap_measure_spo2(health_page: HealthPage):
    logger.info("Tapping Measure Now on SpO2 tile")
    health_page.measure_spo2()


@step('the user taps Measure Now on the Skin Temp tile')
def tap_measure_skin_temp(health_page: HealthPage):
    logger.info("Tapping Measure Now on Skin Temp tile")
    health_page.measure_skin_temp()


@step('the Heart Rate measurement sheet should be displayed')
def heart_rate_sheet_displayed(health_page: HealthPage):
    health_page.capture_screenshot("HeartRate_Sheet_Visible")


@step('the Stress measurement sheet should be displayed')
def stress_sheet_displayed(health_page: HealthPage):
    health_page.capture_screenshot("Stress_Sheet_Visible")


@step('the SpO2 measurement sheet should be displayed')
def spo2_sheet_displayed(health_page: HealthPage):
    health_page.capture_screenshot("SpO2_Sheet_Visible")


@step('the Skin Temp measurement sheet should be displayed')
def skin_temp_sheet_displayed(health_page: HealthPage):
    health_page.capture_screenshot("SkinTemp_Sheet_Visible")


# ── Combined-flow measure-with-retry steps ───────────────────────────────────
# These drive the full popup flow: tap MEASURE → wait → on failure tap Try
# Again → on second failure tap Close → on success tap Done.

@step('the user measures SpO2 with retry on failure')
def measure_spo2_with_retry(health_page: HealthPage):
    secs = MEASURE_WAIT_SECONDS["spo2"]
    logger.info("Measuring SpO2 (wait %ds, retry once on failure)", secs)
    health_page.measure_spo2_with_retry(wait_seconds=secs)


@step('the user measures Stress with retry on failure')
def measure_stress_with_retry(health_page: HealthPage):
    secs = MEASURE_WAIT_SECONDS["stress"]
    logger.info("Measuring Stress (wait %ds, retry once on failure)", secs)
    health_page.measure_stress_with_retry(wait_seconds=secs)


@step('the user measures Heart Rate with retry on failure')
def measure_heart_rate_with_retry(health_page: HealthPage):
    secs = MEASURE_WAIT_SECONDS["heart_rate"]
    logger.info("Measuring Heart Rate (wait %ds, retry once on failure)", secs)
    health_page.measure_heart_rate_with_retry(wait_seconds=secs)


@step('the user measures Skin Temp with retry on failure')
def measure_skin_temp_with_retry(health_page: HealthPage):
    secs = MEASURE_WAIT_SECONDS["skin_temp"]
    logger.info("Measuring Skin Temp (wait %ds, retry once on failure)", secs)
    health_page.measure_skin_temp_with_retry(wait_seconds=secs)


@step('the user should be back on the Health page')
def back_on_health_page(health_page: HealthPage):
    """After the popup closes (Done or X), assert the Health page is visible."""
    health_page.waits.wait_for_visible(
        health_page.driver, health_page.locator.HEALTH_PAGE_TITLE, timeout=15,
    )
    health_page.capture_screenshot("Back_On_Health_Page")


# ── Verify the measured reading shows up on the vital's tile ──────────────────

@step('the SpO2 reading should match the value on the tile')
def verify_spo2_reading(health_page: HealthPage):
    health_page.verify_reading_matches_tile(
        "SpO2", health_page.locator.SPO2_TILE_VALUE,
    )


@step('the Stress reading should match the value on the tile')
def verify_stress_reading(health_page: HealthPage):
    health_page.verify_reading_matches_tile(
        "Stress", health_page.locator.STRESS_TILE_VALUE,
    )


@step('the Heart Rate reading should match the value on the tile')
def verify_heart_rate_reading(health_page: HealthPage):
    health_page.verify_reading_matches_tile(
        "Heart Rate", health_page.locator.HEART_RATE_TILE_VALUE,
    )


@step('the Skin Temp reading should match the value on the tile')
def verify_skin_temp_reading(health_page: HealthPage):
    health_page.verify_reading_matches_tile(
        "Skin Temp", health_page.locator.SKIN_TEMP_TILE_VALUE,
    )


# ── Sleep card → Sleep detail page ───────────────────────────────────────────

@step('the user opens the Sleep card')
def open_sleep_card(health_page: HealthPage):
    logger.info("Opening the Sleep card → Sleep page")
    health_page.open_sleep_card()


@step('the user notes the Sleep card value')
def note_sleep_card_value(health_page: HealthPage):
    health_page.read_sleep_card_value()


@step('the Sleep page should be displayed')
def sleep_page_displayed(health_page: HealthPage):
    logger.info("Verifying the Sleep page is displayed")
    health_page.verify_sleep_page()


@step('the Sleep page value should match the card value')
def sleep_page_value_matches_card(health_page: HealthPage):
    health_page.verify_sleep_page_value()


@step('the user goes back to the Health page')
def go_back_to_health(health_page: HealthPage):
    logger.info("Going back from Sleep page to Health page")
    health_page.go_back_from_sleep_page()


# ── Sleep detail: deficit math + sleep stages (Awake) ────────────────────────

@step('the sleep window should be close to the actual sleep')
def verify_sleep_window_vs_actual(health_page: HealthPage):
    logger.info("Verifying sleep window (start->end) vs actual sleep (+/-20 min)")
    health_page.verify_sleep_window_vs_actual()


@step('the Sleep deficit should equal Sleep needed minus Actual sleep')
def verify_sleep_deficit(health_page: HealthPage):
    logger.info("Verifying Sleep needed - Actual = deficit")
    health_page.verify_sleep_deficit()


@step('the user scrolls to the sleep stages')
def scroll_to_sleep_stages(health_page: HealthPage):
    logger.info("Scrolling to the sleep stages breakdown")
    health_page.scroll_to_sleep_stages()


@step('the Awake stage should show its duration')
def awake_stage_shows_duration(health_page: HealthPage):
    health_page.read_awake_stage()


@step('the user opens the Awake stage')
def open_awake_stage(health_page: HealthPage):
    logger.info("Opening the Awake stage")
    health_page.open_awake_stage()


@step('the user scrolls to the sleep metrics')
def scroll_to_sleep_metrics(health_page: HealthPage):
    logger.info("Scrolling from hypnogram to Toss & Turns / Midpoint metrics")
    health_page.scroll_to_sleep_metrics()


@step('the user scrolls to the end of the Sleep page')
def scroll_to_sleep_end(health_page: HealthPage):
    logger.info("Scrolling from metrics to the end of the Sleep page")
    health_page.scroll_to_sleep_end()


@step('the user verifies each sleep stage bar and the total')
def verify_sleep_stage_bars(health_page: HealthPage):
    logger.info("Verifying sleep stage progress bars (select/deselect) + total")
    health_page.verify_sleep_stage_bars()


# ── Heart Rate card → Heart Rate detail page (with value verification) ────────

@step('the user scrolls to the Heart Rate card')
def scroll_to_hr_card(health_page: HealthPage):
    logger.info("Scrolling to the Heart Rate card")
    health_page.scroll_to_heart_rate_card()


@step('the user notes the Heart Rate card value')
def note_hr_card_value(health_page: HealthPage):
    health_page.read_heart_rate_card_value()


@step('the user opens the Heart Rate card')
def open_hr_card(health_page: HealthPage):
    logger.info("Opening the Heart Rate card → Heart Rate page")
    health_page.open_heart_rate_card()


@step('the Heart Rate page should be displayed')
def hr_page_displayed(health_page: HealthPage):
    logger.info("Verifying the Heart Rate page is displayed")
    health_page.verify_heart_rate_page()


@step('the Heart Rate page value should match the card value')
def hr_page_value_matches_card(health_page: HealthPage):
    health_page.verify_hr_page_value_matches_card()


@step('the user goes back from the Heart Rate page')
def go_back_from_hr_page(health_page: HealthPage):
    logger.info("Going back from Heart Rate page to Health page")
    health_page.go_back_from_heart_rate_page()


# ── Stress tile → Stress detail page (with valid-reading verification) ────────

@step('the user scrolls to the Stress card')
def scroll_to_stress_card(health_page: HealthPage):
    logger.info("Scrolling to the Stress card")
    health_page.scroll_to_stress_card()


@step('the user notes the Stress card value')
def note_stress_card_value(health_page: HealthPage):
    health_page.read_stress_card_value()


@step('the user opens the Stress card')
def open_stress_card(health_page: HealthPage):
    logger.info("Opening the Stress card → Stress page")
    health_page.open_stress_card()


@step('the Stress page should be displayed')
def stress_page_displayed(health_page: HealthPage):
    logger.info("Verifying the Stress page is displayed")
    health_page.verify_stress_page()


@step('the Stress page value should match the card value')
def stress_page_value_matches_card(health_page: HealthPage):
    health_page.verify_stress_page_value()


@step('the user closes the Stress page')
def close_stress_page(health_page: HealthPage):
    logger.info("Closing the Stress page")
    health_page.close_stress_page()


@step('the Stress card should remain at the top of the screen')
def stress_card_remains_at_top(health_page: HealthPage):
    """After returning from the Stress detail page, re-position so the Stress
    tile sits at the top — keeps the card(s) below it visible so the next
    card's automation does not have to scroll again."""
    logger.info("Keeping the Stress card at the top after returning")
    health_page.scroll_to_stress_card()


# ── Activity card → Activity detail page (verify steps match) ─────────────────

@step('the user scrolls to the Activity card')
def scroll_to_activity_card(health_page: HealthPage):
    logger.info("Scrolling to the Activity card")
    health_page.scroll_to_activity_card()


@step('the user notes the Activity card values')
def note_activity_card_values(health_page: HealthPage):
    health_page.read_activity_card_value()


@step('the user opens the Activity card')
def open_activity_card(health_page: HealthPage):
    logger.info("Opening the Activity card → Activity page")
    health_page.open_activity_card()


@step('the Activity page should be displayed')
def activity_page_displayed(health_page: HealthPage):
    logger.info("Verifying the Activity page is displayed")
    health_page.verify_activity_page()


@step('the Activity page values should match the card')
def activity_page_values_match_card(health_page: HealthPage):
    health_page.verify_activity_page_value()


@step('the user goes back from the Activity page')
def go_back_from_activity_page(health_page: HealthPage):
    logger.info("Going back from Activity page to Health page")
    health_page.go_back_from_activity_page()


# ── Composite, resilient section-steps (used by the full-flow scenario) ──────
# Each step is ONE "test case": it runs the section's actions, and on any
# failure it records the failure and moves on (recovery handled by
# _run_section). The granular steps above are left untouched for the other,
# strict scenarios.

@step('the user measures and verifies the SpO2 vital')
def section_spo2(health_page: HealthPage, flow_results):
    def action():
        health_page.waits.wait_for_visible(
            health_page.driver, health_page.locator.SPO2_LABEL, timeout=10,
        )
        health_page.measure_spo2_with_retry(MEASURE_WAIT_SECONDS["spo2"])
        health_page.verify_reading_matches_tile(
            "SpO2", health_page.locator.SPO2_TILE_VALUE,
        )
    _run_section(health_page, flow_results, "SpO2 vital", action)


@step('the user measures and verifies the Stress vital')
def section_stress_vital(health_page: HealthPage, flow_results):
    def action():
        health_page.waits.wait_for_visible(
            health_page.driver, health_page.locator.STRESS_LABEL, timeout=10,
        )
        health_page.measure_stress_with_retry(MEASURE_WAIT_SECONDS["stress"])
        health_page.verify_reading_matches_tile(
            "Stress", health_page.locator.STRESS_TILE_VALUE,
        )
    _run_section(health_page, flow_results, "Stress vital", action)


@step('the user measures and verifies the Heart Rate vital')
def section_heart_rate_vital(health_page: HealthPage, flow_results):
    def action():
        health_page.waits.wait_for_visible(
            health_page.driver, health_page.locator.HEART_RATE_LABEL, timeout=10,
        )
        health_page.measure_heart_rate_with_retry(MEASURE_WAIT_SECONDS["heart_rate"])
        health_page.verify_reading_matches_tile(
            "Heart Rate", health_page.locator.HEART_RATE_TILE_VALUE,
        )
    _run_section(health_page, flow_results, "Heart Rate vital", action)


@step('the user measures and verifies the Skin Temp vital')
def section_skin_temp_vital(health_page: HealthPage, flow_results):
    def action():
        health_page.waits.wait_for_visible(
            health_page.driver, health_page.locator.SKIN_TEMP_LABEL, timeout=10,
        )
        health_page.measure_skin_temp_with_retry(MEASURE_WAIT_SECONDS["skin_temp"])
        health_page.verify_reading_matches_tile(
            "Skin Temp", health_page.locator.SKIN_TEMP_TILE_VALUE,
        )
    _run_section(health_page, flow_results, "Skin Temp vital", action)


@step('the user verifies the Sleep card')
def section_sleep_card(health_page: HealthPage, flow_results):
    def action():
        health_page.verify_sleep_card()
        health_page.read_sleep_card_value()
        health_page.open_sleep_card()
        health_page.verify_sleep_page()
        health_page.verify_sleep_page_value()
        health_page.go_back_from_sleep_page()
    _run_section(health_page, flow_results, "Sleep card", action)


@step('the user verifies the Heart Rate card')
def section_heart_rate_card(health_page: HealthPage, flow_results):
    def action():
        health_page.scroll_to_heart_rate_card()
        health_page.read_heart_rate_card_value()
        health_page.open_heart_rate_card()
        health_page.verify_heart_rate_page()
        health_page.verify_hr_page_value_matches_card()
        health_page.go_back_from_heart_rate_page()
    _run_section(health_page, flow_results, "Heart Rate card", action)


@step('the user verifies the Stress card')
def section_stress_card(health_page: HealthPage, flow_results):
    def action():
        health_page.scroll_to_stress_card()
        health_page.read_stress_card_value()
        health_page.open_stress_card()
        health_page.verify_stress_page()
        health_page.verify_stress_page_value()
        health_page.close_stress_page()
    _run_section(health_page, flow_results, "Stress card", action)


@step('the user verifies the Activity card')
def section_activity_card(health_page: HealthPage, flow_results):
    def action():
        health_page.scroll_to_activity_card()
        health_page.read_activity_card_value()
        health_page.open_activity_card()
        health_page.verify_activity_page()
        health_page.verify_activity_page_value()
        health_page.go_back_from_activity_page()
    _run_section(health_page, flow_results, "Activity card", action)


@step('the flow result summary is reported')
def report_flow_summary(flow_results):
    """Log a pass/fail summary for the whole flow and fail the test if ANY
    section failed (so the result is visible) — but only AFTER the entire flow
    has run."""
    total = len(flow_results)
    passed = sum(1 for _, status, _ in flow_results if status == "PASS")
    failed = total - passed

    lines = [
        "",
        "=" * 64,
        f"  HEALTH FLOW SUMMARY — {passed}/{total} sections passed, {failed} failed",
        "-" * 64,
    ]
    for name, status, detail in flow_results:
        mark = "PASS" if status == "PASS" else "FAIL"
        lines.append(f"  [{mark}] {name}" + (f"  --  {detail}" if detail else ""))
    lines.append("=" * 64)
    logger.info("\n".join(lines))

    failed_names = [name for name, status, _ in flow_results if status == "FAIL"]
    assert not failed_names, (
        f"{failed}/{total} flow sections failed: {', '.join(failed_names)} "
        f"(see the HEALTH FLOW SUMMARY above for details)"
    )


# Register the scenarios — must be at the bottom of the file, after every
# @step definition is in scope.
scenarios("../health_page.feature")
