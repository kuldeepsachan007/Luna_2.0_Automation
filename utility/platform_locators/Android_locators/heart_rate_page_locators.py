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
# The clickable element is the ROW (parent View, clickable=true), NOT the
# "Sleep HR" text (clickable=false) — tap the row to expand/collapse.
SLEEP_HR_ROW   = (AppiumBy.XPATH, '//android.widget.TextView[@text="Sleep HR"]/parent::android.view.View')
# When expanded, the row's chevron content-desc flips Expand -> Collapse.
SLEEP_HR_COLLAPSE = (AppiumBy.XPATH, '//android.view.View[@content-desc="Collapse"]')
WORKOUT_HR     = (AppiumBy.XPATH, '//android.widget.TextView[@text="Workout HR"]')
IDLE_HR        = (AppiumBy.XPATH, '//android.widget.TextView[@text="Idle HR"]')

# ── Sleep HR expanded detail cards (label -> value is its 1st following sibling)
RHR_LABEL          = (AppiumBy.XPATH, '//android.widget.TextView[@text="RHR"]')
RHR_VALUE          = (AppiumBy.XPATH, '//android.widget.TextView[@text="RHR"]/following-sibling::android.widget.TextView[1]')
AVG_SLEEP_HR_LABEL = (AppiumBy.XPATH, '//android.widget.TextView[@text="AVG SLEEP HR"]')
AVG_SLEEP_HR_VALUE = (AppiumBy.XPATH, '//android.widget.TextView[@text="AVG SLEEP HR"]/following-sibling::android.widget.TextView[1]')
TIME_TO_LOW_LABEL  = (AppiumBy.XPATH, '//android.widget.TextView[@text="TIME TO LOW"]')
TIME_TO_LOW_VALUE  = (AppiumBy.XPATH, '//android.widget.TextView[@text="TIME TO LOW"]/following-sibling::android.widget.TextView[1]')

# ── RHR card -> "Resting Heart Rate" detail dialog ───────────────────────────
# The RHR card is clickable (parent View clk=true). Tap by coordinates.
RHR_CARD          = (AppiumBy.XPATH, '//android.widget.TextView[@text="RHR"]/parent::android.view.View')
RHR_DIALOG_TITLE  = (AppiumBy.XPATH, '//android.widget.TextView[@text="Resting Heart Rate"]')
# Current value: layout "<num>" -> "bpm" (siblings); the only bare "bpm" in the
# dialog is the current-value unit, so its preceding sibling is the value.
RHR_DIALOG_VALUE  = (AppiumBy.XPATH, '(//android.widget.TextView[@text="bpm"])[1]/preceding-sibling::android.widget.TextView[1]')
DIALOG_CLOSE      = (AppiumBy.XPATH, '//android.view.View[@content-desc="Close"]')

# Range tabs (TextViews; tap by coordinates like other Compose controls).
TAB_WEEK   = (AppiumBy.XPATH, '//android.widget.TextView[@text="WEEK"]')
TAB_MONTH  = (AppiumBy.XPATH, '//android.widget.TextView[@text="MONTH"]')
TAB_6M     = (AppiumBy.XPATH, '//android.widget.TextView[@text="6M"]')

# Each period view is proven "plotted" by its period-specific AVERAGE label plus
# one of its X-axis labels (bars + Y-axis are Canvas-drawn, not queryable).
WEEKLY_AVERAGE    = (AppiumBy.XPATH, '//android.widget.TextView[@text="WEEKLY AVERAGE"]')
MONTHLY_AVERAGE   = (AppiumBy.XPATH, '//android.widget.TextView[@text="MONTHLY AVERAGE"]')
SIX_MONTH_AVERAGE = (AppiumBy.XPATH, '//android.widget.TextView[@text="6-MONTH AVERAGE"]')
WEEK_AXIS_SAMPLE  = (AppiumBy.XPATH, '//android.widget.TextView[@text="SU"]')
MONTH_AXIS_SAMPLE = (AppiumBy.XPATH, '//android.widget.TextView[@text="W1"]')
SIXM_AXIS_SAMPLE  = (AppiumBy.XPATH, '//android.widget.TextView[@text="JAN"]')
