from datetime import datetime

import pandas as pd

from src.google_sheets import GoogleSheetsAPI
from src.legiscan import LegiscanClient


def main():
    sheet = GoogleSheetsAPI()
    df: pd.DataFrame = sheet.read_sheet()
    client = LegiscanClient()

    for i, row in df.iterrows():
        try:
            bill_id = str(row["Legiscan Bill ID"])
            if bill_id == "None":
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

            if df.at[i, "Manual Override"] != "FALSE":
                continue

            if bill["session"]["sine_die"]:
                latest_action = "Died in Chamber/Committee"
            elif bill["status"] == 4:  # From passed to enacted
                latest_action = "Enacted"
            else:
                latest_action = LegiscanClient.STATUS[bill["status"]]

            df.at[i, "Latest Action"] = latest_action

            # Update the status last updated time if the row changes
            if any(row != df.loc[i]):
                df.at[i, "Status Last Updated"] = datetime.now()

            print(f"{i}. {str(row['Bill Number'])}: {status}")
        except Exception as e:
            print(f"{i}. {str(row['Bill Number'])}: FAILED ({e})")

    sheet.update_data(df)


if __name__ == "__main__":
    main()
