Feature: Sleep API Testing
    As a tester I want to verify the Sleep API
    So that I can ensure sleep data is returned correctly from the backend.


  @api @sleep_api
  Scenario: Verify sleep API returns valid data for 23 March
    Given the sleep API is configured with valid token
    When the user fetches sleep data for "2026-03-30"
    Then the API response status code should be 200
    And the API response should have success as true
    And the sleep score should be present
    And the sleep duration should be present
    And the REM sleep data should be present
    And the deep sleep data should be present
    And the efficiency data should be present
    And the latency data should be present
    And the restfulness data should be present
    And the health trend data should be present


  @api @sleep_api
  Scenario: Verify sleep API returns correct sleep score status
    Given the sleep API is configured with valid token
    When the user fetches sleep data for "2026-03-30"
    Then the sleep score value should be between 0 and 100
    And the sleep score status should be one of "poor,fair,good,excellent,warning"


  @api @sleep_api
  Scenario: Verify REM sleep contributor data
    Given the sleep API is configured with valid token
    When the user fetches sleep data for "2026-03-30"
    Then the REM sleep value should be greater than 0
    And the REM sleep status should be one of "optimal,warning,poor"


  @api @sleep_api
  Scenario: Verify Deep sleep contributor data
    Given the sleep API is configured with valid token
    When the user fetches sleep data for "2026-03-30"
    Then the deep sleep value should be greater than 0
    And the deep sleep status should be one of "optimal,warning,poor"


  @api @sleep_api
  Scenario: Verify Efficiency contributor data
    Given the sleep API is configured with valid token
    When the user fetches sleep data for "2026-03-30"
    Then the efficiency value should be between 0 and 100
    And the efficiency status should be one of "optimal,warning,poor"


  @api @sleep_api
  Scenario: Verify Sleep duration contributor data
    Given the sleep API is configured with valid token
    When the user fetches sleep data for "2026-03-30"
    Then the sleep duration value should be greater than 0
    And the sleep duration status should be one of "optimal,warning,poor"


  @api @sleep_api
  Scenario: Verify Latency contributor data
    Given the sleep API is configured with valid token
    When the user fetches sleep data for "2026-03-30"
    Then the latency value should be greater than or equal to 0
    And the latency status should be one of "optimal,warning,poor"


  @api @sleep_api
  Scenario: Verify Restfulness contributor data
    Given the sleep API is configured with valid token
    When the user fetches sleep data for "2026-03-30"
    Then the restfulness value should be greater than or equal to 0
    And the restfulness status should be one of "optimal,warning,poor"


  @api @sleep_api
  Scenario: Verify Circadian mid-point data
    Given the sleep API is configured with valid token
    When the user fetches sleep data for "2026-03-30"
    Then the circadian mid-point value should be present
    And the circadian mid-point status should be one of "optimal,warning,poor"


  @api @sleep_api
  Scenario: Verify sleep API with invalid date returns error
    Given the sleep API is configured with valid token
    When the user fetches sleep data for "2099-01-01"
    Then the API response status code should not be 200


  @api @sleep_api
  Scenario: Verify sleep API with invalid token returns error
    Given the sleep API is configured with invalid token
    When the user fetches sleep data for "2026-03-30"
    Then the API response status code should not be 200
