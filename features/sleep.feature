Feature: Sleep Module
  As a Luna Ring user I want to view and track my sleep data
  So that I can monitor my sleep health and improve my sleep quality.

  Background:
    Given the user accepts the notifications pop-up
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
    Then near by luna rings shoudld be detected and displayed
    When user selects the luna ring 
    Then pairing should start 
    And user verifies the mac address of the ring is correct
    When user clicks on the Get started button
    Then user lands on the home page screen
    Given the user taps on the sleep button

  @sleep @sleep_overview
  Scenario: View sleep overview on home screen
    Then the user should see the sleep score on the home screen
    And the user should see the sleep duration on the home screen

  @sleep @sleep_detail
  Scenario: View detailed sleep analysis
    When the user taps on the sleep card
    Then the user should be navigated to the sleep detail screen
    And the user should see the total sleep duration
    And the user should see the sleep score
    And the user should see the sleep stages breakdown

  @sleep @sleep_stages
  Scenario: Verify sleep stages data
    When the user taps on the sleep card
    Then the user should be navigated to the sleep detail screen
    And the user should see the deep sleep duration
    And the user should see the light sleep duration
    And the user should see the REM sleep duration
    And the user should see the awake time duration

  @sleep @sleep_heart_rate
  Scenario: Verify heart rate during sleep
    When the user taps on the sleep card
    Then the user should be navigated to the sleep detail screen
    When the user scrolls down to the heart rate section
    Then the user should see the average heart rate during sleep
    And the user should see the minimum heart rate during sleep
    And the user should see the maximum heart rate during sleep

  @sleep @sleep_spo2
  Scenario: Verify blood oxygen level during sleep
    When the user taps on the sleep card
    Then the user should be navigated to the sleep detail screen
    When the user scrolls down to the blood oxygen section
    Then the user should see the average SpO2 level during sleep

  @sleep @sleep_history
  Scenario: View sleep history and trends
    When the user taps on the sleep card
    Then the user should be navigated to the sleep detail screen
    When the user scrolls down to the sleep history section
    Then the user should see the weekly sleep trend chart
    And the user should see the average weekly sleep duration

  @sleep @sleep_tips
  Scenario: View sleep tips and recommendations
    When the user taps on the sleep card
    Then the user should be navigated to the sleep detail screen
    When the user scrolls down to the sleep tips section
    Then the user should see at least one sleep recommendation

  @sleep @sleep_navigation
  Scenario: Navigate back from sleep detail to home screen
    When the user taps on the sleep card
    Then the user should be navigated to the sleep detail screen
    When the user taps the back button on the sleep detail screen
    Then the user should be navigated back to the home screen

  @sleep @sleep_date_navigation
  Scenario Outline: Navigate to a previous night's sleep data
    When the user taps on the sleep card
    Then the user should be navigated to the sleep detail screen
    When the user navigates to the <direction> sleep record
    Then the user should see the sleep data for the <direction> day

    Examples:
      | direction |
      | previous  |
      | next      |
