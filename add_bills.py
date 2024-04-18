import os

import pandas as pd

from src.google_sheets import GoogleSheetsAPI
from src.legiscan import LegiscanClient

KEYWORDS = [
    '"Aerial Drones"',
    '"Acoustic Gunshot Detection"',
    '"Artificial Intelligence"',
    '"Automated Decision Systems"',
    '"Automated Decision Making"',
    '"Automatic License Plate Reader"',
    '"Biometric Data"',
    '"Biometric Information"',
    '"Biometric Surveillance"',
    '"Body-Worn Cameras"',
    '"Cell Phone Location Data"',
    '"Cell Site Simulators"',
    '"Child Data Collection"',
    '"Child Data Surveillance"',
    '"Consumer Data"',
    '"Consumer Health Data"',
    '"Consumer Data Privacy"',
    '"Consumer Privacy"',
    '"Data Broker"',
    '"Data Mining"',
    '"DNA Database"',
    '"Driver’s License Data"',
    '"Drones"',
    '"Electronic Communication"',
    '"Electronic Monitoring"',
    '"Electronic Tolling Data"',
    '"Facial Recognition Technology"',
    '"Forensic Investigative Genetic Genealogy"',
    '"Foreign Intelligence Surveillance Act"',
    '"Genetic Data"',
    '"Geofence"',
    '"Geofence Warrant"',
    '"Geolocation Data"',
    '"Health Data"',
    '"IMSI catchers"',
    '"Location Data"',
    '"DNA Phenotyping"',
    '"Predictive Policing"',
    '"Predictive Algorithm"',
    '"Prison Surveillance"',
    '"Privacy"',
    '"Public Health Surveillance Data"',
    '"National Security Electronic Surveillance"',
    '"Rapid DNA"',
    '"Reverse Keyword Search"',
    '"Reverse Warrant"',
    '"Reproductive Health Surveillance Data"',
    '"Risk Assessment Instrument"',
    '"Robotic Device"',
    '"School Surveillance"',
    '"Social Media Surveillance"',
    '"Stingrays"',
    '"Surveillance"',
    '"Video Surveillance"',
]


def main():
    # sheet = GoogleSheetsAPI()
    # df: pd.DataFrame = sheet.read_sheet()
    client = LegiscanClient()
    for keyword in KEYWORDS:
        response = client.get_search("ALL", query=keyword, year=2)
        if response["status"] != "OK":
            print(f"{keyword} failed during search")
            continue

        search_results = response["searchresult"]
        count = search_results["summary"]["count"]
        print(f"{keyword} : {count}")
        if count == 0:
            continue

        keyword_file_path = keyword.replace('"', "").replace(" ", "_").lower().strip()
        file_path = os.path.join("logs", f"{keyword_file_path}.log")
        with open(file_path, "w") as file:
            for key, candidate in search_results.items():
                if key.isdigit():
                    file.write(format_bill(key, candidate))

    # sheet.update_data(df)


def format_bill(key, candidate):
    return f"""Bill {key}
-------------------------
  - Title: {candidate['title']}
  - Bill_number: {candidate['bill_number']}
  - Relevance: {candidate['relevance']}
  - URL: {candidate['url']}"""

if __name__ == "__main__":
    main()
