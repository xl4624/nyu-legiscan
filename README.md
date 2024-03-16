# nyu-legiscan

## Setup
1. Clone repository 
2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Create a `.env` file in the root directory and add the following:
```bash
LEGISCAN_API_KEY=your_api_key_here
```
4. Follow these quickstart instructions to enable the Google Sheets API: https://developers.google.com/sheets/api/quickstart/python
and save the `credentials.json` file in the root directory.

## Legiscan API Client Progress
Example output using `client.get_monitor_list()`
<img width="1440" alt="image" src="https://github.com/xl4624/nyu-legiscan/assets/116298054/cab49bfa-eb1f-4086-a7b0-a5986a7316fe">


## Google Sheets Progress
Example output using `python quickstart.py`. Data is taken from the Example Spreadsheet provided by Google Sheets API Quickstart Guide, but we can modify it to read from and write to our spreadsheets.  
<img width="292" alt="image" src="https://github.com/xl4624/nyu-legiscan/assets/116298054/2fc77236-3da5-4c1d-a2cd-645439b5946b">

