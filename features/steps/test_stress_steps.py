from pytest_bdd import scenarios, given, when, then

from pages.home_page import HomePage
from pages.health_page import HealthPage
from pages.stress_page import StressPage
from utility.liberaries.decorators import logger


# ── Navigation: Home -> Health -> previous day -> Stress card -> Stress page ──

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


@when('the user scrolls to the Stress card')
def scroll_to_stress_card(health_page: HealthPage):
    logger.info("Scrolling to the Stress card")
    health_page.scroll_to_stress_card()


@when('the user opens the Stress card')
def open_stress_card(health_page: HealthPage):
    logger.info("Opening the Stress card -> Stress detail page")
    health_page.open_stress_card()


@then('the Stress detail page is shown')
def stress_detail_shown(stress_page: StressPage):
    stress_page.verify_stress_page_shown()


@then('the Max, Min and Avg values are shown')
def stress_values_shown(stress_page: StressPage):
    stress_page.verify_values_shown()


@when('the user scrolls to the stress stages')
def scroll_to_stress_stages(stress_page: StressPage):
    stress_page.scroll_to_stress_stages()


@then('the Relaxed, Focused and Stressed stages are shown')
def stress_stages_shown(stress_page: StressPage):
    stress_page.verify_stress_stages_shown()


@then('the stress graph is plotted for the day')
def stress_graph_plotted(stress_page: StressPage):
    stress_page.verify_day_graph_plotted()


@then('the sum of the stage durations equals the total duration')
def stage_durations_sum_equals_total(stress_page: StressPage):
    stress_page.verify_stage_durations_sum_equals_total()


@when('the user taps the Stressed stage again to restore the view')
def tap_stressed_again(stress_page: StressPage):
    stress_page.tap_stressed_again_to_restore()


@when('the user scrolls down to the Is today typical section')
def scroll_to_is_today_typical(stress_page: StressPage):
    stress_page.scroll_to_is_today_typical()


# Register the scenarios — must come after the step definitions.
scenarios("../stress.feature")
