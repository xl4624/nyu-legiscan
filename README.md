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

setMonitor

sync -> update -> add

Federal is "US" state

There is a bill parameter in getSearch that is not in the API manual but seems to be more consistent when passing in the bill number
