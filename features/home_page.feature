Feature: Home Page Elements
    As a user I want to view all elements on the home page
    So that I can track my health data.


  Background:
    Given the user accepts the notifications pop-up
    And the user enters valid email id and otp
        |email|
        |kuldeep.sachan@nexxbase.com|
    And clicks the otp continue button
    Then user asked to select the language
    When user selects the language and clicks on continue button
    Then user should be asked to connect the Luna Ring
    When user click on search now button
    Then user should be asked to allow to access location permission
    And user grands the location access
    And the user waits for 30 seconds for search
    Then near by luna rings shoudld be detected and displayed
    When user selects the luna ring
    Then pairing should start
    And user verifies the mac address of the ring is correct
    When user clicks on the Get started button
    Then user lands on the home page screen


  @circadian
  Scenario: View Circadian Alignment details
    When scrolls up to find the Circadian Alignment card
    And clicks on the Circadian Alignment arrow button
    Then the Circadian Alignment page is displayed
    When the user clicks back from Circadian Alignment page
    Then the user is back on the home page

  @home_activity
  Scenario: View all activity details via home page Activity card
    When scrolls to find the Activity card on home page
    And clicks on the Activity arrow button on home page
    And clicks on activity get started button
    And clicks on Activity Score
    Then the Activity Score page is displayed
    When the user clicks back arrow button
    And clicks on Goal Progress
    Then the Goal Progress page is displayed
    When the user clicks back arrow button
    And clicks on Total Calories
    Then the Total Calories page is displayed
    When the user clicks back arrow button
    And clicks on Steps
    Then the Steps page is displayed
    When the user clicks back arrow button
    And clicks on Distance
    Then the Distance page is displayed
    When the user clicks back arrow button
    Then the user is back on the activity page

  @one_tap_vitals
  Scenario: Measure all vitals using One Tap Vitals feature
    When the user scrolls to find One Tap Vitals on home page
    Then the One Tap Vitals section should be displayed
    And the user waits 10 seconds before starting vitals measurement
    When the user taps on Heart Rate
    Then the user waits 40 seconds for Heart Rate reading
    When the user taps on Stress
    Then the user waits 40 seconds for Stress reading
    When the user taps on SpO2
    Then the user waits 60 seconds for SpO2 reading
    When the user taps on Skin Temperature
    Then the user waits 40 seconds for Skin Temperature reading

  # ── Add new home page element scenarios below ────────────────────────────────
