from datetime import datetime
from typing import Optional

import requests

from .config import LEGISCAN_API_KEY


class LegiscanClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or LEGISCAN_API_KEY
        self.base_url = "https://api.legiscan.com/"

    def get_monitor_list(self, record: str = "all") -> list[dict]:
        return self._make_request("getMonitorList", record=record)["monitorlist"]

    def get_bill(self, bill_id: str) -> dict:
        return self._make_request("getBill", id=bill_id)

    def fetch_bills(self, monitor_list: list[dict]) -> list[dict]:
        """
        Fetches bills from the monitor list and returns a list of bill objects
        """
        return [self.get_bill(bill_id=bill["bill_id"]) for bill in monitor_list]

    def get_search(
        self,
        state: str,
        bill: Optional[str] = None,
        query: Optional[str] = None,
        year: int = 1,
        page: int = 1,
    ):
        if not bill and not query:
            raise ValueError("Either bill or query must be provided.")
        params = {"state": state, "year": year, "page": page}
        if bill:
            params["bill"] = bill
        elif query:
            params["query"] = query
        return self._make_request("getSearch", **params)

    def get_status_from(self, status_id: int, status_date: str, sine_die: int) -> str:
        if status_id >= len(self.STATUS) or status_id < 0:
            status_description = "N/A"
        else:
            status_description = self.STATUS[status_id]

        date_object = datetime.strptime(status_date, "%Y-%m-%d")
        status_date = date_object.strftime("%B %d, %Y")  # Example: May 12, 2024
        response = f"{status_description} on {status_date}"
        if status_id in {1, 2, 3}:
            response += ", died in chamber/committee" if sine_die else ""

        return response

    def _make_request(self, operation: str, **params):
        params.update({"key": self.api_key, "op": operation})
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        return response.json()

    STATUS = [
        "Prefiled",
        "Introduced",
        "Engrossed",
        "Enrolled",
        "Passed",
        "Vetoed",
        "Failed",
        "Override",
        "Chaptered",
        "Refer",
        "Report Pass",
        "Report DNP",
        "Draft",
    ]

    STATE_ABBR_TO_NAME = {
        # https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States#States.
        "AK": "Alaska",
        "AL": "Alabama",
        "AR": "Arkansas",
        "AZ": "Arizona",
        "CA": "California",
        "CO": "Colorado",
        "CT": "Connecticut",
        "DE": "Delaware",
        "FL": "Florida",
        "GA": "Georgia",
        "HI": "Hawaii",
        "IA": "Iowa",
        "ID": "Idaho",
        "IL": "Illinois",
        "IN": "Indiana",
        "KS": "Kansas",
        "KY": "Kentucky",
        "LA": "Louisiana",
        "MA": "Massachusetts",
        "MD": "Maryland",
        "ME": "Maine",
        "MI": "Michigan",
        "MN": "Minnesota",
        "MO": "Missouri",
        "MS": "Mississippi",
        "MT": "Montana",
        "NC": "North Carolina",
        "ND": "North Dakota",
        "NE": "Nebraska",
        "NH": "New Hampshire",
        "NJ": "New Jersey",
        "NM": "New Mexico",
        "NV": "Nevada",
        "NY": "New York",
        "OH": "Ohio",
        "OK": "Oklahoma",
        "OR": "Oregon",
        "PA": "Pennsylvania",
        "RI": "Rhode Island",
        "SC": "South Carolina",
        "SD": "South Dakota",
        "TN": "Tennessee",
        "TX": "Texas",
        "UT": "Utah",
        "VA": "Virginia",
        "VT": "Vermont",
        "WA": "Washington",
        "WI": "Wisconsin",
        "WV": "West Virginia",
        "WY": "Wyoming",
        # https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States#Federal_district.
        "DC": "District of Columbia",
        # https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States#Inhabited_territories.
        "AS": "American Samoa",
        "GU": "Guam GU",
        "MP": "Northern Mariana Islands",
        "PR": "Puerto Rico PR",
        "VI": "U.S. Virgin Islands",
    }

    STATE_NAME_TO_ABBR = {
        "Alabama": "AL",
        "Alaska": "AK",
        "Arizona": "AZ",
        "Arkansas": "AR",
        "California": "CA",
        "Colorado": "CO",
        "Connecticut": "CT",
        "Delaware": "DE",
        "Florida": "FL",
        "Georgia": "GA",
        "Hawaii": "HI",
        "Idaho": "ID",
        "Illinois": "IL",
        "Indiana": "IN",
        "Iowa": "IA",
        "Kansas": "KS",
        "Kentucky": "KY",
        "Louisiana": "LA",
        "Maine": "ME",
        "Maryland": "MD",
        "Massachusetts": "MA",
        "Michigan": "MI",
        "Minnesota": "MN",
        "Mississippi": "MS",
        "Missouri": "MO",
        "Montana": "MT",
        "Nebraska": "NE",
        "Nevada": "NV",
        "New Hampshire": "NH",
        "New Jersey": "NJ",
        "New Mexico": "NM",
        "New York": "NY",
        "North Carolina": "NC",
        "North Dakota": "ND",
        "Ohio": "OH",
        "Oklahoma": "OK",
        "Oregon": "OR",
        "Pennsylvania": "PA",
        "Rhode Island": "RI",
        "South Carolina": "SC",
        "South Dakota": "SD",
        "Tennessee": "TN",
        "Texas": "TX",
        "Utah": "UT",
        "Vermont": "VT",
        "Virginia": "VA",
        "Washington": "WA",
        "West Virginia": "WV",
        "Wisconsin": "WI",
        "Wyoming": "WY",
        "District of Columbia": "DC",
        "American Samoa": "AS",
        "Guam": "GU",
        "Northern Mariana Islands": "MP",
        "Puerto Rico": "PR",
        "United States Minor Outlying Islands": "UM",
        "U.S. Virgin Islands": "VI",
    }
