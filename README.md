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
Current progress when running `python quickstart.py`. We can now read data from the Google Sheets using the Google Sheets API and here is an example row:  
<img width="1431" alt="image" src="https://github.com/xl4624/nyu-legiscan/assets/116298054/7983c7e3-f518-46f2-a48c-0bfdca176853">

Soon we should be able to load this data into a pandas dataframe and compare certain row values to our monitor list's from the LegiScan API.

