Feature: Luna 2.0 Heart Rate details
    As a Luna user
    I want to open the Heart Rate detail page from the Home page
    So that I can review my heart-rate graph and the Sleep HR breakdown.


  @heart_rate
  Scenario: View Heart Rate details and Sleep HR breakdown from Home
    Given the user is on the Home page
    When the user opens the Health page
    And the user goes to the previous day
    And the user opens the Heart Rate card
    Then the Heart Rate detail page is shown for the current date
    And a heart rate graph is plotted for the day
    When the user expands the Sleep HR section
    And the user scrolls until the Sleep HR to Workout HR area is visible
    Then the RHR, AVG Sleep HR and Time to Low details are shown

    When the user opens the RHR card
    Then the Resting Heart Rate dialog is shown
    And the dialog value matches the RHR card value
    And the weekly heart rate graph is plotted
    When the user selects the Month view
    Then the monthly heart rate graph is plotted
    When the user selects the 6 Month view
    Then the 6 month heart rate graph is plotted
    When the user closes the Resting Heart Rate dialog
    Then the Resting Heart Rate dialog is closed

    When the user opens the AVG Sleep HR card
    Then the Avg Sleep Heart Rate dialog is shown
    And the dialog value matches the AVG Sleep HR card value
    And the weekly heart rate graph is plotted
    When the user selects the Month view
    Then the monthly heart rate graph is plotted
    When the user selects the 6 Month view
    Then the 6 month heart rate graph is plotted
    When the user closes the Avg Sleep Heart Rate dialog
    Then the Avg Sleep Heart Rate dialog is closed

    When the user opens the TIME TO LOW card
    Then the Time to Lowest HR dialog is shown
    And the dialog value matches the TIME TO LOW card value
    And the weekly heart rate graph is plotted
    When the user selects the Month view
    Then the monthly heart rate graph is plotted
    When the user selects the 6 Month view
    Then the 6 month heart rate graph is plotted
    When the user closes the Time to Lowest HR dialog
    Then the Time to Lowest HR dialog is closed

    When the user minimises the Sleep HR section
    Then the Sleep HR section is collapsed
    When the user expands the Workout HR section
    Then the Workout HR section is expanded
    When the user minimises the Workout HR section
    Then the Workout HR section is collapsed

    When the user expands the Idle HR section
    Then the Idle HR section is expanded
    When the user opens the Inactive Avg card
    Then the Inactive Avg HR dialog is shown
    And the dialog value matches the Inactive Avg card value
    And the weekly heart rate graph is plotted
    When the user selects the Month view
    Then the monthly heart rate graph is plotted
    When the user selects the 6 Month view
    Then the 6 month heart rate graph is plotted
    When the user closes the Inactive Avg HR dialog
    Then the Inactive Avg HR dialog is closed
    When the user opens the Lowest Waking card
    Then the Lowest Waking HR dialog is shown
    And the dialog value matches the Lowest Waking card value
    And the weekly heart rate graph is plotted
    When the user selects the Month view
    Then the monthly heart rate graph is plotted
    When the user selects the 6 Month view
    Then the 6 month heart rate graph is plotted
    When the user closes the Lowest Waking HR dialog
    Then the Lowest Waking HR dialog is closed
    When the user minimises the Idle HR section
    Then the Idle HR section is collapsed

    When the user goes back from the Heart Rate page
    Then the Health page is shown
