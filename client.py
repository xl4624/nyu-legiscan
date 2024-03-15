import requests


class LegiscanClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = f"https://api.legiscan.com/"

    def get_monitor_list(self, record="current") -> list[dict]:
        return self._make_request("getMonitorList", record=record)["monitorlist"]

    def get_bill(self, bill_id: int) -> dict:
        return self._make_request("getBill", id=bill_id)

    def _make_request(self, operation: str, **params):
        params["key"] = self.api_key
        params["op"] = operation

        response = requests.get(self.base_url, params=params)

        if response.status_code != 200:
            response.raise_for_status()
        return response.json()
