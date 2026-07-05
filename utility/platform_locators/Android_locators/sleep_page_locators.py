from appium.webdriver.common.appiumby import AppiumBy

# ═══════════════════════════════════════════════════════════════════════════
# Luna 2.0 — Sleep detail page locators (Android, Jetpack Compose)
#
# No resource-ids; every locator targets visible text / content-desc.
# CONFIRMED from uiautomator dumps 2026-07-01 (night of Sat, 27 Jun):
#   sleep_detail_top.xml (summary), sleep_s1.xml (stages), sleep_s2.xml (body).
# The page is reached from the Health page's Sleep card. All values are dynamic
# (change per night) — assert shape/range, never fixed numbers.
# ═══════════════════════════════════════════════════════════════════════════

# ── Page identity / header ───────────────────────────────────────────────────
# "Sleep" (exact) is the top app-bar title; other page text is "Sleep fell
# short…", "Sleep latency", "Sleep Environment", "SLEEP DEBT" — none match exact.
PAGE_TITLE = (AppiumBy.XPATH, '//android.widget.TextView[@text="Sleep"]')
BACK       = (AppiumBy.XPATH, '//android.view.View[@content-desc="Back"]')

# ── Summary: total sleep vs target, sleep debt ───────────────────────────────
# All summary texts are flat siblings that Compose renders lazily, so anchoring a
# value by sibling-position is race-prone (the big number appears a beat after
# the page title). Prefer SELF-CONTAINED texts instead:
#   - total sleep: the "5h 31m of sleep · 14 min lost" line (parse the leader)
#   - target:      the "of 9h 10m" line (starts with "of ")
# The sleep-debt value has no self-contained text, so read its sibling AFTER the
# "SLEEP DEBT" label is visible (section rendered).
TOTAL_SLEEP_LINE = (AppiumBy.XPATH, '//android.widget.TextView[contains(@text,"of sleep")]')
SLEEP_TARGET     = (AppiumBy.XPATH, '//android.widget.TextView[starts-with(@text,"of ") and contains(@text,"h")]')
SLEEP_DEBT_LABEL = (AppiumBy.XPATH, '//android.widget.TextView[@text="SLEEP DEBT"]')
SLEEP_DEBT_VALUE = (AppiumBy.XPATH, '//android.widget.TextView[@text="SLEEP DEBT"]/following-sibling::android.widget.TextView[1]')

# ── Sleep window + efficiency ────────────────────────────────────────────────
# Window text carries the arrow, e.g. "23:10 → 04:41" (unique on the page).
SLEEP_WINDOW     = (AppiumBy.XPATH, '//android.widget.TextView[contains(@text,"→")]')
SLEEP_EFFICIENCY = (AppiumBy.XPATH, '//android.widget.TextView[contains(@text,"efficient")]')

# ── Sleep stages legend (row above the hypnogram chart) ──────────────────────
STAGE_LEGEND_AWAKE = (AppiumBy.XPATH, '//android.widget.TextView[@text="AWAKE"]')
STAGE_LEGEND_REM   = (AppiumBy.XPATH, '//android.widget.TextView[@text="REM"]')
STAGE_LEGEND_LIGHT = (AppiumBy.XPATH, '//android.widget.TextView[@text="LIGHT"]')
STAGE_LEGEND_DEEP  = (AppiumBy.XPATH, '//android.widget.TextView[@text="DEEP"]')

# ── Sleep stage breakdown cards ──────────────────────────────────────────────
# Each card = <stage> <subtitle> <duration> <percent> (4 consecutive siblings).
# The subtitle is unique per stage (the stage word itself repeats elsewhere), so
# anchor on the subtitle: duration = following-sibling[1], percent = [2].
AWAKE_SUBTITLE = (AppiumBy.XPATH, '//android.widget.TextView[@text="Natural wakings"]')
AWAKE_DURATION = (AppiumBy.XPATH, '//android.widget.TextView[@text="Natural wakings"]/following-sibling::android.widget.TextView[1]')
AWAKE_PERCENT  = (AppiumBy.XPATH, '//android.widget.TextView[@text="Natural wakings"]/following-sibling::android.widget.TextView[2]')
REM_SUBTITLE   = (AppiumBy.XPATH, '//android.widget.TextView[@text="Mind repair"]')
REM_DURATION   = (AppiumBy.XPATH, '//android.widget.TextView[@text="Mind repair"]/following-sibling::android.widget.TextView[1]')
REM_PERCENT    = (AppiumBy.XPATH, '//android.widget.TextView[@text="Mind repair"]/following-sibling::android.widget.TextView[2]')
LIGHT_SUBTITLE = (AppiumBy.XPATH, '//android.widget.TextView[@text="Sleep continuity"]')
LIGHT_DURATION = (AppiumBy.XPATH, '//android.widget.TextView[@text="Sleep continuity"]/following-sibling::android.widget.TextView[1]')
LIGHT_PERCENT  = (AppiumBy.XPATH, '//android.widget.TextView[@text="Sleep continuity"]/following-sibling::android.widget.TextView[2]')
DEEP_SUBTITLE  = (AppiumBy.XPATH, '//android.widget.TextView[@text="Body repair"]')
DEEP_DURATION  = (AppiumBy.XPATH, '//android.widget.TextView[@text="Body repair"]/following-sibling::android.widget.TextView[1]')
DEEP_PERCENT   = (AppiumBy.XPATH, '//android.widget.TextView[@text="Body repair"]/following-sibling::android.widget.TextView[2]')

