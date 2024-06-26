# Monitor List to Google Sheets Bill ID and Change Hash Sync
# Deprecated since we should search from the Google Sheets to the Legsican API not the other way around.

import Log
import re
from src.config import RANGE_NAME, COPY_SPREADSHEET_ID, SCOPES
from src.google_sheets import GoogleSheetsAPI
from src.legiscan import LegiscanClient


def main():
    # Example of using the Legiscan API Client
    client = LegiscanClient()
    monitor_list = client.get_monitor_list()
    bills = [
        {
            "bill_id": str(bill["bill"]["bill_id"]),
            "change_hash": bill["bill"]["change_hash"],
            "bill_number": bill["bill"]["bill_number"].upper().replace(" ", ""),
            "title": bill["bill"]["title"],
            "state": bill["bill"]["state"],
        }
        for bill in [client.get_bill(bill["bill_id"]) for bill in monitor_list]
    ]

    # Example of using the Google Sheets API to read and update data
    sheets = GoogleSheetsAPI(
        spreadsheet_id=COPY_SPREADSHEET_ID, range_name=RANGE_NAME, scopes=SCOPES
    )
    df = sheets.read_sheet()

    unmatched_bills_length = 0
    for bill in bills:
        bill_number = bill["bill_number"]

        # Split up bill into prefix (without numbers) and suffix (only numbers)
        if parts := re.match(r"(\D+)(\d+)", bill_number):
            prefix, suffix = parts.groups()
            modified_bill_numbers = set(
                [
                    bill_number,  # Original
                    prefix + "B" + suffix,  # Add 'B' to prefix
                    prefix + suffix.lstrip("0"),  # Remove leading zeros from suffix
                    prefix + "B" + suffix.lstrip("0"),  # Both modifications
                ]
            )
            if prefix == "LD":
                modified_bill_numbers.add("SB" + suffix)
                modified_bill_numbers.add("HB" + suffix)

            # Check if any version of the bill number is in the DataFrame
            for bn in modified_bill_numbers:
                state_abbr = bill["state"]
                state_full = LegiscanClient.STATE_ABBR_TO_NAME.get(state_abbr, "Federal")
                mask = df["Bill Number"].str.upper().str.replace(" ", "").eq(bn)

                # There is a SB362 bill in California and a SB362 bill in New Hampshire,
                # so we need to check the jurisdiction as well.
                # Also if it's a state bill it will have the the full state name but if it's a
                # city bill it will be in the "city, state_abbr" format.
                mask &= df["Jurisdiction"].str.contains(state_full) | df[
                    "Jurisdiction"
                ].str.contains(state_abbr)

                if mask.sum() > 1:
                    print(f"Multiple matches for bill number {bn} in {state_full}.")

                if mask.any():
                    df.loc[mask, "Legiscan Bill ID"] = bill["bill_id"]
                    df.loc[mask, "Change Hash"] = bill["change_hash"]
                    df.loc[mask, "Bill Number"] = bill["bill_number"]
                    break
            else:
                unmatched_bills_length += 1
                print(f"Bill not found in Google Sheet: {bill_number}")

    print(f"{unmatched_bills_length} bills were not matched to the Google Sheet.")
    sheets.update_data(df)


if __name__ == "__main__":
    main()
