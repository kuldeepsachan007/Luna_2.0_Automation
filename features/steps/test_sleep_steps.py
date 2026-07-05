from pytest_bdd import scenarios, given, when, then

from pages.home_page import HomePage
from pages.health_page import HealthPage
from pages.sleep_page import SleepPage
from utility.liberaries.decorators import logger


# ── Navigation: Home -> Health -> stable date -> Sleep card -> Sleep page ─────

@given('the user is on the Home page')
def on_home_page(luna_home_page: HomePage):
    logger.info("Ensuring the app is on the Home page")
    luna_home_page.go_to_home_page()


@when('the user opens the Health page')
def open_health_page(health_page: HealthPage):
    logger.info("Navigating Home -> Health via the bottom nav")
    health_page.tap_health_tab()
    health_page.verify_health_page()


@when('the user goes to the stable date')
def go_to_stable_date(health_page: HealthPage):
    logger.info("Navigating to the configured stable date (HEALTH_TARGET_DATE)")
    health_page.go_to_stable_date()


@when('the user opens the Sleep card')
def open_sleep_card(health_page: HealthPage):
    logger.info("Opening the Sleep card -> Sleep detail page")
    health_page.verify_sleep_card()
    health_page.open_sleep_card()


# ── Sleep detail page assertions ──────────────────────────────────────────────

@then('the Sleep detail page is shown')
def sleep_detail_shown(sleep_page: SleepPage):
    sleep_page.verify_sleep_page_shown()


@then('the sleep summary values are shown')
def sleep_summary_values(sleep_page: SleepPage):
    sleep_page.verify_summary_values()


@then('the sleep window and efficiency are shown')
def sleep_window_efficiency(sleep_page: SleepPage):
    sleep_page.verify_window_and_efficiency()


@then('the sleep timing matches the total sleep duration')
def sleep_timing_matches_total(sleep_page: SleepPage):
    sleep_page.verify_timing_matches_total()


@then('the sleep deficit equals sleep needed minus actual sleep')
def sleep_deficit(sleep_page: SleepPage):
    sleep_page.verify_sleep_deficit()


@when('the user scrolls to the sleep stages')
def scroll_to_sleep_stages(sleep_page: SleepPage):
    sleep_page.scroll_to_stages()


@then('the sleep stage legend is shown')
def sleep_stage_legend(sleep_page: SleepPage):
    sleep_page.verify_stage_legend()


@then('the sleep hypnogram is plotted')
def sleep_hypnogram_plotted(sleep_page: SleepPage):
    sleep_page.verify_hypnogram_plotted()


@when('the user taps each sleep stage and collects its value')
def tap_each_sleep_stage(sleep_page: SleepPage):
    sleep_page.tap_each_stage_and_collect()


@then('the sleep stage breakdown percentages sum to about 100')
def sleep_stage_breakdown(sleep_page: SleepPage):
    sleep_page.verify_stage_breakdown()


@then('the sleep metric cards open dialogs with matching values and week month 6M graphs')
def sleep_metric_dialogs(sleep_page: SleepPage):
    sleep_page.verify_metric_cards_and_dialogs()


@when('the user scrolls to how the body responded')
def scroll_to_body_responded(sleep_page: SleepPage):
    sleep_page.scroll_to_body_responded()


@then('the overnight vitals are shown')
def sleep_overnight_vitals(sleep_page: SleepPage):
    sleep_page.verify_overnight_vitals()


@then('the overnight vital cards open dialogs with matching values and day week month 6M graphs')
def overnight_vital_dialogs(sleep_page: SleepPage):
    sleep_page.verify_vitals_and_dialogs()


@when('the user taps the back arrow')
def tap_back_arrow(sleep_page: SleepPage):
    sleep_page.go_back_to_health()


@then('the Health page is shown')
def health_page_shown(health_page: HealthPage):
    health_page.verify_back_on_health()


@when('the user returns to the Home page')
def return_to_home_page(health_page: HealthPage):
    logger.info("Sleep -> Health -> Home: tapping the bottom-nav Home tab (no relaunch)")
    health_page.tap_home_tab()


@then('the sleep check summary is reported')
def sleep_check_summary(sleep_page: SleepPage):
    sleep_page.report_check_summary()


# Register the scenarios — must come after the step definitions.
scenarios("../sleep.feature")
