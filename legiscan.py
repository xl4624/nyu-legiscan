from typing import Optional

import requests

from config import LEGISCAN_API_KEY


class LegiscanClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key if api_key else LEGISCAN_API_KEY
        self.base_url = "https://api.legiscan.com/"

    def get_monitor_list(self, record="all") -> list[dict]:
        return self._make_request("getMonitorList", record=record)["monitorlist"]

    def get_bill(self, bill_id: str) -> dict:
        return self._make_request("getBill", id=bill_id)

    def fetch_bills(self, monitor_list: list[dict]) -> list[dict]:
        """
        Fetches bills from the monitor list and returns a list of bill objects
        """
        return [self.get_bill(bill_id=bill["bill_id"]) for bill in monitor_list]

    def _make_request(self, operation: str, **params):
        params["key"] = self.api_key
        params["op"] = operation

        response = requests.get(self.base_url, params=params)

        if response.status_code != 200:
            response.raise_for_status()
        return response.json()
