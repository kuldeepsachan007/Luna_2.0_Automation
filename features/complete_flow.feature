Feature: Complete Flow - Sleep, Activity and Readiness
    As a user I want to test all modules in a single session
    So that Login happens once and Sleep, Activity and Readiness are tested together.


  Background:
    Given the user accepts the notifications pop-up


  @complete_flow
  Scenario: Complete flow - Login then Sleep then Activity then Readiness
    # ============ LOGIN ============
    Given the user enters valid email id and otp
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
    And the user waits for 30 seconds for pairing
    When user clicks on the Get started button
    Then user lands on the home page screen

    # ============ SLEEP MODULE ============
    When the user clicks on the sleep button
    And selects the date 23 March
    And clicks on REM sleep
    Then the REM sleep trends view page is displayed
    When the user clicks back button from trends view
    And scrolls up from REM sleep to dates to reveal Deep sleep and Efficiency
    And clicks on Deep sleep
    Then the Deep sleep trends view page is displayed
    When the user clicks back button from trends view
    And clicks on Efficiency
    Then the Efficiency trends view page is displayed
    When the user clicks back button from trends view
    And the user clicks on the arrow down button
    And clicks on Sleep duration
    Then the Sleep duration trends view page is displayed
    When the user clicks back button from trends view
    And the user clicks on the arrow down button
    And clicks on Latency
    Then the Latency trends view page is displayed
    When the user clicks back button from trends view
    And the user clicks on the arrow down button
    And clicks on Restfulness
    Then the Restfulness trends view page is displayed
    When the user clicks back button from trends view
    And the user clicks on the arrow down button
    And clicks on Circadian mid-point
    Then the Circadian mid-point trends view page is displayed
    When the user clicks back button from trends view
    And the user clicks on Respiratory Rate
    Then the Respiratory Rate trends view page is displayed
    When the user clicks back button from trends view
    Then the user is back on the sleep details page

    # ============ ACTIVITY MODULE ============
    When the user clicks on the activity button
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

    # ============ READINESS MODULE ============
    When the user clicks on the readiness button
    And clicks on readiness get started button
    And clicks on Readiness Score
    Then the Readiness Score page is displayed
    When the user clicks readiness back button
    And clicks on Resting Heart Rate
    Then the Resting Heart Rate trends view page is displayed
    When the user clicks readiness back button
    And clicks on HRV
    Then the HRV trends view page is displayed
    When the user clicks readiness back button
    And clicks on Skin Temperature
    Then the Skin Temperature trends view page is displayed
    When the user clicks readiness back button
    And clicks on Respiratory Rate
    Then the Readiness Respiratory Rate trends view page is displayed
    When the user clicks readiness back button
    Then the user is back on the readiness page
