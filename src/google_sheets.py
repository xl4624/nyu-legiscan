import os.path
from typing import List, Optional

import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class GoogleSheetsAPI:
    # If modifying these scopes, delete the file token.json.
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

    # The ID and range of the spreadsheet.
    # SPREADSHEET_ID = "1DBmf-9UObut_uh9i9GtEP7_hciqzd6uLMqPPKU9B0MA"  # Real Google Sheet
    SPREADSHEET_ID = "15xeV_rgcHNYVUydU31fre8HZ19aIC7V3jLWuvW1rScI"  # Copy of Google Sheet
    RANGE_NAME = "Input Form Responses!A1:AD"

    def __init__(
        self,
        spreadsheet_id: Optional[str] = None,
        range_name: Optional[str] = None,
        scopes: Optional[List[str]] = None,
    ):
        self.spreadsheet_id = spreadsheet_id if spreadsheet_id else self.SPREADSHEET_ID
        self.range_name = range_name or self.RANGE_NAME
        self.scopes = scopes or self.SCOPES
        self.creds = self._authenticate()

    def read_sheet(self) -> pd.DataFrame:
        service = build("sheets", "v4", credentials=self.creds)
        sheet = service.spreadsheets()
        result = (
            sheet.values().get(spreadsheetId=self.spreadsheet_id, range=self.range_name).execute()
        )
        values = result.get("values", [])
        if not values:
            raise ValueError("No data found")

        # Append None
        header = values[0]
        data_rows = [row + [None] * (len(header) - len(row)) for row in values[1:]]

        return pd.DataFrame(data_rows, columns=header)

    def update_data(self, df: pd.DataFrame) -> None:
        service = build("sheets", "v4", credentials=self.creds)
        data = [df.columns.tolist()] + df.values.tolist()
        body = {"values": data}
        result = (
            service.spreadsheets()
            .values()
            .update(
                spreadsheetId=self.spreadsheet_id,
                range=self.range_name,
                valueInputOption="USER_ENTERED",
                body=body,
            )
            .execute()
        )
        print(f"{result.get('updatedCells')} cells updated.")

    def _authenticate(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", self.scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", self.scopes)
                creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

        return creds
