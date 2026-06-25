import pytest
from pytest_bdd import step, scenarios, parsers
from utility.api.sleep_api import SleepAPI
from utility.liberaries.decorators import logger

# Valid token - update this when it expires
VALID_TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo3NzkwMDksImRldmljZV9pZCI6MSwibXVsdGlMb2dpbiI6ZmFsc2UsImlhdCI6MTc3NDI1MjY1OSwiZXhwIjoxNzc0MjY3MDU5fQ.aU1c6FAnxcqDNZy0sq9ydSvCRl7mnPeQjdf01an-RS4"


@pytest.fixture
def sleep_api():
    """Sleep API instance holder"""
    return {}


@step('the sleep API is configured with valid token')
def configure_valid_token(sleep_api):
    logger.info("Configuring sleep API with valid token")
    sleep_api["client"] = SleepAPI(access_token=VALID_TOKEN)


@step('the sleep API is configured with invalid token')
def configure_invalid_token(sleep_api):
    logger.info("Configuring sleep API with invalid token")
    sleep_api["client"] = SleepAPI(access_token="invalid_token_123")


@step(parsers.parse('the user fetches sleep data for "{date}"'))
def fetch_sleep_data(sleep_api, date):
    logger.info(f"Fetching sleep data for {date}")
    response = sleep_api["client"].get_sleep_data(date)
    sleep_api["response"] = response
    sleep_api["json"] = response.json()
    logger.info(f"Response status: {response.status_code}")


@step('the API response status code should be 200')
def verify_status_200(sleep_api):
    assert sleep_api["response"].status_code == 200, \
        f"Expected 200 but got {sleep_api['response'].status_code}"
    logger.info("Status code is 200")


@step('the API response status code should not be 200')
def verify_status_not_200(sleep_api):
    assert sleep_api["response"].status_code != 200, \
        f"Expected non-200 but got {sleep_api['response'].status_code}"
    logger.info(f"Status code is {sleep_api['response'].status_code} (not 200)")


@step('the API response should have success as true')
def verify_success_true(sleep_api):
    data = sleep_api["json"]
    assert data.get("success") is True, f"Expected success=true but got {data.get('success')}"
    logger.info("API response success is true")


@step('the API response should have empty result')
def verify_empty_result(sleep_api):
    data = sleep_api["json"]
    result = data.get("data", {}).get("result", [])
    assert len(result) == 0, f"Expected empty result but got {len(result)} items"
    logger.info("API response has empty result")


@step('the sleep score should be present')
def verify_sleep_score_present(sleep_api):
    result = sleep_api["json"]["data"]["result"][0]
    assert "sleep_score" in result, "sleep_score not found in response"
    assert result["sleep_score"]["value"] is not None
    logger.info(f"Sleep score: {result['sleep_score']['value']} ({result['sleep_score']['text']})")


@step('the sleep duration should be present')
def verify_sleep_duration_present(sleep_api):
    result = sleep_api["json"]["data"]["result"][0]
    assert "sleep_duration" in result, "sleep_duration not found in response"
    assert result["sleep_duration"]["value"] is not None
    logger.info(f"Sleep duration: {result['sleep_duration']['value']}s ({result['sleep_duration']['text']})")


@step('the REM sleep data should be present')
def verify_rem_sleep_present(sleep_api):
    result = sleep_api["json"]["data"]["result"][0]
    assert "rem_sleep" in result, "rem_sleep not found in response"
    assert result["rem_sleep"]["value"] is not None
    logger.info(f"REM sleep: {result['rem_sleep']['value']}s ({result['rem_sleep']['text']})")


@step('the deep sleep data should be present')
def verify_deep_sleep_present(sleep_api):
    result = sleep_api["json"]["data"]["result"][0]
    assert "deep_sleep" in result, "deep_sleep not found in response"
    assert result["deep_sleep"]["value"] is not None
    logger.info(f"Deep sleep: {result['deep_sleep']['value']}s ({result['deep_sleep']['text']})")


