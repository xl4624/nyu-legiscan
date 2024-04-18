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
4. Follow these quickstart instructions to enable the Google Sheets API: https://developers.google.com/sheets/api/quickstart/python and save the `credentials.json` and `token.json` file in the root directory.

## Progress

### Fields for New Bills

Fields that we might be able to populate when adding bills

Bill Number  
Status/Progress  
Latest History (and date)  
Title  
Description  
Enactment Date  
...  


## TODO

Interesting read from the Legiscan Client (might be useful)

Search (National)

This mode will synchronize the results of searches ran against the national database. To specify the searches edit the config.php and add each search to the searches[] setting.

The searches will also be filtered by the global relevance cutoff setting, which can be overridden on a per search basis by prepending a different score and the pipe | character. In addition a state abbreviations can also be prefixed to override either national or state search. When used with a relevance override the state should appear first separated by a comma ,.

Also notice that the entire search string should be quoted, and any internal quotes should be escaped as \".

searches[] = "gender AND bathroom"
searches[] = "\"national popular vote\""
searches[] = "42|hemp OR cannabis OR marijuana"
searches[] = "NY|charter ADJ schools"
searches[] = "CA,60|vaccination AND status:passed"

## Archived

### Steps to Transition
1. Add `Legiscan Status` and `Legiscan Latest History` columns to the right of the L. `Latest Action` column.
2. Add `Legiscan Bill ID` and `Change Hash` to the end of the columns.
3. Modify `Public-View Filter` from
```
=QUERY('Input Form Responses'!A2:W1000, "select B, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U where C = 'Accepted'")
```
to
```
=QUERY('Input Form Responses'!A2:W1000, "select B, E, F, G, H, I, J, K, L, O, P, Q, R, S, T, U, V, W where C = 'Accepted'")
```

### Things to Note

- There is a `bill` parameter in `getSearch` that is not in the API manual. I found it by looking through their API Client's source code (warning it's in PHP). This seems to be more consistent when passing in the bill number than `query`. We will likely still use query but this is useful for searching by bill number.
- Use `setMonitor` to update the monitoring list to match our Google Sheet  
- Broad workflow of this project:  
    - sync -> update -> add
- Federal/US Congress bills are labeled under "US" state
