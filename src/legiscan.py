from datetime import datetime
from typing import Optional, List
import requests
from .config import LEGISCAN_API_KEY

class LegiscanClient:
    BASE_URL = "https://api.legiscan.com/"

    def __init__(self, api_key: Optional[str] = LEGISCAN_API_KEY):
        self.api_key = api_key

    def get_monitor_list(self, record: Optional[str] = "current") -> List[dict]:
        """
        This operation returns the GAITS monitor list of summary bill data being tracked by the
        account associated with the API key.

        Parameters:
            record (Optional) Record filter current or archived, 2010 >= exact year
        """
        return self._make_request("getMonitorList", record=record)["monitorlist"]

    def get_bill(self, id: str) -> dict:
        """
        This operation returns the primary bill detail information including sponsors, committee
        references, full history, bill text and roll call information.

        Parameters:
            id: Retrieve bill detail information for bill_id as given by id

        Returns:
            Detail bill information object enumerating associated information along with sponsor
            people_id, bill text doc_id and voting roll_call_id.
        """
        return self._make_request("getBill", id=id)

    def get_search(
        self,
        state: str,
        bill: Optional[str] = None,
        query: Optional[str] = None,
        year: Optional[int] = 2,
        page: Optional[int] = 1,
    ) -> dict:
        """
        Performs a search against the national database using the LegiScan full text engine,
        returning a paginated result set, appropriate to drive an interactive search appliance.

        Parameters:
            state: The state abbreviation to search within, or 'ALL' for nationwide search.
            bill: A specific bill number to search for.
            query: A full-text query string, URL encoded, to search within the database.
            year: (Optional) Year where 1=all, 2=current, 3=recent, 4=prior, >1900=exact
            page: (Optional) Result set page number to return.

        Returns:
            Page of search results based on relevance to the given search parameters.

        Raises:
            ValueError: If neither bill nor query is provided.
        """
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
        response = requests.get(self.BASE_URL, params=params)
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
        "AK": "Alaska", "AL": "Alabama", "AR": "Arkansas", "AZ": "Arizona", "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "IA": "Iowa", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "MA": "Massachusetts", "MD": "Maryland", "ME": "Maine", "MI": "Michigan", "MN": "Minnesota", "MO": "Missouri", "MS": "Mississippi", "MT": "Montana", "NC": "North Carolina", "ND": "North Dakota", "NE": "Nebraska", "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NV": "Nevada", "NY": "New York", "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VA": "Virginia", "VT": "Vermont", "WA": "Washington", "WI": "Wisconsin", "WV": "West Virginia", "WY": "Wyoming",
        # https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States#Federal_district.
        "DC": "District of Columbia",
        # https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States#Inhabited_territories.
        "AS": "American Samoa", "GU": "Guam GU", "MP": "Northern Mariana Islands", "PR": "Puerto Rico PR", "VI": "U.S. Virgin Islands",
    }  # fmt: skip

    STATE_NAME_TO_ABBR = {
        "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY", "District of Columbia": "DC", "American Samoa": "AS", "Guam": "GU", "Northern Mariana Islands": "MP", "Puerto Rico": "PR", "United States Minor Outlying Islands": "UM", "U.S. Virgin Islands": "VI",
    }  # fmt: skip
