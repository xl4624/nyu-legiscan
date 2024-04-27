# Script to remove duplicate rows from the Google Sheet. Can be used if a previous script
# accidentally added duplicate rows and we need to clean up the data.

import pandas as pd

from src.google_sheets import GoogleSheetsAPI


def main():
    sheet = GoogleSheetsAPI()
    df = sheet.read_sheet()
    original_len = df.shape[0]

    # Ensure 'Legiscan Bill ID' is treated as a string to avoid any data type issues.
    df["Legiscan Bill ID"] = df["Legiscan Bill ID"].apply(
        lambda x: "" if pd.isna(x) or x == "None" else str(x)
    )

    seen_ids = set()
    rows_to_keep = []
    for idx, row in df.iterrows():
        bill_id = row["Legiscan Bill ID"]
        if bill_id == "" or bill_id == "None":  # Keep rows with empty or 'None' IDs.
            rows_to_keep.append(idx)
        elif bill_id not in seen_ids:
            seen_ids.add(bill_id)
            rows_to_keep.append(idx)

    # Create a new DataFrame with the rows we want to keep.
    df = df.loc[rows_to_keep]

    # Add empty rows to the end of the DataFrame to clear out the rest of the data.
    len_diff = original_len - df.shape[0]
    if len_diff > 0:
        empty_rows = [{col: "" for col in df.columns} for _ in range(len_diff)]
        empty_df = pd.DataFrame(empty_rows)
        df = pd.concat([df, empty_df], ignore_index=True)

    sheet.update_data(df)


if __name__ == "__main__":
    main()
