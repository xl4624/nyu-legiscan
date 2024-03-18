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

So far, we have Legiscan and Google Sheets bills matched by Bill Number.

### List of Unmatched Legiscan API Monitor List Bills

By Bill Number (24):
```
AB1814
SB00003
SB974
SB1180
HB3026
SB3423
HB3199
HB1563
HF43
LD949
SB762
HF4235
SF954
HF2532
SB401
A06787
A01880
S02308
S02615
S03281
A04423
A04967
A05517
S06224
```

### List of Bills that have multiple entries in the Google Sheets

By Bill Number (10):
```
AB793
SB1085
SB176
HB626
HB483
HB1585
HB259
HB33
SB169
H4024
```
