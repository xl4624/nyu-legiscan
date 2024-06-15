# TODO: Use the Change Hash to compare with getMasterListRaw calls to detect
# when bills have changed and need updating.

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
        try:
            bill_id = str(row["Legiscan Bill ID"])
            if bill_id == "None" or row["Review Status"] == "Rejected":
                continue

            response = client.get_bill(bill_id)
            bill = response["bill"]
            status = client.get_status_from(
                bill["status"],
                bill["status_date"],
                bill["session"]["sine_die"],
            )
            history = bill["history"][-1]["action"]

            df.at[i, "Legiscan Status"] = status
            df.at[i, "Legiscan Latest History"] = history

            if df.at[i, "Manual Override (for Latest Action)"] == "TRUE":
                continue

            if bill["status"] in {1, 2, 3}:
                if bill["session"]["sine_die"] == 1:
                    latest_action = "Died in Chamber/Committee"
                else:
                    latest_action = LegiscanClient.STATUS[bill["status"]]
            elif bill["status"] == 4:  # From passed to enacted
                latest_action = "Enacted" # passed
            else:
                latest_action = LegiscanClient.STATUS[bill["status"]]

            df.at[i, "Latest Action"] = latest_action

            print(f"{i}. {str(row['Bill Number'])}: {status}")
        except Exception as e:
            print(f"{i}. {str(row['Bill Number'])}: FAILED ({e})")
            exit()

    # sheet.update_data(df)

if __name__ == "__main__":
    main()
