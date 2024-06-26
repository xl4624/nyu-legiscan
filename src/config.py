import os
import datetime
import pytz
from dotenv import load_dotenv

load_dotenv()

LEGISCAN_API_KEY = os.getenv("LEGISCAN_API_KEY")
# LOCAL_TIMEZONE = get_localzone()
LOCAL_TIMEZONE = pytz.timezone('Etc/GMT+5')
LOCAL_TIMEZONE_OFFSET = int(datetime.datetime.now(LOCAL_TIMEZONE).strftime("%Z"))

if LEGISCAN_API_KEY is None:
    print("Please add the LEGISCAN_API_KEY variable to your .env file")
    exit(1)

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

COPY_SPREADSHEET_ID = "19_D-eZL31ThVDAghXH5rGmzkJY0J8b0-Fs2QVpPidSM"
SPREADSHEET_ID = "1DBmf-9UObut_uh9i9GtEP7_hciqzd6uLMqPPKU9B0MA" # Live spreadsheet id
# COPY_SPREADSHEET_ID = SPREADSHEET_ID # live spreadsheet id

RANGE_NAME = "Input Form Responses!A1:AD"

# Tier one - Keyword list 
filtered_keywords = [
    # "Aerial Drones", 
    "Automated Decision Systems", 
    "Automated Decision Making", 
    "Automatic License Plate Reader", 
    "Biometric Data", 
    "Biometric Information", 
    "Biometric Surveillance", 
    "Body-Worn Cameras", 
    "Cell Site Simulators", 
    "Consumer Health Data", 
    "Consumer Data Privacy", 
    "Consumer Privacy", 
    "Data Broker", 
    "Data Mining", 
    "DNA Database", 
    "Drones", 
    "Electronic Monitoring", 
    "Electronic Tolling Data", 
    "Facial Recognition Technology", 
    "Forensic Investigative Genetic Genealogy", 
    "Foreign Intelligence Surveillance Act", 
    "Genetic Data", 
    "Geofence", 
    "Geolocation Data", 
    "IMSI catchers", 
    "Location Data", 
    "DNA Phenotyping", 
    "Predictive Policing", 
    "Public Health Surveillance Data", 
    "Rapid DNA", 
    "Reverse Keyword Search", 
    "Reverse Warrant", 
    "Risk Assessment Instrument", 
    "Robotic Device", 
    "Social Media Surveillance", 
    "Stingrays", 
    "Video Surveillance",
    "Shotspotter", 
    "Voice Surveillance"
]
filtered_keywords = ['Facial Recognition Technology', 'DNA Database']
filtered_keywords = [f'"{keyword}"' for keyword in filtered_keywords]
KEYWORDS = filtered_keywords