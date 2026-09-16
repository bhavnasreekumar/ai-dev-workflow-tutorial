import csv

import pandas as pd
import pytest

from sales_data import SalesDataError, load_sales_data


COLUMNS = [
    "date", "order_id", "product", "category", "region",
    "quantity", "unit_price", "total_amount",
]
VALID_ROW = ["2024-01-03", "001", "Headphones", "Audio", "North", "2", "5.25", "10.50"]


def write_csv(tmp_path, rows, columns=COLUMNS):
    path = tmp_path / "sales.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(columns)
        writer.writerows(rows)
    return path


def test_load_valid_data_preserves_text_ids(tmp_path):
    data = load_sales_data(write_csv(tmp_path, [VALID_ROW]))
    assert data.loc[0, "order_id"] == "001"
    assert data.loc[0, "date"] == pd.Timestamp("2024-01-03")
    assert data.loc[0, "quantity"] == 2
    assert data.loc[0, "total_amount"] == pytest.approx(10.50, abs=0.001)


def test_missing_file(tmp_path):
    with pytest.raises(SalesDataError, match="Cannot read"):
        load_sales_data(tmp_path / "missing.csv")


@pytest.mark.parametrize("content", ["", ",".join(COLUMNS) + "\n"])
def test_empty_data(tmp_path, content):
    path = tmp_path / "empty.csv"
    path.write_text(content, encoding="utf-8")
    with pytest.raises(SalesDataError, match="no transactions"):
        load_sales_data(path)


def test_missing_column(tmp_path):
    path = write_csv(tmp_path, [VALID_ROW[:-1]], COLUMNS[:-1])
    with pytest.raises(SalesDataError, match="total_amount"):
        load_sales_data(path)


@pytest.mark.parametrize("field,value", [
    ("date", "2024-02-30"), ("date", "01/03/2024"),
    ("date", "2024-1-3"), ("total_amount", "bad"),
    ("total_amount", "NaN"), ("unit_price", "inf"),
    ("quantity", "1.5"), ("region", " "), ("order_id", ""),
])
def test_invalid_values(tmp_path, field, value):
    row = VALID_ROW.copy()
    row[COLUMNS.index(field)] = value
    with pytest.raises(SalesDataError, match=field):
        load_sales_data(write_csv(tmp_path, [row]))


@pytest.mark.parametrize("row", [VALID_ROW[:-1], VALID_ROW + ["extra"]])
def test_wrong_row_length(tmp_path, row):
    with pytest.raises(SalesDataError, match="CSV"):
        load_sales_data(write_csv(tmp_path, [row]))


def test_unclosed_quote(tmp_path):
    path = tmp_path / "malformed.csv"
    path.write_text(",".join(COLUMNS) + '\n"unclosed', encoding="utf-8")
    with pytest.raises(SalesDataError, match="CSV"):
        load_sales_data(path)


def test_extra_columns_are_ignored(tmp_path):
    path = write_csv(tmp_path, [VALID_ROW + ["note"]], COLUMNS + ["notes"])
    assert list(load_sales_data(path).columns) == COLUMNS
