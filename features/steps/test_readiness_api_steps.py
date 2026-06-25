import pytest
from pytest_bdd import step, scenarios, parsers
from utility.api.readiness_api import ReadinessAPI
from utility.liberaries.decorators import logger

# Valid token - update this when it expires
VALID_TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo3NzkwMDksImRldmljZV9pZCI6MSwibXVsdGlMb2dpbiI6ZmFsc2UsImlhdCI6MTc3NDI1MjY1OSwiZXhwIjoxNzc0MjY3MDU5fQ.aU1c6FAnxcqDNZy0sq9ydSvCRl7mnPeQjdf01an-RS4"


@pytest.fixture
def readiness_api():
    """Readiness API instance holder"""
    return {}


# ============ SETUP STEPS ============

@step('the readiness API is configured with valid token')
def configure_valid_token(readiness_api):
    logger.info("Configuring readiness API with valid token")
    readiness_api["client"] = ReadinessAPI(access_token=VALID_TOKEN)


@step('the readiness API is configured with invalid token')
def configure_invalid_token(readiness_api):
    logger.info("Configuring readiness API with invalid token")
    readiness_api["client"] = ReadinessAPI(access_token="invalid_token_123")


# ============ ACTION STEPS ============

@step('the user fetches readiness details')
def fetch_readiness_details(readiness_api):
    logger.info("Fetching readiness details")
    response = readiness_api["client"].get_readiness_details()
    readiness_api["response"] = response
    readiness_api["json"] = response.json()
    logger.info(f"Response status: {response.status_code}")


@step(parsers.parse('the user fetches readiness health data for "{date}"'))
def fetch_readiness_health_data(readiness_api, date):
    logger.info(f"Fetching readiness health data for {date}")
    response = readiness_api["client"].get_readiness_health_data(date)
    readiness_api["health_response"] = response
    readiness_api["health_json"] = response.json()
    logger.info(f"Response status: {response.status_code}")


# ============ DETAILS API VERIFICATION STEPS ============

@step('the readiness API response status code should be 200')
def verify_status_200(readiness_api):
    assert readiness_api["response"].status_code == 200, \
        f"Expected 200 but got {readiness_api['response'].status_code}"
    logger.info("Readiness API status code is 200")


@step('the readiness health API response should not be 200')
def verify_health_status_not_200(readiness_api):
    assert readiness_api["health_response"].status_code != 200, \
        f"Expected non-200 but got {readiness_api['health_response'].status_code}"
    logger.info(f"Health API status code is {readiness_api['health_response'].status_code}")


@step('the readiness API response should have success as true')
def verify_success_true(readiness_api):
    data = readiness_api["json"]
    assert data.get("success") is True, f"Expected success=true but got {data.get('success')}"
    logger.info("Readiness API response success is true")


@step('the readiness score description should be present')
def verify_readiness_score_desc(readiness_api):
    data = readiness_api["json"]["data"]
    assert "readiness_score" in data, "readiness_score description not found"
    assert len(data["readiness_score"]) > 0, "readiness_score description is empty"
    logger.info("Readiness score description is present")


@step('the resting heart rate description should be present')
def verify_rhr_desc(readiness_api):
    data = readiness_api["json"]["data"]
    assert "resting_hr" in data, "resting_hr description not found"
    assert len(data["resting_hr"]) > 0, "resting_hr description is empty"
    logger.info("Resting heart rate description is present")


@step('the HRV description should be present')
def verify_hrv_desc(readiness_api):
    data = readiness_api["json"]["data"]
    assert "hrv" in data, "hrv description not found"
    assert len(data["hrv"]) > 0, "hrv description is empty"
    logger.info("HRV description is present")


@step('the skin temperature description should be present')
def verify_skin_temp_desc(readiness_api):
    data = readiness_api["json"]["data"]
    assert "avg_temp" in data, "avg_temp (skin temperature) description not found"
    assert len(data["avg_temp"]) > 0, "avg_temp description is empty"
    logger.info("Skin temperature description is present")


