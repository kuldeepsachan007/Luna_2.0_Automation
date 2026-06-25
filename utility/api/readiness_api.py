import time
import requests
import logging
from utility.api.api_config import BASE_URL, DEFAULT_HEADERS

logger = logging.getLogger(__name__)


class ReadinessAPI:
    def __init__(self, access_token: str):
        self.base_url = BASE_URL
        self.headers = {
            **DEFAULT_HEADERS,
            "access-token": f"Bearer {access_token}",
            "epoch-time": str(int(time.time() * 1000)),
        }

    def get_readiness_details(self):
        """
        GET /luna/protean/v1/details?type=readiness
        Returns readiness descriptions/explanations
        """
        url = f"{self.base_url}/luna/protean/v1/details"
        params = {"type": "readiness"}

        logger.info(f"GET {url} | params={params}")
        response = requests.get(url, headers=self.headers, params=params, verify=False)
        logger.info(f"Status: {response.status_code}")
        return response

    def get_readiness_health_data(self, date: str):
        """
        GET /luna/sleep/v2/get - health_trend field has actual readiness values
        (RHR, HRV, Skin temp, Respiratory rate)
        """
        url = f"{self.base_url}/luna/sleep/v2/get"
        params = {"start_date": date, "end_date": date}

        logger.info(f"GET {url} | params={params}")
        response = requests.get(url, headers=self.headers, params=params, verify=False)
        logger.info(f"Status: {response.status_code}")
        return response