# ── "How your body responded" — overnight vitals ─────────────────────────────
# Each metric = <label> <value> <unit> <status>; value = following-sibling[1].
# (SKIN TEMP has no separate unit: value "+0.2°" then status "ABOVE BASELINE".)
# The section header appears at the screen edge before the metric rows compose,
# so scroll each LABEL into view before reading its value.
BODY_RESPONDED_TITLE = (AppiumBy.XPATH, '//android.widget.TextView[@text="How your body responded"]')
HRV_LABEL       = (AppiumBy.XPATH, '//android.widget.TextView[@text="HRV"]')
HRV_VALUE       = (AppiumBy.XPATH, '//android.widget.TextView[@text="HRV"]/following-sibling::android.widget.TextView[1]')
RHR_LABEL       = (AppiumBy.XPATH, '//android.widget.TextView[@text="RHR"]')
RHR_VALUE       = (AppiumBy.XPATH, '//android.widget.TextView[@text="RHR"]/following-sibling::android.widget.TextView[1]')
SPO2_LABEL      = (AppiumBy.XPATH, '//android.widget.TextView[starts-with(@text,"SPO")]')
SPO2_VALUE      = (AppiumBy.XPATH, '//android.widget.TextView[starts-with(@text,"SPO")]/following-sibling::android.widget.TextView[1]')
RESP_RATE_LABEL = (AppiumBy.XPATH, '//android.widget.TextView[@text="RESP RATE"]')
RESP_RATE_VALUE = (AppiumBy.XPATH, '//android.widget.TextView[@text="RESP RATE"]/following-sibling::android.widget.TextView[1]')
SKIN_TEMP_LABEL = (AppiumBy.XPATH, '//android.widget.TextView[@text="SKIN TEMP"]')
SKIN_TEMP_VALUE = (AppiumBy.XPATH, '//android.widget.TextView[@text="SKIN TEMP"]/following-sibling::android.widget.TextView[1]')

# ── Sleep deficit (top summary) ──────────────────────────────────────────────
# The summary sentence carries both the total and the below-target (deficit)
# minutes: "Total sleep lasted 331 minutes, 219 minutes below your target."
# We verify needed - actual == below-target (the displayed deficit, also shown
# as the duration "3h 39m" in the summary row).
DEFICIT_SENTENCE = (AppiumBy.XPATH, '//android.widget.TextView[contains(@text,"below your target")]')

# ── Sleep metric cards (2x2 grid below the stage breakdown) ──────────────────
# Each card is a clickable View holding <value> then <label> (value is the
# preceding-sibling of the label). Tap the label to open the metric dialog.
RESTORATIVE_CARD       = (AppiumBy.XPATH, '//android.widget.TextView[@text="Restorative"]')
RESTORATIVE_CARD_VALUE = (AppiumBy.XPATH, '//android.widget.TextView[@text="Restorative"]/preceding-sibling::android.widget.TextView[1]')
LATENCY_CARD           = (AppiumBy.XPATH, '//android.widget.TextView[@text="Latency"]')
LATENCY_CARD_VALUE     = (AppiumBy.XPATH, '//android.widget.TextView[@text="Latency"]/preceding-sibling::android.widget.TextView[1]')
TOSS_CARD              = (AppiumBy.XPATH, '//android.widget.TextView[@text="Toss & Turns"]')
TOSS_CARD_VALUE        = (AppiumBy.XPATH, '//android.widget.TextView[@text="Toss & Turns"]/preceding-sibling::android.widget.TextView[1]')
MIDPOINT_CARD          = (AppiumBy.XPATH, '//android.widget.TextView[@text="Midpoint"]')
MIDPOINT_CARD_VALUE    = (AppiumBy.XPATH, '//android.widget.TextView[@text="Midpoint"]/preceding-sibling::android.widget.TextView[1]')