@step('the respiratory rate description should be present')
def verify_resp_desc(readiness_api):
    data = readiness_api["json"]["data"]
    assert "respiration" in data, "respiration description not found"
    assert len(data["respiration"]) > 0, "respiration description is empty"
    logger.info("Respiratory rate description is present")


# ============ HEALTH TREND (ACTUAL VALUES) STEPS ============

@step('the readiness health API response should be 200')
def verify_health_status_200(readiness_api):
    assert readiness_api["health_response"].status_code == 200, \
        f"Expected 200 but got {readiness_api['health_response'].status_code}"
    logger.info("Health API status code is 200")


@step('the resting heart rate value should be present')
def verify_rhr_value(readiness_api):
    result = readiness_api["health_json"]["data"]["result"][0]
    trend = result["health_trend"]
    assert "rhr" in trend, "rhr not found in health_trend"
    assert trend["rhr"]["value"] is not None, "RHR value is None"
    logger.info(f"Resting Heart Rate: {trend['rhr']['value']} bpm ({trend['rhr']['text']})")


@step(parsers.parse('the resting heart rate status should be one of "{statuses}"'))
def verify_rhr_status(readiness_api, statuses):
    result = readiness_api["health_json"]["data"]["result"][0]
    status = result["health_trend"]["rhr"]["status"]
    valid = [s.strip() for s in statuses.split(",")]
    assert status in valid, f"RHR status '{status}' not in {valid}"
    logger.info(f"Resting Heart Rate status: {status}")


@step('the HRV value should be present')
def verify_hrv_value(readiness_api):
    result = readiness_api["health_json"]["data"]["result"][0]
    trend = result["health_trend"]
    assert "hrv" in trend, "hrv not found in health_trend"
    assert trend["hrv"]["value"] is not None, "HRV value is None"
    logger.info(f"HRV: {trend['hrv']['value']} ms ({trend['hrv']['text']})")


@step(parsers.parse('the HRV status should be one of "{statuses}"'))
def verify_hrv_status(readiness_api, statuses):
    result = readiness_api["health_json"]["data"]["result"][0]
    status = result["health_trend"]["hrv"]["status"]
    valid = [s.strip() for s in statuses.split(",")]
    assert status in valid, f"HRV status '{status}' not in {valid}"
    logger.info(f"HRV status: {status}")


@step('the skin temperature value should be present')
def verify_skin_temp_value(readiness_api):
    result = readiness_api["health_json"]["data"]["result"][0]
    trend = result["health_trend"]
    assert "skin_temp" in trend, "skin_temp not found in health_trend"
    assert trend["skin_temp"]["value"] is not None, "Skin temp value is None"
    logger.info(f"Skin Temperature: {trend['skin_temp']['value']} ({trend['skin_temp']['text']})")


@step(parsers.parse('the skin temperature status should be one of "{statuses}"'))
def verify_skin_temp_status(readiness_api, statuses):
    result = readiness_api["health_json"]["data"]["result"][0]
    status = result["health_trend"]["skin_temp"]["status"]
    valid = [s.strip() for s in statuses.split(",")]
    assert status in valid, f"Skin temp status '{status}' not in {valid}"
    logger.info(f"Skin Temperature status: {status}")


@step('the respiratory rate value should be present')
def verify_resp_value(readiness_api):
    result = readiness_api["health_json"]["data"]["result"][0]
    trend = result["health_trend"]
    assert "resp" in trend, "resp not found in health_trend"
    assert trend["resp"]["value"] is not None, "Respiratory rate value is None"
    logger.info(f"Respiratory Rate: {trend['resp']['value']} rpm ({trend['resp']['text']})")


@step(parsers.parse('the respiratory rate status should be one of "{statuses}"'))
def verify_resp_status(readiness_api, statuses):
    result = readiness_api["health_json"]["data"]["result"][0]
    status = result["health_trend"]["resp"]["status"]
    valid = [s.strip() for s in statuses.split(",")]
    assert status in valid, f"Respiratory rate status '{status}' not in {valid}"
    logger.info(f"Respiratory Rate status: {status}")


# scenarios() at bottom
scenarios("../readiness_api.feature")
