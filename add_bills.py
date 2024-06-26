from datetime import datetime, timedelta, timezone
import pandas as pd
from src.config import (
    COPY_SPREADSHEET_ID,
    KEYWORDS,
    RANGE_NAME,
    SCOPES,
    LOCAL_TIMEZONE_OFFSET,
)
from src.google_sheets import GoogleSheetsAPI
from src.legiscan import LegiscanClient

def main():
    sheet = GoogleSheetsAPI(
        spreadsheet_id=COPY_SPREADSHEET_ID, range_name=RANGE_NAME, scopes=SCOPES
    )
    df: pd.DataFrame = sheet.read_sheet()
    client = LegiscanClient()
    session_year = 3 # year=3: recent(24/23), 2: current(24) 
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
            response = client.get_search(state="ALL", bill=None, query=keyword, year=session_year, page=page) 
            if response["status"] != "OK":
                print(f"{keyword} failed during search")
                break

            search_results = response["searchresult"]
            count = search_results["summary"]["count"]
            page_total = search_results["summary"]["page_total"]
            print(f"{keyword}: {count} (PAGE {page}) Session year: {session_year}")

            for key, candidate in search_results.items():
                if not key.isdigit():  # skip the summary
                    continue

                bill_id = str(candidate["bill_id"])
                if bill_id in seen_ids:  # avoid duplicates
                    continue

                # Since getSearch is sorted by relevance, if we find a bill with a
                # relevance score less than 90, we can stop searching for that keyword
                if candidate["relevance"] < 90:
                    print(f"Found a bill with relevance < 90, stopping search for {keyword}")
                    stop = True
                    break

                if passes_pre_detail_filter(candidate):
                    response = client.get_bill(bill_id)
                    if response["status"] != "OK":
                        continue

                    bill = response["bill"]
                    if True: #passes_post_detail_filter(bill): 
                        current_time = datetime.now(timezone(-timedelta(hours=5)))  # assuming gmt-5
                        # current_time = #datetime.now(timezone(timedelta(hours=abs(LOCAL_TIMEZONE_OFFSET)) * (abs(LOCAL_TIMEZONE_OFFSET)/LOCAL_TIMEZONE_OFFSET) ))  # LOCAL_TIMEZONE_OFFSET changes based of the timezone of the server
                        status_last_updated = (
                            f"{current_time.strftime('%Y-%m-%d %I:%M:%S %p')} GMT-05:00"
                        )
                        # status_last_updated = (
                        #     f"{current_time.strftime('%Y-%m-%d %I:%M:%S %p')} GMT-0{LOCAL_TIMEZONE_OFFSET}:00"
                        # )
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
                        bill["status"] = 'Enacted' if bill["status"] in [4, 7, 8] else LegiscanClient.STATUS[bill["status"]]
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
                            "Latest Action": bill["status"], #"Enacted",
                            "Legiscan Status": status,
                            "Legiscan Latest History": history,
                            "Official Description": bill["description"],
                            "Sponsors and Co-Sponsors": "\n".join(sponsors),
                            "Data Contributed By": "The Center on Race, Inequality, and the Law",
                            "Legiscan Bill ID": bill["bill_id"],
                            "Change Hash": bill["change_hash"],
                        }
                        print(f"Adding new bill from keyword {keyword}: {bill['title']}, {jurisdiction}, {bill['bill_number']}")
                        rows_to_append.append(row)
                        seen_ids.add(bill_id)

            # The reason we don't just for loop using page_total is that for some
            # reason, the page_total (for the first few pages at least) is not
            # accurate and will increase as we paginate through the results.
            if page >= page_total:
                break
            page += 1

    print(f"Added {len(rows_to_append)} new bills")
    new_df = pd.DataFrame(rows_to_append)
    df = pd.concat([df, new_df], ignore_index=True).fillna("")
    sheet.update_data(df)


# These are just example filters that we used on 05/01/2024.
def passes_pre_detail_filter(candidate):
    """
    Criteria for filtering bills from search results.
    """
    return (candidate["last_action_date"] and (
                candidate["last_action_date"][0:4] == "2023" 
            )
        )


def passes_post_detail_filter(bill):
    """
    Criteria for filtering bills from bill details.
    """
    return bill["status"] == 4


if __name__ == "__main__":
    main()
