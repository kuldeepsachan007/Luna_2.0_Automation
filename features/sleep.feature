Feature: Luna 2.0 Sleep details
    As a Luna user
    I want to open the Sleep detail page from the Health page
    So that I can review my sleep for the night.


  @sleep
  Scenario: View Sleep details from the Health page
    Given the user is on the Home page
    When the user opens the Health page
    And the user goes to the stable date
    And the user opens the Sleep card
    Then the Sleep detail page is shown
    And the sleep summary values are shown
    And the sleep window and efficiency are shown
    And the sleep timing matches the total sleep duration
    And the sleep deficit equals sleep needed minus actual sleep
    When the user scrolls to the sleep stages
    Then the sleep stage legend is shown
    And the sleep hypnogram is plotted
    When the user taps each sleep stage and collects its value
    Then the sleep stage breakdown percentages sum to about 100
    Then the sleep metric cards open dialogs with matching values and week month 6M graphs
    When the user scrolls to how the body responded
    Then the overnight vitals are shown
    Then the overnight vital cards open dialogs with matching values and day week month 6M graphs
    When the user taps the back arrow
    Then the Health page is shown
    When the user returns to the Home page
    Then the sleep check summary is reported
