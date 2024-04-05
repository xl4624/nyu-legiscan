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
and save the `credentials.json` and `token.json` file in the root directory.

## Progress

### Fields for Updated Bills

Status/Progress  
Latest History (and date)  
Sine Die (in session or died in chamber)  

### Fields for New Bills

Bill Number  
Status/Progress  
Latest History (and date)  
Title  
Description  
Enactment Date  
...  

### Todo

Use `setMonitor` to update the monitoring list to match our Google Sheet  

Broad workflow of this project:  
sync -> update -> add

Federal/US Congress bills are labeled under "US" state

There is a `bill` parameter in `getSearch` that is not in the API manual. I found it by looking through
their API Client's source code (warning it's in PHP). This seems to be more consistent when passing
in the bill number than `query`. We will likely still use query but probably just to add bills.
