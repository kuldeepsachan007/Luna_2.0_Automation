Feature: Activity API Testing
    As a tester I want to verify the Activity API
    So that I can ensure activity data is returned correctly from the backend.


  @api @activity_api
  Scenario: Verify activity API returns valid data
    Given the activity API is configured with valid token
    When the user fetches activity data for "2026-03-30"
    Then the activity API response status code should be 200
    And the activity API response should have success as true
    And the steps data should be present
    And the calorie data should be present
    And the distance data should be present


  @api @activity_api
  Scenario: Verify activity score and goal progress
    Given the activity API is configured with valid token
    When the user fetches activity data for "2026-03-30"
    Then the steps value should be greater than or equal to 0
    And the steps required goal should be greater than 0
    And the calorie value should be greater than or equal to 0
    And the calorie required goal should be greater than 0
    And the distance value should be greater than or equal to 0
    And the distance required goal should be greater than 0


  @api @activity_api
  Scenario: Verify total calories data
    Given the activity API is configured with valid token
    When the user fetches activity data for "2026-03-30"
    Then the calorie value should be greater than or equal to 0
    And the calorie required goal should be greater than 0


  @api @activity_api
  Scenario: Verify steps data
    Given the activity API is configured with valid token
    When the user fetches activity data for "2026-03-30"
    Then the steps value should be greater than or equal to 0
    And the steps required goal should be greater than 0


  @api @activity_api
  Scenario: Verify distance data
    Given the activity API is configured with valid token
    When the user fetches activity data for "2026-03-30"
    Then the distance value should be greater than or equal to 0
    And the distance required goal should be greater than 0


  @api @activity_api
  Scenario: Verify activity API with invalid token returns error
    Given the activity API is configured with invalid token
    When the user fetches activity data for "2026-03-30"
    Then the activity API response status code should not be 200
