import csv
import math
from pathlib import Path

import pandas as pd


COLUMNS = [
    "date", "order_id", "product", "category", "region",
    "quantity", "unit_price", "total_amount",
]


class SalesDataError(ValueError):
    """A source-data problem the dashboard can explain to its user."""


def load_sales_data(path: str | Path) -> pd.DataFrame:
    try:
        with Path(path).open(newline="", encoding="utf-8-sig") as handle:
            records = list(csv.reader(handle, strict=True))
    except (OSError, UnicodeError) as error:
        raise SalesDataError(
            f"Cannot read {path}. Check that the CSV exists and is readable UTF-8."
        ) from error
    except csv.Error as error:
        raise SalesDataError("Invalid CSV formatting. Correct the file and retry.") from error

    if not records or len(records) == 1:
        raise SalesDataError("The CSV contains no transactions. Add sales rows and retry.")
    header, *rows = records
    missing = [column for column in COLUMNS if column not in header]
    if missing:
        raise SalesDataError(f"Missing CSV columns: {', '.join(missing)}.")
    if len(header) != len(set(header)):
        raise SalesDataError("Duplicate CSV column names. Use unique names.")
    for number, row in enumerate(rows, start=2):
        if len(row) != len(header):
            raise SalesDataError(f"Invalid CSV field count in record {number}.")

    data = pd.DataFrame(rows, columns=header)[COLUMNS].copy()
    for column in COLUMNS:
        blank = data[column].str.strip().eq("")
        if blank.any():
            number = int(blank[blank].index[0]) + 2
            raise SalesDataError(f"Blank {column} in record {number}. Supply a value.")

    date_shape = data["date"].str.fullmatch(r"\d{4}-\d{2}-\d{2}")
    dates = pd.to_datetime(data["date"], format="%Y-%m-%d", errors="coerce")
    bad_dates = ~date_shape | dates.isna()
    if bad_dates.any():
        number = int(bad_dates[bad_dates].index[0]) + 2
        raise SalesDataError(f"Invalid date in record {number}. Use YYYY-MM-DD.")
    data["date"] = dates

    for column in ["quantity", "unit_price", "total_amount"]:
        values = pd.to_numeric(data[column], errors="coerce")
        invalid = ~values.map(math.isfinite)
        if column == "quantity":
            invalid = invalid | values.mod(1).ne(0)
        if invalid.any():
            number = int(invalid[invalid].index[0]) + 2
            rule = "a finite whole number" if column == "quantity" else "a finite number"
            raise SalesDataError(f"Invalid {column} in record {number}. Use {rule}.")
        data[column] = values
    return data


def calculate_kpis(data: pd.DataFrame) -> tuple[float, int]:
    return float(data["total_amount"].sum()), len(data)


def monthly_sales(data: pd.DataFrame) -> pd.DataFrame:
    return (
        data.set_index("date")["total_amount"]
        .resample("MS").sum().reset_index()
    )


def _sales_by(data: pd.DataFrame, column: str) -> pd.DataFrame:
    return (
        data.groupby(column, as_index=False)["total_amount"].sum()
        .sort_values(["total_amount", column], ascending=[False, True])
        .reset_index(drop=True)
    )


def sales_by_category(data: pd.DataFrame) -> pd.DataFrame:
    return _sales_by(data, "category")


def sales_by_region(data: pd.DataFrame) -> pd.DataFrame:
    return _sales_by(data, "region")
