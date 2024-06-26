import os
import datetime
from tzlocal import get_localzone
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

COPY_SPREADSHEET_ID = "1DBmf-9UObut_uh9i9GtEP7_hciqzd6uLMqPPKU9B0MA"
COPY_SPREADSHEET_ID = "15xeV_rgcHNYVUydU31fre8HZ19aIC7V3jLWuvW1rScI"
COPY_SPREADSHEET_ID = "19_D-eZL31ThVDAghXH5rGmzkJY0J8b0-Fs2QVpPidSM"
SPREADSHEET_ID = "1DBmf-9UObut_uh9i9GtEP7_hciqzd6uLMqPPKU9B0MA"
# COPY_SPREADSHEET_ID = SPREADSHEET_ID # live spreadsheet id

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
    '"Driver\'s License Data"',
    '"Drones"',
    '"Electronic Communication"',
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

zero_value_keywords = [
    "Acoustic Gunshot Detection",
    "Cell Phone Location Data",
    "Child Data Collection",
    "Child Data Surveillance",
    "Driver's License Data",
    "Geofence Warrant",
    "Predictive Algorithm",
    "Prison Surveillance",
    "National Security Electronic Surveillance",
    "Reproductive Health Surveillance Data",
    "School Surveillance"
]



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

''''
Aerial Drones
Aerial Surveillance
Artificial Intelligence
Automated Decision Tool/System
Automated License Plate Readers (ALPRs)
Biometric Surveillance (excluding Facial Recognition)
Biometric Surveillance (including Facial Recognition)
Body Worn Cameras
Cell Site Simulators
Consumer Privacy/Consumer Data
Public Health Data
Data Broker
DNA Analysis/DNA Database/Genetic Data
Electronic Communication
Electronic Monitoring/Electronic Tracking
Electronic Tolling Data
Encryption
Facial Recognition
Geofencing
Gunshot Detection
Identification and Credentials
Immigration Surveillance
Geolocation/Location Data
National Security Surveillance
Personal Data
Predictive Policing
Prison Surveillance/Data
Public Health Data/Surveillance
Radio Frequency Identification Devices
Reproductive Health Data/Surveillance
Robotic Device
Satellite Imagery
Social Media/Network Analysis
Social Media (general)
Street-Level Surveillance
Tracking Devices
Video Surveillance
Reverse/Key Word Search/Warrant
Driver's License/Traffic Enforcement
Genetic data
Digital Records
Student Data/Data, Technology & Schools
Gov't Data Infrastructure
Risk Assessment Instrument
Procurement Policy
Criminal Justice/Gang Database
Automated Decision Systems
Automated Decision Making
Biometric Data
Biometric Information
Consumer Health Data
Consumer Data Privacy
DNA Phenotyping
Forensic Investigative Genetic Genealogy
Foreign Intelligence Surveillance Act
IMSI catchers
Rapid DNA


'''