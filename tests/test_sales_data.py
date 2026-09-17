import csv
from pathlib import Path

import pandas as pd
import pytest

from sales_data import (
    SalesDataError,
    calculate_kpis,
    load_sales_data,
    monthly_sales,
    sales_by_category,
    sales_by_region,
)


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


def test_kpis_count_transactions_and_use_recorded_amounts():
    data = pd.DataFrame({
        "order_id": ["same", "same", "other"],
        "quantity": [1, 1, 1], "unit_price": [999, 999, 999],
        "total_amount": [10.25, 20.50, 0.25],
    })
    sales, orders = calculate_kpis(data)
    assert sales == pytest.approx(31.00, abs=0.001)
    assert orders == 3


def test_monthly_sales_orders_years_and_fills_missing_months():
    data = pd.DataFrame({
        "date": pd.to_datetime(["2025-01-03", "2024-01-20", "2024-01-02"]),
        "total_amount": [30.0, 10.25, 0.75],
    })
    result = monthly_sales(data)
    assert result["date"].tolist() == list(pd.date_range("2024-01-01", "2025-01-01", freq="MS"))
    assert result["total_amount"].tolist() == [11.0] + [0.0] * 11 + [30.0]
    assert result["total_amount"].sum() == pytest.approx(41.0, abs=0.001)


@pytest.mark.parametrize("column,function", [
    ("category", sales_by_category), ("region", sales_by_region),
])
def test_breakdowns_include_all_groups_and_sort_ties(column, function):
    data = pd.DataFrame({
        column: ["Zeta", "Beta", "Alpha", "Beta"],
        "total_amount": [20.0, 4.0, 10.0, 6.0],
    })
    result = function(data)
    assert result[column].tolist() == ["Zeta", "Alpha", "Beta"]
    assert result["total_amount"].tolist() == [20.0, 10.0, 10.0]
    assert result["total_amount"].sum() == pytest.approx(40.0, abs=0.001)


def test_supplied_csv_matches_known_results():
    path = Path(__file__).resolve().parents[1] / "data" / "sales-data.csv"
    data = load_sales_data(path)
    sales, orders = calculate_kpis(data)
    assert orders == 482
    assert sales == pytest.approx(116500.21, rel=0, abs=0.001)
    assert data["date"].min() == pd.Timestamp("2024-01-03")
    assert data["date"].max() == pd.Timestamp("2024-12-31")
    categories = sales_by_category(data)
    regions = sales_by_region(data)
    assert categories["category"].tolist() == [
        "Electronics", "Wearables", "Audio", "Smart Home", "Accessories",
    ]
    assert categories["total_amount"].tolist() == pytest.approx(
        [42683.67, 23698.23, 19638.44, 19317.23, 11162.64], rel=0, abs=0.001,
    )
    assert regions["region"].tolist() == ["North", "West", "East", "South"]
    assert regions["total_amount"].tolist() == pytest.approx(
        [38857.24, 27463.74, 26783.53, 23395.70], rel=0, abs=0.001,
    )
    trend = monthly_sales(data)
    assert len(trend) == 12
    for totals in [categories, regions, trend]:
        assert totals["total_amount"].sum() == pytest.approx(sales, rel=0, abs=0.001)
