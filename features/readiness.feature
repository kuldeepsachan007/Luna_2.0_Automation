Feature: Readiness Module
    As a user I want to view my readiness data
    So that I can track my readiness score, resting heart rate, HRV, skin temperature and respiratory rate.


  Background:
    Given the user accepts the notifications pop-up


  @readiness
  Scenario: View all readiness details
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