# ── Metric dialog (bottom sheet; identical layout for all four) ──────────────
# Reached by tapping a card, then swiping right->left to page between metrics
# (Restorative -> Sleep Latency -> Toss & Turns -> Circadian Midpoint). The hero
# "Last night" value is the sibling right after the "Last night" label — the
# same anchor works for every dialog. Tapping outside the sheet closes it.
DIALOG_LAST_NIGHT  = (AppiumBy.XPATH, '//android.widget.TextView[@text="Last night"]')
DIALOG_HERO_VALUE  = (AppiumBy.XPATH, '//android.widget.TextView[@text="Last night"]/following-sibling::android.widget.TextView[1]')

RESTORATIVE_DIALOG_TITLE = (AppiumBy.XPATH, '//android.widget.TextView[@text="Restorative Sleep"]')
LATENCY_DIALOG_TITLE     = (AppiumBy.XPATH, '//android.widget.TextView[@text="Sleep Latency"]')
TOSS_DIALOG_TITLE        = (AppiumBy.XPATH, '//android.widget.TextView[@text="Toss & Turns"]')
MIDPOINT_DIALOG_TITLE    = (AppiumBy.XPATH, '//android.widget.TextView[@text="Circadian Midpoint"]')

# Trend-graph range toggles + the average caption that proves each range plotted.
# Metric dialogs (Restorative/Latency/Toss/Midpoint) have WEEK/MONTH/6M; the
# overnight-vital dialogs additionally have DAY (DAILY AVERAGE).
RANGE_DAY   = (AppiumBy.XPATH, '//android.widget.TextView[@text="DAY"]')
RANGE_WEEK  = (AppiumBy.XPATH, '//android.widget.TextView[@text="WEEK"]')
RANGE_MONTH = (AppiumBy.XPATH, '//android.widget.TextView[@text="MONTH"]')
RANGE_6M    = (AppiumBy.XPATH, '//android.widget.TextView[@text="6M"]')
AVG_DAY     = (AppiumBy.XPATH, '//android.widget.TextView[@text="DAILY AVERAGE"]')
AVG_WEEK    = (AppiumBy.XPATH, '//android.widget.TextView[@text="WEEKLY AVERAGE"]')
AVG_MONTH   = (AppiumBy.XPATH, '//android.widget.TextView[@text="MONTHLY AVERAGE"]')
AVG_6M      = (AppiumBy.XPATH, '//android.widget.TextView[@text="6-MONTH AVERAGE"]')

# ── Overnight-vital dialogs (How your body responded) ────────────────────────
# The five vitals are clickable cards (label above, value = following-sibling).
# Tapping HRV opens a bottom-sheet, then right->left swipe pages through them:
# HRV -> Resting Heart Rate -> SpO2 -> Respiratory Rate -> Skin Temperature.
# Same DIALOG_LAST_NIGHT / DIALOG_HERO_VALUE anchors apply. Skin Temp shows no
# "last night" value ("—"), so its card-vs-dialog match is expected to differ.
HRV_DIALOG_TITLE       = (AppiumBy.XPATH, '//android.widget.TextView[@text="HRV"]')
RHR_DIALOG_TITLE       = (AppiumBy.XPATH, '//android.widget.TextView[@text="Resting Heart Rate"]')
SPO2_DIALOG_TITLE      = (AppiumBy.XPATH, '//android.widget.TextView[contains(@text,"SpO")]')
RESP_DIALOG_TITLE      = (AppiumBy.XPATH, '//android.widget.TextView[@text="Respiratory Rate"]')
SKIN_TEMP_DIALOG_TITLE = (AppiumBy.XPATH, '//android.widget.TextView[@text="Skin Temperature"]')

# The Skin Temperature dialog has NO trend graph / range toggles and no
# "last night" value ("—"); instead it shows explanatory sections. Verify one
# of those (guidance) rather than a value-match / DAY-WEEK-MONTH-6M graphs.
SKIN_TEMP_GUIDANCE = (AppiumBy.XPATH, '//android.widget.TextView[@text="HOW LUNA REPORTS IT"]')
