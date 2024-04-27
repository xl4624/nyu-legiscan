from datetime import datetime, timedelta, timezone

import pandas as pd

from src.google_sheets import GoogleSheetsAPI
from src.legiscan import LegiscanClient

KEYWORDS = [
    # '"Aerial Drones"',
    # '"Acoustic Gunshot Detection"',
    # '"Artificial Intelligence"',
    # '"Automated Decision Systems"',
    '"Automated Decision Making"',
    # '"Automatic License Plate Reader"',
    # '"Biometric Data"',
    # '"Biometric Information"',
    # '"Biometric Surveillance"',
    # '"Body-Worn Cameras"',
    # '"Cell Phone Location Data"',
    # '"Cell Site Simulators"',
    # '"Child Data Collection"',
    # '"Child Data Surveillance"',
    # '"Consumer Data"',
    # '"Consumer Health Data"',
    # '"Consumer Data Privacy"',
    # '"Consumer Privacy"',
    # '"Data Broker"',
    # '"Data Mining"',
    # '"DNA Database"',
    # '"Driver’s License Data"',
    # '"Drones"',
    # # '"Electronic Communication"',
    # '"Electronic Monitoring"',
    # '"Electronic Tolling Data"',
    # '"Facial Recognition Technology"',
    # '"Forensic Investigative Genetic Genealogy"',
    # '"Foreign Intelligence Surveillance Act"',
    # '"Genetic Data"',
    # '"Geofence"',
    # '"Geofence Warrant"',
    # '"Geolocation Data"',
    # # '"Health Data"',
    # '"IMSI catchers"',
    # '"Location Data"',
    # '"DNA Phenotyping"',
    # '"Predictive Policing"',
    # '"Predictive Algorithm"',
    # '"Prison Surveillance"',
    # # '"Privacy"',
    # '"Public Health Surveillance Data"',
    # '"National Security Electronic Surveillance"',
    # '"Rapid DNA"',
    # '"Reverse Keyword Search"',
    # '"Reverse Warrant"',
    # '"Reproductive Health Surveillance Data"',
    # '"Risk Assessment Instrument"',
    # '"Robotic Device"',
    # '"School Surveillance"',
    # '"Social Media Surveillance"',
    # '"Stingrays"',
    # # '"Surveillance"',
    # '"Video Surveillance"',
]


def main():
    sheet = GoogleSheetsAPI()
    df: pd.DataFrame = sheet.read_sheet()
    client = LegiscanClient()
    seen_ids = set()
    for bill_id in df["Legiscan Bill ID"]:
        if bill_id is not None and bill_id != "" and bill_id in seen_ids:
            print(bill_id)
        seen_ids.add(bill_id)
    rows_to_append = []

    for keyword in KEYWORDS:
        page = 1
        while True:
            response = client.get_search("ALL", query=keyword, year=3, page=page)
            if response["status"] != "OK":
                print(f"{keyword} failed during search")
                break

            search_results = response["searchresult"]
            count = search_results["summary"]["count"]
            page_total = search_results["summary"]["page_total"]
            print(f"{keyword}: {count} (PAGE {page})")

            for key, candidate in search_results.items():
                if key.isdigit() and str(candidate["bill_id"]) not in seen_ids:
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
                            if sponsor["sponsor_type_id"] == 1:
                                sponsors.append(f"{sponsor['role']} {sponsor['name']}")
                        row = {
                            "Status Last Updated": status_last_updated,
                            "Review Status": "Unreviewed",
                            "Level of Government": level_of_government,
                            "Jurisdiction": jurisdiction,
                            "Legislation Title": bill["title"],
                            "Bill Number": bill["bill_number"],
                            "Link to Bill": bill["state_link"],
                            "Introduction Date": bill["progress"][0]["date"],
                            "Enactment Date": bill["status_date"],
                            "Latest Action": "Enacted",
                            "Official Description": bill["description"],
                            "Sponsors and Co-Sponsors": "\n".join(sponsors),
                            "Data Contributed By": "The Center on Race, Inequality, and the Law",
                            "Legiscan Bill ID": bill["bill_id"],
                            "Change Hash": bill["change_hash"],
                        }
                        rows_to_append.append(row)
                        print(row)
                        seen_ids.add(bill_id)

            # Break if we have reached the end of the results
            if page >= page_total:
                # print(f"{keyword}: {count}")
                break
            page += 1

    new_df = pd.DataFrame(rows_to_append)
    df = pd.concat([df, new_df], ignore_index=True)
    df = df.fillna("")
    # sheet.update_data(df)


if __name__ == "__main__":
    main()
