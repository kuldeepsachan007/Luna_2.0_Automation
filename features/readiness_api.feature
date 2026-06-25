Feature: Readiness API Testing
    As a tester I want to verify the Readiness API
    So that I can ensure readiness data is returned correctly from the backend.


  @api @readiness_api
  Scenario: Verify readiness details API returns valid response
    Given the readiness API is configured with valid token
    When the user fetches readiness details
    Then the readiness API response status code should be 200
    And the readiness API response should have success as true
    And the readiness score description should be present
    And the resting heart rate description should be present
    And the HRV description should be present
    And the skin temperature description should be present
    And the respiratory rate description should be present


  @api @readiness_api
  Scenario: Verify Resting Heart Rate data from health trend
    Given the readiness API is configured with valid token
    When the user fetches readiness health data for "2026-03-30"
    Then the readiness health API response should be 200
    And the resting heart rate value should be present
    And the resting heart rate status should be one of "optimal,warning,poor"


  @api @readiness_api
  Scenario: Verify HRV data from health trend
    Given the readiness API is configured with valid token
    When the user fetches readiness health data for "2026-03-30"
    Then the readiness health API response should be 200
    And the HRV value should be present
    And the HRV status should be one of "optimal,warning,poor"


  @api @readiness_api
  Scenario: Verify Skin Temperature data from health trend
    Given the readiness API is configured with valid token
    When the user fetches readiness health data for "2026-03-30"
    Then the readiness health API response should be 200
    And the skin temperature value should be present
    And the skin temperature status should be one of "optimal,warning,poor,fair"


  @api @readiness_api
  Scenario: Verify Respiratory Rate data from health trend
    Given the readiness API is configured with valid token
    When the user fetches readiness health data for "2026-03-30"
    Then the readiness health API response should be 200
    And the respiratory rate value should be present
    And the respiratory rate status should be one of "optimal,warning,poor"


  @api @readiness_api
  Scenario: Verify readiness health API with invalid token returns error
    Given the readiness API is configured with invalid token
    When the user fetches readiness health data for "2026-03-30"
    Then the readiness health API response should not be 200
