import time
import requests
import logging
from utility.api.api_config import BASE_URL, DEFAULT_HEADERS

logger = logging.getLogger(__name__)


class SleepAPI:
    def __init__(self, access_token: str):
        self.base_url = BASE_URL
        self.headers = {
            **DEFAULT_HEADERS,
            "access-token": f"Bearer {access_token}",
            "epoch-time": str(int(time.time() * 1000)),
        }

    def get_sleep_data(self, start_date: str, end_date: str = None):
        """
        GET /luna/sleep/v2/get?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
        """
        if end_date is None:
            end_date = start_date

        url = f"{self.base_url}/luna/sleep/v2/get"
        params = {"start_date": start_date, "end_date": end_date}

        logger.info(f"GET {url} | params={params}")
        response = requests.get(url, headers=self.headers, params=params, verify=False)
        logger.info(f"Status: {response.status_code}")
        return response

    def get_sleep_score(self, date: str):
        """Get sleep score from sleep data"""
        response = self.get_sleep_data(date)
        data = response.json()
        if data.get("success") and data["data"]["result"]:
            return data["data"]["result"][0].get("sleep_score")
        return None

    def get_sleep_duration(self, date: str):
        """Get sleep duration from sleep data"""
        response = self.get_sleep_data(date)
        data = response.json()
        if data.get("success") and data["data"]["result"]:
            return data["data"]["result"][0].get("sleep_duration")
        return None

    def get_rem_sleep(self, date: str):
        """Get REM sleep data"""
        response = self.get_sleep_data(date)
        data = response.json()
        if data.get("success") and data["data"]["result"]:
            return data["data"]["result"][0].get("rem_sleep")
        return None

    def get_deep_sleep(self, date: str):
        """Get deep sleep data"""
        response = self.get_sleep_data(date)
        data = response.json()
        if data.get("success") and data["data"]["result"]:
            return data["data"]["result"][0].get("deep_sleep")
        return None

    def get_efficiency(self, date: str):
        """Get efficiency data"""
        response = self.get_sleep_data(date)
        data = response.json()
        if data.get("success") and data["data"]["result"]:
            return data["data"]["result"][0].get("efficiency")
        return None

    def get_latency(self, date: str):
        """Get latency data"""
        response = self.get_sleep_data(date)
        data = response.json()
        if data.get("success") and data["data"]["result"]:
            return data["data"]["result"][0].get("latency")
        return None

    def get_restfulness(self, date: str):
        """Get restfulness data"""
        response = self.get_sleep_data(date)
        data = response.json()
        if data.get("success") and data["data"]["result"]:
            return data["data"]["result"][0].get("restfulness")
        return None

    def get_health_trend(self, date: str):
        """Get health trend (resp, rhr, hrv, skin_temp)"""
        response = self.get_sleep_data(date)
        data = response.json()
        if data.get("success") and data["data"]["result"]:
            return data["data"]["result"][0].get("health_trend")
        return None
