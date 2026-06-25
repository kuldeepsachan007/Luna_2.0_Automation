Feature: Luna 2.0 Health Page
    As a Luna user
    I want to view my vitals (Heart Rate, Stress, SpO2, Skin Temp) and
    Sleep summary on the Health page
    So that I can spot-check my biometrics and trigger on-demand measurements.


  Background:
    Given the user has signed in and paired the Luna ring
    And the user lands on the Health page


  # ── Combined flow for SpO2 + Stress (Heart Rate / Skin Temp coming later) ──
  #
  # For each vital:
  #   1. Tap MEASURE on the tile → popup opens.
  #   2. Wait 60s for the reading.
  #   3. If "Couldn't get a reading" appears → tap Try Again (same button
  #      position as Done). One retry. If it fails again → tap Close (X)
  #      and move on. If it succeeds → tap Done.
  #   4. Move to the next vital.
  #
  # Both vitals are exercised in a SINGLE Appium session so the app does
  # not relaunch between measurements.
  
  @smoke @vitals_full
  Scenario: Measure SpO2 and Stress one after another
    Then the SpO2 tile should be visible
    When the user measures SpO2 with retry on failure
    Then the user should be back on the Health page

    Then the Stress tile should be visible
    When the user measures Stress with retry on failure
    Then the user should be back on the Health page


  # ── COMPLETE end-to-end flow (everything in one test) ─────────────────────
  # SpO2 → Stress → Heart Rate → Skin Temp (measure + verify each reading on
  # its tile) → Sleep card (open & return) → Heart Rate card (scroll, verify
  # the card value matches the Heart Rate page). All steps run one after
  # another in a single Appium session.
  @health @full_flow
  Scenario: Full Health page flow end to end
    # 1) SpO2
    Then the SpO2 tile should be visible
    When the user measures SpO2 with retry on failure
    Then the SpO2 reading should match the value on the tile

    # 2) Stress
    Then the Stress tile should be visible
    When the user measures Stress with retry on failure
    Then the Stress reading should match the value on the tile

    # 3) Heart Rate (tile)
    Then the Heart Rate tile should be visible
    When the user measures Heart Rate with retry on failure
    Then the Heart Rate reading should match the value on the tile

    # 4) Skin Temp
    Then the Skin Temp tile should be visible
    When the user measures Skin Temp with retry on failure
    Then the Skin Temp reading should match the value on the tile

    # 5) Sleep card → Sleep page → back
    Then the Sleep card should be visible
    When the user opens the Sleep card
    Then the Sleep page should be displayed
    When the user goes back to the Health page
    Then the user should be back on the Health page

    # 6) Heart Rate card → Heart Rate page (verify value) → back
    When the user scrolls to the Heart Rate card
    And the user notes the Heart Rate card value
    And the user opens the Heart Rate card
    Then the Heart Rate page should be displayed
    And the Heart Rate page value should match the card value
    When the user goes back from the Heart Rate page
    Then the user should be back on the Health page


  # ── Full flow: measure all four vitals in order and verify each reading ───
  # For each vital (SpO2 → Stress → Heart Rate → Skin Temp): measure with the
  # retry flow, then confirm the value captured in the popup is the SAME value
  # now shown on that vital's Health-page tile. All four must match to pass.
  @verify_vitals
  Scenario: Measure all four vitals and verify each reading on its tile
    Then the SpO2 tile should be visible
    When the user measures SpO2 with retry on failure
    Then the SpO2 reading should match the value on the tile

    Then the Stress tile should be visible
    When the user measures Stress with retry on failure
    Then the Stress reading should match the value on the tile

    Then the Heart Rate tile should be visible
    When the user measures Heart Rate with retry on failure
    Then the Heart Rate reading should match the value on the tile

    Then the Skin Temp tile should be visible
    When the user measures Skin Temp with retry on failure
    Then the Skin Temp reading should match the value on the tile


  # ── Individual scenarios kept for targeted re-runs of a single vital ──────
  @smoke @page_render
  Scenario: Health page renders all main sections
    Then the Health page title should be visible
    And the SpO2 tile should be visible
    And the Stress tile should be visible
    And the Heart Rate tile should be visible
    And the Skin Temp tile should be visible
    And the Sleep card should be visible


  @vitals
  Scenario: Measure Heart Rate from the Health page
    Then the Heart Rate tile should be visible
    When the user measures Heart Rate with retry on failure
    Then the user should be back on the Health page


  @vitals
  Scenario: Measure Stress from the Health page
    When the user taps Measure Now on the Stress tile
    Then the Stress measurement sheet should be displayed


  @vitals
  Scenario: Measure SpO2 from the Health page
    When the user taps Measure Now on the SpO2 tile
    Then the SpO2 measurement sheet should be displayed


  @vitals
  Scenario: Measure Skin Temperature from the Health page
    Then the Skin Temp tile should be visible
    When the user measures Skin Temp with retry on failure
    Then the user should be back on the Health page


  # ── Sleep card → Sleep detail page (navigation only for now) ──────────────
  # Opens the Sleep page from the Health page's Sleep card and confirms it is
  # displayed. Value verification (Sleep card RHR/HRV == Sleep page RHR/HRV)
  # will be added once a dump with actual sleep data is available.
  @sleep_card
  Scenario: Open Sleep details from the Health page sleep card
    Then the Sleep card should be visible
    When the user opens the Sleep card
    Then the Sleep page should be displayed
    When the user goes back to the Health page
    Then the user should be back on the Health page


  # ── Heart Rate card → Heart Rate page, verify the value matches ───────────
  # Scroll to the Heart Rate card, note the value shown on it, open the card,
  # and confirm the Heart Rate page shows the same value. Then go back.
  @heart_card
  Scenario: Open Heart Rate details and verify the card value matches the page
    When the user scrolls to the Heart Rate card
    And the user notes the Heart Rate card value
    And the user opens the Heart Rate card
    Then the Heart Rate page should be displayed
    And the Heart Rate page value should match the card value
    When the user goes back from the Heart Rate page
    Then the user should be back on the Health page
