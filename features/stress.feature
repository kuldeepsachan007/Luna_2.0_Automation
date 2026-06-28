Feature: Luna 2.0 Stress details
    As a Luna user
    I want to open the Stress detail page from the Health page
    So that I can review my stress for the day.


  @stress
  Scenario: View Stress details from the Health page
    Given the user is on the Home page
    When the user opens the Health page
    And the user goes to the previous day
    And the user scrolls to the Stress card
    And the user opens the Stress card
    Then the Stress detail page is shown
    And the Max, Min and Avg values are shown
    When the user scrolls to the stress stages
    Then the Relaxed, Focused and Stressed stages are shown
    And the stress graph is plotted for the day
    And the sum of the stage durations equals the total duration
    When the user taps the Stressed stage again to restore the view
    And the user scrolls so the Stress trends section is at the top
    Then the WEEK, MONTH and 6 MONTHS stress trends graphs are plotted
    And the today stress comparison is shown
    When the user switches to the Non-activity comparison
    Then the Non-activity stress comparison is shown
    When the user taps the back arrow
    Then the Health page is shown
