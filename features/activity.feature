Feature: Activity Module
    As a user I want to view my activity data
    So that I can track my activity score, goal progress, calories, steps and distance.


  Background:
    Given the user accepts the notifications pop-up


  @activity
  Scenario: View all activity details
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
