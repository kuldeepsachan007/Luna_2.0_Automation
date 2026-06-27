from appium.webdriver.common.appiumby import AppiumBy

# ═══════════════════════════════════════════════════════════════════════════
# Luna 2.0 — Heart Rate detail page locators (Android, Jetpack Compose)
#
# No resource-ids; all locators target visible text / content-desc.
# CONFIRMED from uiautomator dumps 2026-06-27: hr_detail.xml, sleep_hr.xml,
# sleephr_scrolled.xml.
# ═══════════════════════════════════════════════════════════════════════════

# ── Page identity / date ────────────────────────────────────────────────────
PAGE_TITLE     = (AppiumBy.XPATH, '//android.widget.TextView[@text="Heart Rate"]')
# Date selector reads "Today" when viewing the current day.
DATE_TODAY     = (AppiumBy.XPATH, '//android.widget.TextView[@text="Today"]')
# "Today's average" is unique to this page (not on the Health landing) -> use as
# the reliable HR-detail marker. Layout: <value> -> "bpm" -> "Today's average".
TODAYS_AVERAGE   = (AppiumBy.XPATH, "//android.widget.TextView[@text=\"Today's average\"]")
TODAYS_AVG_VALUE = (AppiumBy.XPATH, "//android.widget.TextView[@text=\"Today's average\"]/preceding-sibling::android.widget.TextView[2]")
BACK           = (AppiumBy.XPATH, '//android.view.View[@content-desc="Back"]')

# ── Heart-rate graph ─────────────────────────────────────────────────────────
# NOTE: the main HR chart (x: 12 AM..12 AM, y: 60..120) is drawn on a Canvas —
# its axis labels are NOT in the accessibility tree, so they cannot be asserted
# by locators. Presence of TODAYS_AVERAGE + a numeric average is used to confirm
# the HR data/graph section rendered; pixel-level axis checks need a screenshot.

# ── Sleep HR / Workout HR / Idle HR sections ─────────────────────────────────
SLEEP_HR       = (AppiumBy.XPATH, '//android.widget.TextView[@text="Sleep HR"]')
WORKOUT_HR     = (AppiumBy.XPATH, '//android.widget.TextView[@text="Workout HR"]')
IDLE_HR        = (AppiumBy.XPATH, '//android.widget.TextView[@text="Idle HR"]')

# ── Sleep HR expanded detail cards (label -> value is its 1st following sibling)
RHR_LABEL          = (AppiumBy.XPATH, '//android.widget.TextView[@text="RHR"]')
RHR_VALUE          = (AppiumBy.XPATH, '//android.widget.TextView[@text="RHR"]/following-sibling::android.widget.TextView[1]')
AVG_SLEEP_HR_LABEL = (AppiumBy.XPATH, '//android.widget.TextView[@text="AVG SLEEP HR"]')
AVG_SLEEP_HR_VALUE = (AppiumBy.XPATH, '//android.widget.TextView[@text="AVG SLEEP HR"]/following-sibling::android.widget.TextView[1]')
TIME_TO_LOW_LABEL  = (AppiumBy.XPATH, '//android.widget.TextView[@text="TIME TO LOW"]')
TIME_TO_LOW_VALUE  = (AppiumBy.XPATH, '//android.widget.TextView[@text="TIME TO LOW"]/following-sibling::android.widget.TextView[1]')
