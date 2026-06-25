from pytest_bdd import step, scenarios
from pages.activity_page import ActivityPage
from utility.liberaries.decorators import logger


@step('the user clicks on the activity button')
def click_activity_button(activity_page: ActivityPage):
    logger.info("Clicking on activity button")
    activity_page.click_activity_button()


@step('clicks on activity get started button')
def click_activity_get_started(activity_page: ActivityPage):
    logger.info("Clicking on activity Get Started button")
    activity_page.click_get_started_button()


@step('clicks on Activity Score')
def click_activity_score(activity_page: ActivityPage):
    logger.info("Clicking on Activity Score")
    activity_page.click_activity_score()


@step('the Activity Score page is displayed')
def activity_score_displayed(activity_page: ActivityPage):
    logger.info("Activity Score page is displayed")
    activity_page.capture_screenshot("Activity_Score_Page")


@step('the user clicks back arrow button')
def click_back_arrow(activity_page: ActivityPage):
    logger.info("Clicking back arrow button")
    activity_page.click_back_button()


@step('clicks on Goal Progress')
def click_goal_progress(activity_page: ActivityPage):
    logger.info("Clicking on Goal Progress")
    activity_page.click_goal_progress()


@step('the Goal Progress page is displayed')
def goal_progress_displayed(activity_page: ActivityPage):
    logger.info("Goal Progress page is displayed")
    activity_page.capture_screenshot("Goal_Progress_Page")


@step('clicks on Total Calories')
def click_total_calories(activity_page: ActivityPage):
    logger.info("Clicking on Total Calories")
    activity_page.click_total_calories()


@step('the Total Calories page is displayed')
def total_calories_displayed(activity_page: ActivityPage):
    logger.info("Total Calories page is displayed")
    activity_page.capture_screenshot("Total_Calories_Page")


@step('clicks on Steps')
def click_steps(activity_page: ActivityPage):
    logger.info("Clicking on Steps")
    activity_page.click_steps()


@step('the Steps page is displayed')
def steps_displayed(activity_page: ActivityPage):
    logger.info("Steps page is displayed")
    activity_page.capture_screenshot("Steps_Page")


@step('clicks on Distance')
def click_distance(activity_page: ActivityPage):
    logger.info("Clicking on Distance")
    activity_page.click_distance()


@step('the Distance page is displayed')
def distance_displayed(activity_page: ActivityPage):
    logger.info("Distance page is displayed")
    activity_page.capture_screenshot("Distance_Page")


@step('the user is back on the activity page')
def back_on_activity_page(activity_page: ActivityPage):
    logger.info("User is back on activity page")
    activity_page.capture_screenshot("Activity_Page")


# scenarios() MUST be at the bottom - after all @step definitions are registered
# This is why we don't put it in test_commons_steps.py
scenarios("../activity.feature")
