from pytest_bdd import step
from pages.home_page import HomePage
from utility.liberaries.decorators import logger


@step('user lands on the home page screen')
def verify_home_page(luna_home_page: HomePage):
    logger.info("Verifying home page")
    luna_home_page.verify_home_page()



# ── Circadian Alignment steps ──────────────────────────────────────────────────

@step('scrolls up to find the Circadian Alignment card')
def scroll_up_to_find_circadian_card(luna_home_page: HomePage):
    logger.info("Scrolling up to reveal the Circadian Alignment card")
    luna_home_page.scroll_up_to_find_circadian_card()


@step('clicks on the Circadian Alignment arrow button')
def click_circadian_arrow_button(luna_home_page: HomePage):
    logger.info("Clicking the arrow button on the Circadian Alignment card")
    luna_home_page.click_circadian_arrow_button()


@step('the Circadian Alignment page is displayed')
def verify_circadian_alignment_page(luna_home_page: HomePage):
    logger.info("Verifying Circadian Alignment page is displayed")
    luna_home_page.verify_circadian_alignment_page()


@step('the user clicks back from Circadian Alignment page')
def click_back_from_circadian(luna_home_page: HomePage):
    logger.info("Clicking back button from Circadian Alignment page")
    luna_home_page.click_circadian_back_button()


@step('the user is back on the home page')
def back_on_home_page(luna_home_page: HomePage):
    logger.info("User is back on home page")
    luna_home_page.capture_screenshot("Home_Page_After_Circadian")

# ── Activity Card steps ────────────────────────────────────────────────────────

@step('scrolls to find the Activity card on home page')
def scroll_to_activity_card(luna_home_page: HomePage):
    logger.info("Scrolling to find the Activity card on home page")
    luna_home_page.scroll_to_activity_card()


@step('clicks on the Activity arrow button on home page')
def click_activity_arrow_button(luna_home_page: HomePage):
    logger.info("Clicking the arrow button on the Activity card")
    luna_home_page.click_activity_arrow_button()


# ── One Tap Vitals steps ───────────────────────────────────────────────────────

@step('the user scrolls to find One Tap Vitals on home page')
def scroll_to_one_tap_vitals(luna_home_page: HomePage):
    logger.info("Scrolling to One Tap Vitals section on home page")
    luna_home_page.scroll_to_one_tap_vitals()


@step('the One Tap Vitals section should be displayed')
def verify_one_tap_vitals_displayed(luna_home_page: HomePage):
    logger.info("One Tap Vitals section is now visible")
    luna_home_page.capture_screenshot("One_Tap_Vitals_Visible")


@step('the user waits 10 seconds before starting vitals measurement')
def wait_before_vitals_measurement(luna_home_page: HomePage):
    logger.info("Waiting 10 seconds before starting vitals measurement")
    luna_home_page.wait_before_vitals()


@step('the user taps on Heart Rate')
def tap_heart_rate(luna_home_page: HomePage):
    logger.info("Tapping Heart Rate in One Tap Vitals")
    luna_home_page.tap_heart_rate_and_wait()


@step('the user waits 40 seconds for Heart Rate reading')
def wait_for_heart_rate_reading(luna_home_page: HomePage):
    logger.info("Heart Rate reading wait completed")
    luna_home_page.capture_screenshot("Heart_Rate_Reading_Done")


@step('the user taps on Stress')
def tap_stress(luna_home_page: HomePage):
    logger.info("Tapping Stress in One Tap Vitals")
    luna_home_page.tap_stress_and_wait()


@step('the user waits 40 seconds for Stress reading')
def wait_for_stress_reading(luna_home_page: HomePage):
    logger.info("Stress reading wait completed")
    luna_home_page.capture_screenshot("Stress_Reading_Done")


@step('the user taps on SpO2')
def tap_spo2(luna_home_page: HomePage):
    logger.info("Tapping SpO2 in One Tap Vitals")
    luna_home_page.tap_spo2_and_wait()


@step('the user waits 60 seconds for SpO2 reading')
def wait_for_spo2_reading(luna_home_page: HomePage):
    logger.info("SpO2 reading wait completed")
    luna_home_page.capture_screenshot("SpO2_Reading_Done")


@step('the user taps on Skin Temperature')
def tap_skin_temperature(luna_home_page: HomePage):
    logger.info("Tapping Skin Temperature in One Tap Vitals")
    luna_home_page.tap_skin_temp_and_wait()


@step('the user waits 40 seconds for Skin Temperature reading')
def wait_for_skin_temp_reading(luna_home_page: HomePage):
    logger.info("Skin Temperature reading wait completed")
    luna_home_page.capture_screenshot("Skin_Temp_Reading_Done")


# ── Add new home page element steps below ─────────────────────────────────────
