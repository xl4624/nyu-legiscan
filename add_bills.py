from datetime import datetime, timedelta, timezone

import pandas as pd

from src.config import COPY_SPREADSHEET_ID, KEYWORDS, RANGE_NAME, REAL_SPREADSHEET_ID, SCOPES
from src.google_sheets import GoogleSheetsAPI
from src.legiscan import LegiscanClient


def main():
    sheet = GoogleSheetsAPI(
        spreadsheet_id=COPY_SPREADSHEET_ID, range_name=RANGE_NAME, scopes=SCOPES
    )
    df: pd.DataFrame = sheet.read_sheet()
    client = LegiscanClient()
    rows_to_append = []
    seen_ids = set()
    for bill_id in df["Legiscan Bill ID"]:
        if bill_id is not None and bill_id != "" and bill_id in seen_ids:
            print(bill_id)
        seen_ids.add(bill_id)

    for keyword in KEYWORDS:
        page = 1
        stop = False
        while not stop:
            response = client.get_search(state="ALL", bill=None, query=keyword, year=3, page=page)
            if response["status"] != "OK":
                print(f"{keyword} failed during search")
                break

            search_results = response["searchresult"]
            count = search_results["summary"]["count"]
            page_total = search_results["summary"]["page_total"]
            print(f"{keyword}: {count} (PAGE {page})")

            for key, candidate in search_results.items():
                if not key.isdigit():  # skip the summary
                    continue

                # Since getSearch is sorted by relevance, if we find a bill with a
                # relevance score less than 90, we can stop searching for that keyword
                if candidate["relevance"] < 90:
                    print(f"Found a bill with relevance < 90, stopping search for {keyword}")
                    stop = True
                    break

                if str(candidate["bill_id"]) not in seen_ids:
                    bill_id = str(candidate["bill_id"])
                    if (
                        candidate["last_action_date"]
                        and candidate["last_action_date"][0:4] != "2023"
                    ):
                        continue

                    response = client.get_bill(bill_id)
                    if response["status"] == "OK" and response["bill"]["status"] == 4:
                        bill = response["bill"]
                        current_time = datetime.now(timezone(-timedelta(hours=5)))  # assuming gmt-5
                        status_last_updated = (
                            f"{current_time.strftime('%Y-%m-%d %I:%M:%S %p')} GMT-05:00"
                        )
                        level_of_government = "State" if bill["state"] != "US" else "Federal"

                        if bill["state"] != "US":
                            jurisdiction = client.STATE_ABBR_TO_NAME[bill["state"]]
                        else:
                            jurisdiction = "Federal"

                        sponsors: list[str] = []
                        for sponsor in bill["sponsors"]:
                            if sponsor["sponsor_type_id"] == 1:  # filters out co-sponsors
                                sponsors.append(f"{sponsor['role']} {sponsor['name']}")

                        status = client.get_status_from(
                            bill["status"],
                            bill["status_date"],
                            bill["session"]["sine_die"],
                        )
                        history = bill["history"][-1]["action"]

                        row = {
                            "Status Last Updated": status_last_updated,
                            "Review Status": "Unreviewed",
                            "Level of Government": level_of_government,
                            "Jurisdiction": jurisdiction,
                            "Legislation Title": bill["title"],
                            "Bill Number": bill["bill_number"],
                            "Link to Bill": bill["state_link"],
                            "Introduction Date": bill["progress"][0]["date"],
                            "Enactment Date": bill["status_date"] if bill["status"] == 4 else "N/A",
                            "Latest Action": "Enacted",
                            "Legiscan Status": status,
                            "Legiscan Latest History": history,
                            "Official Description": bill["description"],
                            "Sponsors and Co-Sponsors": "\n".join(sponsors),
                            "Data Contributed By": "The Center on Race, Inequality, and the Law",
                            "Legiscan Bill ID": bill["bill_id"],
                            "Change Hash": bill["change_hash"],
                        }
                        print(f"Adding new bill from keyword {keyword}: {bill['title']}")
                        rows_to_append.append(row)
                        seen_ids.add(bill_id)

            # The reason we don't just for loop using page_total is that for some
            # reason, the page_total (especially in the first few pages) is not accurate
            # and will increase as we paginate through the results.
            if page >= page_total:
                break
            page += 1

    print(f"Added {len(rows_to_append)} new bills")
    new_df = pd.DataFrame(rows_to_append)
    df = pd.concat([df, new_df], ignore_index=True).fillna("")
    sheet.update_data(df)


if __name__ == "__main__":
    main()