@step('the efficiency data should be present')
def verify_efficiency_present(sleep_api):
    result = sleep_api["json"]["data"]["result"][0]
    assert "efficiency" in result, "efficiency not found in response"
    assert result["efficiency"]["value"] is not None
    logger.info(f"Efficiency: {result['efficiency']['value']}% ({result['efficiency']['text']})")


@step('the latency data should be present')
def verify_latency_present(sleep_api):
    result = sleep_api["json"]["data"]["result"][0]
    assert "latency" in result, "latency not found in response"
    assert result["latency"]["value"] is not None
    logger.info(f"Latency: {result['latency']['value']}m ({result['latency']['text']})")


@step('the restfulness data should be present')
def verify_restfulness_present(sleep_api):
    result = sleep_api["json"]["data"]["result"][0]
    assert "restfulness" in result, "restfulness not found in response"
    assert result["restfulness"]["value"] is not None
    logger.info(f"Restfulness: {result['restfulness']['value']} ({result['restfulness']['text']})")


@step('the health trend data should be present')
def verify_health_trend_present(sleep_api):
    result = sleep_api["json"]["data"]["result"][0]
    assert "health_trend" in result, "health_trend not found in response"
    trend = result["health_trend"]
    assert "resp" in trend, "resp not in health_trend"
    assert "rhr" in trend, "rhr not in health_trend"
    assert "hrv" in trend, "hrv not in health_trend"
    assert "skin_temp" in trend, "skin_temp not in health_trend"
    logger.info(f"Health trend - RHR: {trend['rhr']['value']}, HRV: {trend['hrv']['value']}, Resp: {trend['resp']['value']}, Skin temp: {trend['skin_temp']['value']}")


@step('the sleep score value should be between 0 and 100')
def verify_sleep_score_range(sleep_api):
    result = sleep_api["json"]["data"]["result"][0]
    score = result["sleep_score"]["value"]
    assert 0 <= score <= 100, f"Sleep score {score} not between 0 and 100"
    logger.info(f"Sleep score {score} is in valid range 0-100")


@step(parsers.parse('the sleep score status should be one of "{statuses}"'))
def verify_sleep_score_status(sleep_api, statuses):
    result = sleep_api["json"]["data"]["result"][0]
    status = result["sleep_score"]["status"]
    valid_statuses = [s.strip() for s in statuses.split(",")]
    assert status in valid_statuses, f"Sleep score status '{status}' not in {valid_statuses}"
    logger.info(f"Sleep score status '{status}' is valid")


# ============ SLEEP CONTRIBUTORS STEPS ============

@step('the REM sleep value should be greater than 0')
def verify_rem_value(sleep_api):
    result = sleep_api["json"]["data"]["result"][0]
    value = result["rem_sleep"]["value"]
    assert value > 0, f"REM sleep value {value} is not > 0"
    logger.info(f"REM sleep value: {value}s")


@step(parsers.parse('the REM sleep status should be one of "{statuses}"'))
def verify_rem_status(sleep_api, statuses):
    result = sleep_api["json"]["data"]["result"][0]
    status = result["rem_sleep"]["status"]
    valid = [s.strip() for s in statuses.split(",")]
    assert status in valid, f"REM sleep status '{status}' not in {valid}"
    logger.info(f"REM sleep status: {status}")


@step('the deep sleep value should be greater than 0')
def verify_deep_value(sleep_api):
    result = sleep_api["json"]["data"]["result"][0]
    value = result["deep_sleep"]["value"]
    assert value > 0, f"Deep sleep value {value} is not > 0"
    logger.info(f"Deep sleep value: {value}s")


@step(parsers.parse('the deep sleep status should be one of "{statuses}"'))
def verify_deep_status(sleep_api, statuses):
    result = sleep_api["json"]["data"]["result"][0]
    status = result["deep_sleep"]["status"]
    valid = [s.strip() for s in statuses.split(",")]
    assert status in valid, f"Deep sleep status '{status}' not in {valid}"
    logger.info(f"Deep sleep status: {status}")


