# Rejects bills from the real sheet if they are rejected in the copy sheet
# to ensure that rejected bills are not re-reviewed in the real sheet

import pandas as pd

from src.config import COPY_SPREADSHEET_ID, RANGE_NAME, REAL_SPREADSHEET_ID, SCOPES
from src.google_sheets import GoogleSheetsAPI


def main():
    real_sheet = GoogleSheetsAPI(
        range_name=RANGE_NAME, spreadsheet_id=REAL_SPREADSHEET_ID, scopes=SCOPES
    )
    real_df: pd.DataFrame = real_sheet.read_sheet()
    copy_sheet = GoogleSheetsAPI(
        range_name=RANGE_NAME, spreadsheet_id=COPY_SPREADSHEET_ID, scopes=SCOPES
    )
    copy_df = pd.DataFrame = copy_sheet.read_sheet()

    rejected_ids = set()
    for _, row in copy_df.iterrows():
        if row["Review Status"] == "Rejected":
            print(f"Adding {row['Legiscan Bill ID']} to rejected_ids")
            rejected_ids.add(row["Legiscan Bill ID"])

    for i, row in real_df.iterrows():
        if row["Review Status"] == "Unreviewed":
            if row["Legiscan Bill ID"] in rejected_ids:
                print(f"Rejecting {row['Legiscan Bill ID']} from real sheet")
                real_df.at[i, "Review Status"] = "Rejected"

    real_sheet.update_data(real_df)


if __name__ == "__main__":
    main()
