import time
import requests
import logging
from utility.api.api_config import BASE_URL, DEFAULT_HEADERS

logger = logging.getLogger(__name__)


class ActivityAPI:
    def __init__(self, access_token: str):
        self.base_url = BASE_URL
        self.headers = {
            **DEFAULT_HEADERS,
            "access-token": f"Bearer {access_token}",
            "epoch-time": str(int(time.time() * 1000)),
        }

    def get_activity_goals(self, date: str):
        """
        GET /luna/activity/v2/goals?date=YYYY-MM-DD
        """
        url = f"{self.base_url}/luna/activity/v2/goals"
        params = {"date": date}

        logger.info(f"GET {url} | params={params}")
        response = requests.get(url, headers=self.headers, params=params, verify=False)
        logger.info(f"Status: {response.status_code}")
        return response
