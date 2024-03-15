import os
from dotenv import load_dotenv

load_dotenv()

LEGISCAN_API_KEY = os.getenv("LEGISCAN_API_KEY")
if LEGISCAN_API_KEY is None:
    print("Please add your LEGISCAN_API_KEY variable in your .env file")
    exit(1)
