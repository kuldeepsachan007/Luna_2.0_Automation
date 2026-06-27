from pytest_bdd import scenarios, given, when, then

from pages.home_page import HomePage
from pages.health_page import HealthPage
from pages.heart_rate_page import HeartRatePage
from utility.liberaries.decorators import logger


# ── Navigation: Home -> Health -> Heart Rate card -> Heart Rate detail ───────

@given('the user is on the Home page')
def on_home_page(luna_home_page: HomePage):
    logger.info("Verifying the Home page is displayed")
    luna_home_page.verify_home_page()


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


# Register the scenarios — must come after the step definitions.
scenarios("../heart_rate.feature")
