# Google Sheets to Search in LegiScan API
# Should be run biweekly(?) to update bills that are manually added
# either by Terrance or by other community members

import re

import pandas as pd

from src.config import COPY_SPREADSHEET_ID, RANGE_NAME, SCOPES
from src.google_sheets import GoogleSheetsAPI
from src.legiscan import LegiscanClient


def main():
    sheet = GoogleSheetsAPI(
        spreadsheet_id=COPY_SPREADSHEET_ID, range_name=RANGE_NAME, scopes=SCOPES
    )
    df: pd.DataFrame = sheet.read_sheet()
    client = LegiscanClient()

    for i, row in df.iterrows():
        if row["Level of Government"] not in {"State", "Federal"}:
            continue

        state = str(row["Jurisdiction"]).strip()
        state = (
            LegiscanClient.STATE_NAME_TO_ABBR.get(state, "ALL")
            if state != "Federal"
            else "US"
        )

        bill_number = str(row["Bill Number"]).strip()
        bill_number = re.sub(r"\s+", "", bill_number)

        introduction_date = str(row["Introduction Date"]).strip()
        if introduction_date not in {"NA", "N/A", "", "nan"}:
            year = int(introduction_date.split("/")[-1])
        else:
            year = 1

        try:
            result = client.get_search(state, bill=bill_number, year=year)
            bill_id, change_hash = search_result(result)
            if bill_id and change_hash:
                print(f"{i}. ({state}, {bill_number})")
                df.at[i, "Legiscan Bill ID"] = bill_id
                df.at[i, "Change Hash"] = change_hash
            else:
                print(f"{i}. ({state}, {bill_number}): NOT FOUND")
        except Exception as e:
            print(f"{i}. ({state}, {bill_number}): FAILED ({e})")
    sheet.update_data(df)


def search_result(result):
    search_results = result.get("searchresult", {})
    print(f"COUNT {search_results['summary']['count']} | ", end="")
    for key in search_results:
        if key.isdigit():
            candidate = search_results[key]
            return (candidate["bill_id"], candidate["change_hash"])
    return (None, None)


if __name__ == "__main__":
    main()
