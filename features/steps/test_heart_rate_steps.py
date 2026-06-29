from pytest_bdd import scenarios, given, when, then

from pages.home_page import HomePage
from pages.health_page import HealthPage
from pages.heart_rate_page import HeartRatePage
from utility.liberaries.decorators import logger


# ── Navigation: Home -> Health -> Heart Rate card -> Heart Rate detail ───────

@given('the user is on the Home page')
def on_home_page(luna_home_page: HomePage):
    logger.info("Ensuring the app is on the Home page")
    luna_home_page.go_to_home_page()


@when('the user opens the Health page')
def open_health_page(health_page: HealthPage):
    logger.info("Navigating Home -> Health via the bottom nav")
    health_page.tap_health_tab()
    health_page.verify_health_page()


@when('the user goes to the previous day')
def go_to_previous_day(health_page: HealthPage):
    logger.info("Navigating to the previous day (Health page)")
    health_page.go_to_previous_day()


@when('the user goes to the stable date')
def go_to_stable_date(health_page: HealthPage):
    logger.info("Navigating to the configured stable date (HEALTH_TARGET_DATE)")
    health_page.go_to_stable_date()


@when('the user opens the Heart Rate card')
def open_heart_rate_card(health_page: HealthPage):
    logger.info("Scrolling to and opening the Heart Rate card")
    health_page.scroll_to_heart_rate_card()
    health_page.open_heart_rate_card()


# ── Heart Rate detail verifications ──────────────────────────────────────────

@then('the Heart Rate detail page is shown for the current date')
def hr_detail_current_date(heart_rate_page: HeartRatePage):
    heart_rate_page.verify_open_on_current_date()


@then('a heart rate graph is plotted for the day')
def hr_graph_plotted(heart_rate_page: HeartRatePage):
    heart_rate_page.verify_hr_graph_plotted()


@when('the user expands the Sleep HR section')
def expand_sleep_hr(heart_rate_page: HeartRatePage):
    heart_rate_page.expand_sleep_hr()


@when('the user scrolls until the Sleep HR to Workout HR area is visible')
def scroll_to_workout_hr(heart_rate_page: HeartRatePage):
    heart_rate_page.scroll_to_workout_hr()


@then('the RHR, AVG Sleep HR and Time to Low details are shown')
def verify_sleep_hr_details(heart_rate_page: HeartRatePage):
    heart_rate_page.verify_sleep_hr_details()


# ── RHR card -> Resting Heart Rate dialog (value match + WEEK/MONTH/6M graphs) ─

@when('the user opens the RHR card')
def open_rhr_card(heart_rate_page: HeartRatePage):
    heart_rate_page.open_rhr_card()


@then('the Resting Heart Rate dialog is shown')
def rhr_dialog_shown(heart_rate_page: HeartRatePage):
    heart_rate_page.verify_rhr_dialog_title()


@then('the dialog value matches the RHR card value')
def rhr_value_matches_card(heart_rate_page: HeartRatePage):
    heart_rate_page.verify_rhr_dialog_value_matches_card()


@then('the weekly heart rate graph is plotted')
def weekly_graph(heart_rate_page: HeartRatePage):
    heart_rate_page.verify_week_graph()


@when('the user selects the Month view')
def select_month(heart_rate_page: HeartRatePage):
    heart_rate_page.select_month_view()


@then('the monthly heart rate graph is plotted')
def monthly_graph(heart_rate_page: HeartRatePage):
    heart_rate_page.verify_month_graph()


@when('the user selects the 6 Month view')
def select_6m(heart_rate_page: HeartRatePage):
    heart_rate_page.select_6m_view()


@then('the 6 month heart rate graph is plotted')
def sixm_graph(heart_rate_page: HeartRatePage):
    heart_rate_page.verify_6m_graph()


@when('the user closes the Resting Heart Rate dialog')
def close_rhr_dialog(heart_rate_page: HeartRatePage):
    heart_rate_page.close_rhr_dialog()


@then('the Resting Heart Rate dialog is closed')
def rhr_dialog_closed(heart_rate_page: HeartRatePage):
    heart_rate_page.verify_dialog_closed()


# ── AVG SLEEP HR card -> Avg Sleep Heart Rate dialog (mirrors the RHR flow) ───
# The WEEK/MONTH/6M graph + tab-select steps above are reused for this dialog.

@when('the user opens the AVG Sleep HR card')
def open_avg_sleep_card(heart_rate_page: HeartRatePage):
    heart_rate_page.open_avg_sleep_card()


@then('the Avg Sleep Heart Rate dialog is shown')
def avg_dialog_shown(heart_rate_page: HeartRatePage):
    heart_rate_page.verify_avg_dialog_title()


@then('the dialog value matches the AVG Sleep HR card value')
def avg_value_matches_card(heart_rate_page: HeartRatePage):
    heart_rate_page.verify_avg_dialog_value_matches_card()


@when('the user closes the Avg Sleep Heart Rate dialog')
def close_avg_dialog(heart_rate_page: HeartRatePage):
    heart_rate_page.close_avg_dialog()


@then('the Avg Sleep Heart Rate dialog is closed')
def avg_dialog_closed(heart_rate_page: HeartRatePage):
    heart_rate_page.verify_avg_dialog_closed()


