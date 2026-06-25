import warnings
import pytest
from pytest_bdd import step, scenarios, parsers
from utility.api.activity_api import ActivityAPI
from utility.liberaries.decorators import logger

# Valid token - update this when it expires
VALID_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo3NzkwMDksImRldmljZV9pZCI6MSwibXVsdGlMb2dpbiI6ZmFsc2UsImlhdCI6MTc3NDg3MTY3NiwiZXhwIjoxNzc0ODg2MDc2fQ.u7SIss47Ge_PQVhCnEI0eIBXnqIjqH4xBNLYiGhiScc"


@pytest.fixture
def activity_api():
    """Activity API instance holder"""
    return {}


# ============ SETUP STEPS ============

@step('the activity API is configured with valid token')
def configure_valid_token(activity_api):
    logger.info("Configuring activity API with valid token")
    activity_api["client"] = ActivityAPI(access_token=VALID_TOKEN)


@step('the activity API is configured with invalid token')
def configure_invalid_token(activity_api):
    logger.info("Configuring activity API with invalid token")
    activity_api["client"] = ActivityAPI(access_token="invalid_token_123")


# ============ ACTION STEPS ============

@step(parsers.parse('the user fetches activity data for "{date}"'))
def fetch_activity_data(activity_api, date):
    logger.info(f"Fetching activity data for {date}")
    response = activity_api["client"].get_activity_goals(date)
    activity_api["response"] = response
    activity_api["json"] = response.json()
    logger.info(f"Response status: {response.status_code}")


# ============ VERIFICATION STEPS ============

@step('the activity API response status code should be 200')
def verify_status_200(activity_api):
    assert activity_api["response"].status_code == 200, \
        f"Expected 200 but got {activity_api['response'].status_code}"
    status = activity_api["response"].status_code
    data = activity_api["json"]["data"]
    msg = f"Status: {status} | Steps: {data.get('steps')}/{data.get('steps_required')} | Calories: {data.get('calorie')}/{data.get('calorie_required')} | Distance: {data.get('distance')}m/{data.get('distance_required')}m | Hydration: {data.get('hydration')}ml/{data.get('hydration_required')}ml"
    warnings.warn(f"\n{'='*50}\nACTIVITY API DATA: {msg}\n{'='*50}", UserWarning)


@step('the activity API response status code should not be 200')
def verify_status_not_200(activity_api):
    assert activity_api["response"].status_code != 200, \
        f"Expected non-200 but got {activity_api['response'].status_code}"
    logger.info(f"Activity API status code is {activity_api['response'].status_code}")


@step('the activity API response should have success as true')
def verify_success_true(activity_api):
    data = activity_api["json"]
    assert data.get("success") is True, f"Expected success=true but got {data.get('success')}"
    logger.info("Activity API response success is true")


# ============ STEPS DATA ============

@step('the steps data should be present')
def verify_steps_present(activity_api):
    data = activity_api["json"]["data"]
    assert "steps" in data, "steps not found in response"
    assert "steps_required" in data, "steps_required not found in response"
    logger.info(f"Steps: {data['steps']} / {data['steps_required']}")


@step('the steps value should be greater than or equal to 0')
def verify_steps_value(activity_api):
    value = activity_api["json"]["data"]["steps"]
    assert value >= 0, f"Steps value {value} is not >= 0"
    logger.info(f"Steps: {value}")


@step('the steps required goal should be greater than 0')
def verify_steps_goal(activity_api):
    value = activity_api["json"]["data"]["steps_required"]
    assert value > 0, f"Steps required {value} is not > 0"
    logger.info(f"Steps goal: {value}")


# ============ CALORIE DATA ============

@step('the calorie data should be present')
def verify_calorie_present(activity_api):
    data = activity_api["json"]["data"]
    assert "calorie" in data, "calorie not found in response"
    assert "calorie_required" in data, "calorie_required not found in response"
    logger.info(f"Calories: {data['calorie']} / {data['calorie_required']}")


@step('the calorie value should be greater than or equal to 0')
def verify_calorie_value(activity_api):
    value = activity_api["json"]["data"]["calorie"]
    assert value >= 0, f"Calorie value {value} is not >= 0"
    logger.info(f"Calories: {value}")


@step('the calorie required goal should be greater than 0')
def verify_calorie_goal(activity_api):
    value = activity_api["json"]["data"]["calorie_required"]
    assert value > 0, f"Calorie required {value} is not > 0"
    logger.info(f"Calorie goal: {value}")


# ============ DISTANCE DATA ============

@step('the distance data should be present')
def verify_distance_present(activity_api):
    data = activity_api["json"]["data"]
    assert "distance" in data, "distance not found in response"
    assert "distance_required" in data, "distance_required not found in response"
    logger.info(f"Distance: {data['distance']}m / {data['distance_required']}m")


@step('the distance value should be greater than or equal to 0')
def verify_distance_value(activity_api):
    value = activity_api["json"]["data"]["distance"]
    assert value >= 0, f"Distance value {value} is not >= 0"
    logger.info(f"Distance: {value}m")


@step('the distance required goal should be greater than 0')
def verify_distance_goal(activity_api):
    value = activity_api["json"]["data"]["distance_required"]
    assert value > 0, f"Distance required {value} is not > 0"
    logger.info(f"Distance goal: {value}m")


# scenarios() at bottom
scenarios("../activity_api.feature")