@step('the efficiency value should be between 0 and 100')
def verify_efficiency_value(sleep_api):
    result = sleep_api["json"]["data"]["result"][0]
    value = result["efficiency"]["value"]
    assert 0 <= value <= 100, f"Efficiency value {value} not between 0-100"
    logger.info(f"Efficiency value: {value}%")


@step(parsers.parse('the efficiency status should be one of "{statuses}"'))
def verify_efficiency_status(sleep_api, statuses):
    result = sleep_api["json"]["data"]["result"][0]
    status = result["efficiency"]["status"]
    valid = [s.strip() for s in statuses.split(",")]
    assert status in valid, f"Efficiency status '{status}' not in {valid}"
    logger.info(f"Efficiency status: {status}")


@step('the sleep duration value should be greater than 0')
def verify_duration_value(sleep_api):
    result = sleep_api["json"]["data"]["result"][0]
    value = result["sleep_duration"]["value"]
    assert value > 0, f"Sleep duration value {value} is not > 0"
    logger.info(f"Sleep duration value: {value}s")


@step(parsers.parse('the sleep duration status should be one of "{statuses}"'))
def verify_duration_status(sleep_api, statuses):
    result = sleep_api["json"]["data"]["result"][0]
    status = result["sleep_duration"]["status"]
    valid = [s.strip() for s in statuses.split(",")]
    assert status in valid, f"Sleep duration status '{status}' not in {valid}"
    logger.info(f"Sleep duration status: {status}")


@step('the latency value should be greater than or equal to 0')
def verify_latency_value(sleep_api):
    result = sleep_api["json"]["data"]["result"][0]
    value = result["latency"]["value"]
    assert value >= 0, f"Latency value {value} is not >= 0"
    logger.info(f"Latency value: {value}m")


@step(parsers.parse('the latency status should be one of "{statuses}"'))
def verify_latency_status(sleep_api, statuses):
    result = sleep_api["json"]["data"]["result"][0]
    status = result["latency"]["status"]
    valid = [s.strip() for s in statuses.split(",")]
    assert status in valid, f"Latency status '{status}' not in {valid}"
    logger.info(f"Latency status: {status}")


@step('the restfulness value should be greater than or equal to 0')
def verify_restfulness_value(sleep_api):
    result = sleep_api["json"]["data"]["result"][0]
    value = result["restfulness"]["value"]
    assert value >= 0, f"Restfulness value {value} is not >= 0"
    logger.info(f"Restfulness value: {value}")


@step(parsers.parse('the restfulness status should be one of "{statuses}"'))
def verify_restfulness_status(sleep_api, statuses):
    result = sleep_api["json"]["data"]["result"][0]
    status = result["restfulness"]["status"]
    valid = [s.strip() for s in statuses.split(",")]
    assert status in valid, f"Restfulness status '{status}' not in {valid}"
    logger.info(f"Restfulness status: {status}")


@step('the circadian mid-point value should be present')
def verify_circadian_value(sleep_api):
    result = sleep_api["json"]["data"]["result"][0]
    assert "timing" in result, "timing (circadian mid-point) not found in response"
    value = result["timing"]["value"]
    assert value is not None, "Circadian mid-point value is None"
    logger.info(f"Circadian mid-point: {value} ({result['timing']['text']})")


@step(parsers.parse('the circadian mid-point status should be one of "{statuses}"'))
def verify_circadian_status(sleep_api, statuses):
    result = sleep_api["json"]["data"]["result"][0]
    status = result["timing"]["status"]
    valid = [s.strip() for s in statuses.split(",")]
    assert status in valid, f"Circadian mid-point status '{status}' not in {valid}"
    logger.info(f"Circadian mid-point status: {status}")


# scenarios() at bottom
scenarios("../sleep_api.feature")