# ── TIME TO LOW card -> Time to Lowest HR dialog (mirrors the RHR/AVG flow) ────

@when('the user opens the TIME TO LOW card')
def open_ttl_card(heart_rate_page: HeartRatePage):
    heart_rate_page.open_ttl_card()


@then('the Time to Lowest HR dialog is shown')
def ttl_dialog_shown(heart_rate_page: HeartRatePage):
    heart_rate_page.verify_ttl_dialog_title()


@then('the dialog value matches the TIME TO LOW card value')
def ttl_value_matches_card(heart_rate_page: HeartRatePage):
    heart_rate_page.verify_ttl_dialog_value_matches_card()


@when('the user closes the Time to Lowest HR dialog')
def close_ttl_dialog(heart_rate_page: HeartRatePage):
    heart_rate_page.close_ttl_dialog()


@then('the Time to Lowest HR dialog is closed')
def ttl_dialog_closed(heart_rate_page: HeartRatePage):
    heart_rate_page.verify_ttl_dialog_closed()


# ── Collapse Sleep HR, expand/collapse Workout HR (its two cards are deferred) ─

@when('the user minimises the Sleep HR section')
def minimise_sleep_hr(heart_rate_page: HeartRatePage):
    heart_rate_page.collapse_sleep_hr()


@then('the Sleep HR section is collapsed')
def sleep_hr_collapsed(heart_rate_page: HeartRatePage):
    heart_rate_page.verify_sleep_hr_collapsed()


@when('the user expands the Workout HR section')
def expand_workout_hr(heart_rate_page: HeartRatePage):
    heart_rate_page.expand_workout_hr()


@then('the Workout HR section is expanded')
def workout_hr_expanded(heart_rate_page: HeartRatePage):
    heart_rate_page.verify_workout_hr_expanded()


@when('the user minimises the Workout HR section')
def minimise_workout_hr(heart_rate_page: HeartRatePage):
    heart_rate_page.collapse_workout_hr()


@then('the Workout HR section is collapsed')
def workout_hr_collapsed(heart_rate_page: HeartRatePage):
    heart_rate_page.verify_workout_hr_collapsed()


# ── Idle HR section + its two cards (Inactive Avg, Lowest Waking) ─────────────
# The WEEK/MONTH/6M graph + tab-select steps above are reused for both dialogs.

@when('the user expands the Idle HR section')
def expand_idle_hr(heart_rate_page: HeartRatePage):
    heart_rate_page.expand_idle_hr()


@then('the Idle HR section is expanded')
def idle_hr_expanded(heart_rate_page: HeartRatePage):
    heart_rate_page.verify_idle_hr_expanded()


@when('the user opens the Inactive Avg card')
def open_inactive_avg_card(heart_rate_page: HeartRatePage):
    heart_rate_page.open_inactive_avg_card()


@then('the Inactive Avg HR dialog is shown')
def inactive_avg_dialog_shown(heart_rate_page: HeartRatePage):
    heart_rate_page.verify_inactive_avg_dialog_title()


@then('the dialog value matches the Inactive Avg card value')
def inactive_avg_value_matches(heart_rate_page: HeartRatePage):
    heart_rate_page.verify_inactive_avg_value_matches_card()


@when('the user closes the Inactive Avg HR dialog')
def close_inactive_avg_dialog(heart_rate_page: HeartRatePage):
    heart_rate_page.close_inactive_avg_dialog()


@then('the Inactive Avg HR dialog is closed')
def inactive_avg_dialog_closed(heart_rate_page: HeartRatePage):
    heart_rate_page.verify_inactive_avg_dialog_closed()


@when('the user opens the Lowest Waking card')
def open_lowest_waking_card(heart_rate_page: HeartRatePage):
    heart_rate_page.open_lowest_waking_card()


@then('the Lowest Waking HR dialog is shown')
def lowest_waking_dialog_shown(heart_rate_page: HeartRatePage):
    heart_rate_page.verify_lowest_waking_dialog_title()


@then('the dialog value matches the Lowest Waking card value')
def lowest_waking_value_matches(heart_rate_page: HeartRatePage):
    heart_rate_page.verify_lowest_waking_value_matches_card()


@when('the user closes the Lowest Waking HR dialog')
def close_lowest_waking_dialog(heart_rate_page: HeartRatePage):
    heart_rate_page.close_lowest_waking_dialog()


@then('the Lowest Waking HR dialog is closed')
def lowest_waking_dialog_closed(heart_rate_page: HeartRatePage):
    heart_rate_page.verify_lowest_waking_dialog_closed()


@when('the user minimises the Idle HR section')
def minimise_idle_hr(heart_rate_page: HeartRatePage):
    heart_rate_page.collapse_idle_hr()


@then('the Idle HR section is collapsed')
def idle_hr_collapsed(heart_rate_page: HeartRatePage):
    heart_rate_page.verify_idle_hr_collapsed()


# ── Back to the Health page ───────────────────────────────────────────────────

@when('the user goes back from the Heart Rate page')
def go_back_from_hr(heart_rate_page: HeartRatePage):
    heart_rate_page.go_back_to_health()


@then('the Health page is shown')
def health_page_shown(health_page: HealthPage):
    health_page.verify_health_page()


# Register the scenarios — must come after the step definitions.
scenarios("../heart_rate.feature")
