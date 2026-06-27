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
# Clickable row that expands/collapses the Workout HR section (like SLEEP_HR_ROW).
WORKOUT_HR_ROW = (AppiumBy.XPATH, '//android.widget.TextView[@text="Workout HR"]/parent::android.view.View')
IDLE_HR        = (AppiumBy.XPATH, '//android.widget.TextView[@text="Idle HR"]')
IDLE_HR_ROW    = (AppiumBy.XPATH, '//android.widget.TextView[@text="Idle HR"]/parent::android.view.View')

# Idle HR's two cards -> detail dialogs (same layout as RHR; bpm values).
INACTIVE_AVG_CARD    = (AppiumBy.XPATH, '//android.widget.TextView[@text="INACTIVE AVG"]/parent::android.view.View')
INACTIVE_AVG_VALUE   = (AppiumBy.XPATH, '//android.widget.TextView[@text="INACTIVE AVG"]/following-sibling::android.widget.TextView[1]')
INACTIVE_AVG_TITLE   = (AppiumBy.XPATH, '//android.widget.TextView[@text="Inactive Avg HR"]')
LOWEST_WAKING_CARD   = (AppiumBy.XPATH, '//android.widget.TextView[@text="LOWEST WAKING"]/parent::android.view.View')
LOWEST_WAKING_VALUE  = (AppiumBy.XPATH, '//android.widget.TextView[@text="LOWEST WAKING"]/following-sibling::android.widget.TextView[1]')
LOWEST_WAKING_TITLE  = (AppiumBy.XPATH, '//android.widget.TextView[@text="Lowest Waking HR"]')

# ── Sleep HR expanded detail cards (label -> value is its 1st following sibling)
RHR_LABEL          = (AppiumBy.XPATH, '//android.widget.TextView[@text="RHR"]')
RHR_VALUE          = (AppiumBy.XPATH, '//android.widget.TextView[@text="RHR"]/following-sibling::android.widget.TextView[1]')
AVG_SLEEP_HR_LABEL = (AppiumBy.XPATH, '//android.widget.TextView[@text="AVG SLEEP HR"]')
AVG_SLEEP_HR_VALUE = (AppiumBy.XPATH, '//android.widget.TextView[@text="AVG SLEEP HR"]/following-sibling::android.widget.TextView[1]')
TIME_TO_LOW_LABEL  = (AppiumBy.XPATH, '//android.widget.TextView[@text="TIME TO LOW"]')
TIME_TO_LOW_VALUE  = (AppiumBy.XPATH, '//android.widget.TextView[@text="TIME TO LOW"]/following-sibling::android.widget.TextView[1]')

# ── Metric cards -> detail dialogs (RHR + AVG Sleep HR share the same layout) ─
# Cards are clickable (parent View clk=true). Tap via clickGesture.
RHR_CARD          = (AppiumBy.XPATH, '//android.widget.TextView[@text="RHR"]/parent::android.view.View')
RHR_DIALOG_TITLE  = (AppiumBy.XPATH, '//android.widget.TextView[@text="Resting Heart Rate"]')
AVG_SLEEP_CARD    = (AppiumBy.XPATH, '//android.widget.TextView[@text="AVG SLEEP HR"]/parent::android.view.View')
AVG_DIALOG_TITLE  = (AppiumBy.XPATH, '//android.widget.TextView[@text="Avg Sleep Heart Rate"]')
# TIME TO LOW card -> "Time to Lowest HR" dialog. Same layout, but the value is
# a DURATION in hours: "3.0" + "h" (the card shows "3h 0m"); value = the number
# before the standalone "h".
TTL_CARD          = (AppiumBy.XPATH, '//android.widget.TextView[@text="TIME TO LOW"]/parent::android.view.View')
TTL_DIALOG_TITLE  = (AppiumBy.XPATH, '//android.widget.TextView[@text="Time to Lowest HR"]')
TTL_DIALOG_VALUE  = (AppiumBy.XPATH, '(//android.widget.TextView[@text="h"])[1]/preceding-sibling::android.widget.TextView[1]')
# Current value (generic for both dialogs): layout "<num>" -> "bpm" (siblings);
# the only bare "bpm" in the dialog is the current-value unit, so its preceding
# sibling is the value.
DIALOG_VALUE      = (AppiumBy.XPATH, '(//android.widget.TextView[@text="bpm"])[1]/preceding-sibling::android.widget.TextView[1]')
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
