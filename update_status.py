from google_sheets import GoogleSheetsAPI
from legiscan import LegiscanClient
import pandas as pd


def main():
    sheet = GoogleSheetsAPI()
    df: pd.DataFrame = sheet.read_sheet()
    client = LegiscanClient()
    for i, row in df.iterrows():
        try:
            # if row["Latest Action"] not in {"Proposed and Pending", "Engrossed"}:
            #     continue
            bill_id = str(row["Legiscan Bill ID"])
            if bill_id == 'None':
                continue
            response = client.get_bill(bill_id)
            bill = response["bill"]
            status = client.get_status(
                bill["status"],
                bill["status_date"],
                bill["session"]["sine_die"],
            )
            history = bill["history"][-1]["action"]

            df.at[i, "Legiscan Status"] = status
            df.at[i, "Legiscan Latest History"] = history

            print(f"{i}. {str(row['Bill Number'])}: {status}")
        except Exception as e:
            print(f"{i}. {str(row['Bill Number'])}: FAILED ({e})")
    sheet.update_data(df)


if __name__ == "__main__":
    main()
