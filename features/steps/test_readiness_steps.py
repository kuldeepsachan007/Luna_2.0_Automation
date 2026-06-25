from pytest_bdd import step, scenarios
from pages.readiness_page import ReadinessPage
from utility.liberaries.decorators import logger



@step('the user clicks on the readiness button')
def click_readiness_button(readiness_page: ReadinessPage):
    logger.info("Clicking on readiness button")
    readiness_page.click_readiness_button()


@step('clicks on readiness get started button')
def click_readiness_get_started(readiness_page: ReadinessPage):
    logger.info("Clicking on readiness Get Started button")
    readiness_page.click_get_started_button()


@step('clicks on Readiness Score')
def click_readiness_score(readiness_page: ReadinessPage):
    logger.info("Clicking on Readiness Score")
    readiness_page.click_readiness_score()


@step('the Readiness Score page is displayed')
def readiness_score_displayed(readiness_page: ReadinessPage):
    logger.info("Readiness Score page is displayed")
    readiness_page.capture_screenshot("Readiness_Score_Page")


@step('the user clicks readiness back button')
def click_readiness_back(readiness_page: ReadinessPage):
    logger.info("Clicking readiness back button")
    readiness_page.click_back_button()


@step('clicks on Resting Heart Rate')
def click_resting_heart_rate(readiness_page: ReadinessPage):
    logger.info("Clicking on Resting Heart Rate")
    readiness_page.click_resting_heart_rate()


@step('the Resting Heart Rate trends view page is displayed')
def resting_heart_rate_displayed(readiness_page: ReadinessPage):
    logger.info("Resting Heart Rate trends view page is displayed")
    readiness_page.capture_screenshot("Resting_Heart_Rate_Trends_View")


@step('clicks on HRV')
def click_hrv(readiness_page: ReadinessPage):
    logger.info("Clicking on HRV")
    readiness_page.click_hrv()


@step('the HRV trends view page is displayed')
def hrv_displayed(readiness_page: ReadinessPage):
    logger.info("HRV trends view page is displayed")
    readiness_page.capture_screenshot("HRV_Trends_View")


@step('clicks on Skin Temperature')
def click_skin_temp(readiness_page: ReadinessPage):
    logger.info("Clicking on Skin Temperature")
    readiness_page.click_skin_temp()


@step('the Skin Temperature trends view page is displayed')
def skin_temp_displayed(readiness_page: ReadinessPage):
    logger.info("Skin Temperature trends view page is displayed")
    readiness_page.capture_screenshot("Skin_Temp_Trends_View")


@step('clicks on Respiratory Rate')
def click_respiratory_rate(readiness_page: ReadinessPage):
    logger.info("Clicking on Respiratory Rate")
    readiness_page.click_respiratory_rate()


@step('the Readiness Respiratory Rate trends view page is displayed')
def respiratory_rate_displayed(readiness_page: ReadinessPage):
    logger.info("Respiratory Rate trends view page is displayed")
    readiness_page.capture_screenshot("Respiratory_Rate_Trends_View")


@step('the user is back on the readiness page')
def back_on_readiness_page(readiness_page: ReadinessPage):
    logger.info("User is back on readiness page")
    readiness_page.capture_screenshot("Readiness_Page")


# scenarios() MUST be at the bottom - after all @step definitions are registered
scenarios("../readiness.feature")
