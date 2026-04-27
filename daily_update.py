"""
daily_update.py — write a daily value to the Interview Dashboard Google Sheet.

Auth: gspread OAuth (uses ~/.config/gspread/credentials.json + token cache).
Spreadsheet: 1Lf0jBFtz8jZ_yTRrcZ3xQl-9-uN0c-mu7YijyCpJS5w
Worksheet:   Daily Tracker
Column:      J  (column 10)
Row formula: 6 + (target_date - date(2026, 1, 1)).days
"""

import argparse
from datetime import date

import gspread


SPREADSHEET_ID = "1Lf0jBFtz8jZ_yTRrcZ3xQl-9-uN0c-mu7YijyCpJS5w"
WORKSHEET_NAME = "Daily Tracker"
COLUMN_J = 10
BASE_DATE = date(2026, 1, 1)
BASE_ROW = 6


def row_for(target_date: date) -> int:
    return BASE_ROW + (target_date - BASE_DATE).days


def write_daily_update(value: str, target_date: date) -> None:
    gc = gspread.oauth()
    sh = gc.open_by_key(SPREADSHEET_ID)
    ws = sh.worksheet(WORKSHEET_NAME)
    row = row_for(target_date)
    ws.update_cell(row, COLUMN_J, value)
    print(f"Written to row {row}, column J: {value!r}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Write a daily update to the Google Sheet.")
    parser.add_argument("value", help="Value to write into column J for the target date.")
    parser.add_argument(
        "--date",
        default=str(date.today()),
        help="Target date in YYYY-MM-DD format (default: today).",
    )
    args = parser.parse_args()

    target_date = date.fromisoformat(args.date)
    write_daily_update(args.value, target_date)


if __name__ == "__main__":
    main()
