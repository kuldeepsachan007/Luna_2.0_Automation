Feature: Luna 2.0 Heart Rate details
    As a Luna user
    I want to open the Heart Rate detail page from the Home page
    So that I can review my heart-rate graph and the Sleep HR breakdown.


  @heart_rate
  Scenario: View Heart Rate details and Sleep HR breakdown from Home
    Given the user is on the Home page
    When the user opens the Health page
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
