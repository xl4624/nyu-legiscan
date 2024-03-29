import os
from dotenv import load_dotenv

load_dotenv()

LEGISCAN_API_KEY = os.getenv("LEGISCAN_API_KEY")
if LEGISCAN_API_KEY is None:
    print("Please add the LEGISCAN_API_KEY variable to your .env file")
    exit(1)
