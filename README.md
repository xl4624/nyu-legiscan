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

4. Follow these [quickstart instructions](https://developers.google.com/sheets/api/quickstart/python)
to enable the Google Sheets API: and save the `credentials.json` and `token.json`
file in the root directory.

### Developer Setup

Here is some of the stuff I'm using, feel free to use whatever setup you like.  

- I'm using `pyenv` to manage Python virtualenvs
- I'm using `pyright` lsp and `ruff` lsp/formatter with this line of code inside
`pyproject.toml`

    ```toml
    [tool.ruff]
    line-length = 100
    ```

## Progress

### TODO

- [ ] Making a Google Docs of the technical documentation.
- [x] Adding the rest of the fields to the new bills.
- [x] Run the `add_bills.py` script with >90 relevance score
- [ ] Sync up the copy and the real Google Sheets. (5/17 if needed)

### Notes

We need to break down big keywords down to smaller chunks that are more manageable.
For example, instead of "Artificial intelligence", we might need to add more qualifiers
that specify the context in which we want to search bills related to artificial
intelligence, such as in the context of surveillance, privacy, law enforcement:

- "Artificial Intelligence" AND "surveillance"
- "Artificial Intelligence" AND "privacy"
- "Artificial Intelligence" AND "law enforcement"

probably all at relevance > 90

More things to note:

- There is a `bill` parameter in `getSearch` that is not in the API manual. I
found it by looking through their API Client's source code (warning it's in PHP).
This seems to be more consistent when passing in the bill number than `query`.
We will likely still use `query` when it's time to add bills but this is useful
for searching by bill number.
- Use `setMonitor` to update the monitoring list to match our Google Sheet  
- Broad stages of progress for this project:
  - sync -> update -> add
- Federal/US Congress bills are labeled under "US" state

### Google Sheet

Might want another sheet inside the same Google Sheet with the title and
Legsican URL that Terrance can review as relevant and then once they are marked
relevant, query in `getBill`. Looking back at this, probably not though just
because it would need to run two different scripts. It probably works to do
`getSearch` and then `getBill` and add the relevant bills to the Google Sheet
as "Unreviewed".

## Archived

### Steps to Transition

1. Add `Legiscan Status` and `Legiscan Latest History` columns to the right of
the `Latest Action` column.

2. Add `Legiscan Bill ID` and `Change Hash` to the end of the columns.

3. Modify `Public-View Filter` from

    ```appscript
    =QUERY('Input Form Responses'!A2:W1000, "select B, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U where C = 'Accepted'")
    ```

    to

    ```appscript
    =QUERY('Input Form Responses'!A2:W1000, "select B, E, F, G, H, I, J, K, L, O, P, Q, R, S, T, U, V, W where C = 'Accepted'")
    ```
