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


# Register the scenarios — must come after the step definitions.
scenarios("../heart_rate.feature")
