import os
from dotenv import load_dotenv

load_dotenv()

LEGISCAN_API_KEY = os.getenv("LEGISCAN_API_KEY")
if LEGISCAN_API_KEY is None:
    print("Please add the LEGISCAN_API_KEY variable to your .env file")
    exit(1)

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

REAL_SPREADSHEET_ID = "1DBmf-9UObut_uh9i9GtEP7_hciqzd6uLMqPPKU9B0MA"
COPY_SPREADSHEET_ID = "15xeV_rgcHNYVUydU31fre8HZ19aIC7V3jLWuvW1rScI"

RANGE_NAME = "Input Form Responses!A1:AD"

# Keywords to search for
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
