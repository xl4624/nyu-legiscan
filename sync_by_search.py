# Google Sheets to Search in LegiScan API
# Should be run biweekly(?) to update bills that are manually added
# either by Terrance or by other community members

import re

import pandas as pd

from google_sheets import GoogleSheetsAPI
from legiscan import LegiscanClient


def main():
    sheets = GoogleSheetsAPI()
    try:
        df = sheets.read_sheet()
    except ValueError as e:
        print(e)
        return
    client = LegiscanClient()

    df = df[df["Level of Government"] == "State"]
    df = df.dropna(how="all")
    df["Introduction Date"] = pd.to_datetime(
        df["Introduction Date"], format="mixed", errors="coerce"
    )
    rows = df.to_dict("records")  # type: ignore
    for row in rows:
        state = row["Jurisdiction"]
        # if state not in LegiscanClient.STATE_NAME_TO_ABBR:
        #     print(state)
        state = LegiscanClient.STATE_NAME_TO_ABBR[state]
        queries = [
            row["Bill Number"].replace(" ", ""),
            re.sub(r"[A-Za-z]", "", row["Bill Number"]),
        ]
        result, query = None, None
        try:
            for query in queries:
                result = client.get_search(state, query)
                if result["status"] == "OK" and result["searchresult"]["summary"]["count"] > 0:
                    break
            if (result is None) or (result and result["searchresult"]["summary"]["count"] == 0):
                print(f"No bill found for ({state}, {query}): {row['Bill Number']}")
        except Exception as e:
            print(f"Failed to search for ({state}, {query}): - {row['Bill Number']}")
            print(e)


if __name__ == "__main__":
    main()
