# Sales Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task, inline in the current session. Steps use checkbox (`- [ ]`) syntax for tracking. Do not execute until the user explicitly authorizes implementation; stop at the end of each authorized milestone.

**Goal:** Build a clear, correct sales dashboard from the supplied CSV, ready for the user to deploy.

**Architecture:** `sales_data.py` loads, validates, and summarizes the CSV independently of the UI. `app.py` uses those results to display two metrics and three Plotly charts through Streamlit. Invalid input stops the dashboard before it presents any results.

**Tech Stack:** Python 3.11+, Streamlit, Pandas, Plotly, pytest; plain `venv/` and `requirements.txt`.

**Spec:** [Approved design](../specs/2026-09-15-sales-dashboard-design.md).

## Global Constraints

- Work in the existing checkout on `feature/sales-dashboard`; do not create a worktree.
- Use Python 3.11+, Streamlit, Pandas, and Plotly, with pytest for calculation and validation tests.
- Use a plain virtual environment in `venv/` and record dependencies in `requirements.txt`; do not use uv or conda.
- Use two application modules: `app.py` for presentation and `sales_data.py` for data loading, validation, and calculations.
- Aggregate the trend by calendar month.
- Show a clear error and stop when the CSV is missing or invalid. Never silently discard invalid rows or display partial totals.
- Preserve `data/sales-data.csv` and existing tutorial documentation.
- Title: **ShopSmart Sales Dashboard**. Use the approved layout and currency formatting.
- Keep the board's M1–M7 IDs; plan task numbers below are separate. Include milestone IDs in implementation commit messages.
- All code blocks below are instructions for future implementation, not code to execute during planning.
- Deployment is the final step, executed by the user from `main` after review and merge. No deployment, merge, or push is part of creating this plan.
- Keep execution inline for learning and wait for an explicit implementation go-ahead after plan review.
- Exclude authentication, database integration, exports, alerts, filters/date selection, drill-down, dedicated mobile design, and automated refresh.

## Files and interfaces

| File | Action and purpose |
| --- | --- |
| `app.py` | Create: layout, formatted metrics, charts, and user-facing errors. |
| `sales_data.py` | Create: CSV validation and pure calculation functions. |
| `tests/test_sales_data.py` | Create: meaningful data/validation tests, independent of Streamlit. |
| `requirements.txt` | Create: installable, verified dependency versions. |
| `README.md` | Append setup, run, test, and deployment instructions; preserve existing content. |
| `TASKS.md` | Add the shared completion standard and commit records; update progress only as work is performed. |
| `docs/verification/sales-dashboard.md` | Create during M6: actual acceptance/performance/browser results and limitations. |
| `.gitignore` | Already covers `venv/`, `__pycache__/`, and `.pytest_cache/`; verify without unnecessary edits. |

Data module interfaces (all calculation inputs are already validated):

- `SalesDataError(ValueError)`: expected data problem safe to explain to the user.
- `load_sales_data(path: str | Path) -> pd.DataFrame`: eight required columns, parsed dates/numbers, text IDs preserved.
- `calculate_kpis(data: pd.DataFrame) -> tuple[float, int]`: total sales and transaction count.
- `monthly_sales(data: pd.DataFrame) -> pd.DataFrame`: columns `date`, `total_amount`; chronological month-start dates, zero-filled intervening months.
- `sales_by_category(data: pd.DataFrame) -> pd.DataFrame`: `category`, `total_amount`; descending sales, alphabetical ties.
- `sales_by_region(data: pd.DataFrame) -> pd.DataFrame`: `region`, `total_amount`; same ordering rule.

## Task 1 — Runnable project setup [M1]

**Files:** Create `requirements.txt`, `app.py`; update `README.md`, `TASKS.md`. **Verification:** setup and manual launch; no test-first cycle needed for scaffolding.

**Interfaces:** Produces a runnable `app.py` and an isolated Python environment for all later tasks.

- [ ] Check `git status --short --branch` and `python3 --version`. Stay on the existing feature branch and preserve unrelated work. Confirm Python is at least 3.11 before installing packages.
- [ ] Mark M1 **In progress** on the existing board. Add a shared Definition of Done: acceptance criteria met, app runs locally with `streamlit run app.py`, changes committed with the milestone ID. Add a blank `Commit:` line to each M1–M7 section; keep all unfinished checkboxes unchecked.
- [ ] Create `requirements.txt` initially containing:

```text
streamlit>=1.63,<2
pandas>=2.2,<4
plotly>=5,<7
pytest>=8,<10
```

- [ ] Create and install into the environment, then check package compatibility:

```bash
python3 -m venv venv
venv/bin/python -m pip install -r requirements.txt
venv/bin/python -m pip check
git check-ignore venv/ .pytest_cache/ __pycache__/
```

Expected: installation succeeds, pip reports no broken requirements, all three generated directories are ignored. If installation fails, resolve it before proceeding. Do not claim dependency compatibility based solely on the ranges above.

- [ ] Record the four installed versions and replace the ranges with those exact `==` versions in `requirements.txt`. Obtain them with:

```bash
venv/bin/python -m pip show streamlit pandas plotly pytest
```

- [ ] Create this minimal `app.py`:

```python
import streamlit as st

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
st.title("ShopSmart Sales Dashboard")
```

- [ ] Append a **Run the sales dashboard** section to README with Python 3.11+ prerequisites and these commands. State that test files arrive in M2 and the app currently shows its title only. Include the Windows activation equivalent `venv\Scripts\activate`.

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
# Once tests exist:
python -m pytest -q
```

- [ ] Launch `venv/bin/python -m streamlit run app.py`, open its reported local URL, and verify the title appears without errors or warnings. Record Python/package versions and any environment problems. Stop only the server started for this task when finished.
- [ ] Commit the deliverable:

```bash
git add app.py requirements.txt README.md TASKS.md
git commit -m "M1: set up runnable Streamlit project"
```

- [ ] Record the actual commit hash under M1, check its accepted criteria, and commit the board update with `M1: record setup completion`. Stop for the user's milestone review.

## Task 2 — Load and validate CSV, then connect the app [M2, test-first]

**Files:** Create `sales_data.py`, `tests/test_sales_data.py`; update `app.py`, `TASKS.md`.

**Interfaces:** Produces `SalesDataError` and `load_sales_data(path)`. The returned frame has parsed `date`, numeric `quantity`/`unit_price`/`total_amount`, and string identifiers/categories.

- [ ] Mark M2 in progress. Create these tests first. `write_csv` creates temporary test data; it never edits the real CSV.

```python
import csv
from pathlib import Path

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
```

- [ ] Run `venv/bin/python -m pytest tests/test_sales_data.py -q`. Expected: collection fails because `sales_data` does not exist yet. Explain one test to the user before implementing.
- [ ] Create `sales_data.py` with this loading/validation logic. Standard-library CSV parsing ensures malformed row lengths are rejected before Pandas calculations.

```python
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
```

- [ ] Run `venv/bin/python -m pytest tests/test_sales_data.py -q`. Expected: all loader tests pass. Fix failures rather than weakening expectations.
- [ ] Add `from pathlib import Path` and `from sales_data import SalesDataError, load_sales_data` to the app imports. After its title, add:

```python
try:
    data = load_sales_data(Path(__file__).resolve().parent / "data" / "sales-data.csv")
except SalesDataError as error:
    st.error(str(error))
    st.stop()

start = data["date"].min().strftime("%B %d, %Y")
end = data["date"].max().strftime("%B %d, %Y")
st.caption(f"Sales recorded from {start} to {end}")
```

- [ ] Launch the app and confirm the January 3–December 31, 2024 period appears. Commit with `M2: load and validate sales CSV` after staging only `sales_data.py`, `tests/test_sales_data.py`, `app.py`, and `TASKS.md`.
- [ ] Leave M2 open until its aggregation/layout requirements are fulfilled in Tasks 3–5. Record this dependency on the board; do not mark planned calculations complete. Stop for milestone review.

## Task 3 — Calculate and display KPI cards [M3; contributes to M2, test-first]

**Files:** Update `sales_data.py`, `tests/test_sales_data.py`, `app.py`, `TASKS.md`.

**Interfaces:** Consumes validated data; produces `calculate_kpis(data) -> tuple[float, int]`.

- [ ] Mark M3 in progress. Add `calculate_kpis` to the test import and add:

```python
def test_kpis_count_transactions_and_use_recorded_amounts():
    data = pd.DataFrame({
        "order_id": ["same", "same", "other"],
        "quantity": [1, 1, 1], "unit_price": [999, 999, 999],
        "total_amount": [10.25, 20.50, 0.25],
    })
    sales, orders = calculate_kpis(data)
    assert sales == pytest.approx(31.00, abs=0.001)
    assert orders == 3
```

- [ ] Run `venv/bin/python -m pytest tests/test_sales_data.py -k kpis -q`. Expected: missing-function import failure. Explain that duplicate IDs still count as separate transactions, and recorded amounts are authoritative.
- [ ] Add the function to `sales_data.py`:

```python
def calculate_kpis(data: pd.DataFrame) -> tuple[float, int]:
    return float(data["total_amount"].sum()), len(data)
```

- [ ] Run `venv/bin/python -m pytest -q`; expected: all tests pass.
- [ ] Import `calculate_kpis` in `app.py` and add after the date caption:

```python
total_sales, total_orders = calculate_kpis(data)
sales_column, orders_column = st.columns(2)
sales_column.metric("Total Sales", f"${total_sales:,.2f}")
orders_column.metric("Total Orders", f"{total_orders:,}")
```

- [ ] Launch the app; verify `$116,500.21` and `482` are prominent. Commit with `M3: calculate and display sales KPIs`, recording the passing tests and actual completion commit under M3 in a separate board update. Stop for review.

## Task 4 — Monthly sales trend [M4; contributes to M2, test-first]

**Files:** Update `sales_data.py`, `tests/test_sales_data.py`, `app.py`, `TASKS.md`.

**Interfaces:** Produces `monthly_sales(data)` with `date` month-start timestamps and numeric `total_amount`.

- [ ] Mark M4 in progress. Import `monthly_sales` in the tests and add:

```python
def test_monthly_sales_orders_years_and_fills_missing_months():
    data = pd.DataFrame({
        "date": pd.to_datetime(["2025-01-03", "2024-01-20", "2024-01-02"]),
        "total_amount": [30.0, 10.25, 0.75],
    })
    result = monthly_sales(data)
    assert result["date"].tolist() == list(pd.date_range("2024-01-01", "2025-01-01", freq="MS"))
    assert result["total_amount"].tolist() == [11.0] + [0.0] * 11 + [30.0]
    assert result["total_amount"].sum() == pytest.approx(41.0, abs=0.001)
```

- [ ] Run `venv/bin/python -m pytest tests/test_sales_data.py -k monthly -q`; expected: missing-function import failure.
- [ ] Add to `sales_data.py`:

```python
def monthly_sales(data: pd.DataFrame) -> pd.DataFrame:
    return (
        data.set_index("date")["total_amount"]
        .resample("MS").sum().reset_index()
    )
```

- [ ] Run the full pytest suite; expected: pass. Monthly resampling uses the documented Pandas [resample API](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.resample.html).
- [ ] Import `plotly.express as px` and `monthly_sales` in `app.py`; add after the metrics:

```python
st.subheader("Monthly Sales Trend")
trend = px.line(
    monthly_sales(data), x="date", y="total_amount", markers=True,
    labels={"date": "Month", "total_amount": "Sales ($)"},
    color_discrete_sequence=["#2563EB"],
)
trend.update_traces(hovertemplate="%{x|%B %Y}<br>Sales: $%{y:,.2f}<extra></extra>")
trend.update_xaxes(dtick="M1", tickformat="%b %Y")
trend.update_yaxes(tickprefix="$", tickformat=",.0f")
st.plotly_chart(trend, width="stretch", config={"displayModeBar": False})
```

Use `width="stretch"` per the current [Streamlit chart API](https://docs.streamlit.io/develop/api-reference/charts/st.plotly_chart); avoid deprecated `use_container_width`.

- [ ] Launch the app; verify 12 chronological monthly points for the sample, clear axes, and dollar/cents hover values. Commit with `M4: add monthly sales trend`, record M4 completion, and stop for review.

## Task 5 — Category and region breakdowns [M5; completes M2, test-first]

**Files:** Update `sales_data.py`, `tests/test_sales_data.py`, `app.py`, `TASKS.md`.

**Interfaces:** Produces `sales_by_category(data)` and `sales_by_region(data)`, each returning a two-column sorted frame. A private helper shares the grouping operation.

- [ ] Mark M5 in progress. Import both functions in the tests and add:

```python
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
```

- [ ] Run `venv/bin/python -m pytest tests/test_sales_data.py -k breakdowns -q`; expected: missing-function import failure.
- [ ] Add these functions to `sales_data.py`:

```python
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
```

- [ ] Run the full pytest suite; expected: pass.
- [ ] Import the two public functions in `app.py`; add below the monthly chart:

```python
category_column, region_column = st.columns(2)
for container, dimension, totals, title in [
    (category_column, "category", sales_by_category(data), "Sales by Category"),
    (region_column, "region", sales_by_region(data), "Sales by Region"),
]:
    with container:
        st.subheader(title)
        figure = px.bar(
            totals, x="total_amount", y=dimension, orientation="h",
            labels={"total_amount": "Sales ($)", dimension: dimension.title()},
            category_orders={dimension: totals[dimension].tolist()},
            color_discrete_sequence=["#2563EB"],
        )
        figure.update_traces(hovertemplate="%{y}<br>Sales: $%{x:,.2f}<extra></extra>")
        figure.update_xaxes(tickprefix="$", tickformat=",.0f")
        st.plotly_chart(figure, width="stretch", config={"displayModeBar": False})
```

- [ ] Launch the app. Verify five categories and four regions, largest bars at the top, exact-value tooltips, consistent colors, and the approved side-by-side arrangement. Electronics should lead categories; North should lead regions. Correct visual order if manual inspection disagrees with the intended order.
- [ ] Commit with `M5 M2: complete breakdown charts and dashboard structure`. Verify all M2 loading/aggregation/layout criteria now hold, record completion hashes for M2 and M5, and commit the board update. Stop for review.

## Task 6 — Acceptance verification and refinement [M6]

**Files:** Update `tests/test_sales_data.py`, `README.md`, `TASKS.md`; create `docs/verification/sales-dashboard.md`. Modify app/data code only to fix observed failures.

**Interfaces:** Consumes all five public data functions and the complete app; produces evidence for the PRD's acceptance criteria. This task adds a regression check, not new product behavior.

- [ ] Mark M6 in progress. Add the sample-data regression test below. Imports for all referenced functions were introduced above.

```python
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
```

- [ ] Run `venv/bin/python -m pytest -q -W error` and `venv/bin/python -m pip check`. Expected: all tests pass without warnings and no dependency conflicts. Investigate failures before claiming acceptance.
- [ ] Verify the error screen without modifying the real CSV. Run this temporary, in-memory app check from the repository root, using Streamlit's documented [AppTest API](https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest):

```bash
venv/bin/python - <<'PY'
from pathlib import Path
from unittest.mock import patch
from streamlit.testing.v1 import AppTest
from sales_data import SalesDataError

for message in ["Cannot read sales CSV.", "Invalid total_amount in record 2."]:
    with patch("sales_data.load_sales_data", side_effect=SalesDataError(message)):
        app = AppTest.from_file(Path("app.py").resolve()).run()
    assert not app.exception
    assert len(app.error) == 1
    assert app.error[0].value == message
    assert not app.metric
    assert not app.get("plotly_chart")
print("Both error paths stop before displaying results.")
PY
```

- [ ] Launch the complete app and manually check each PRD acceptance criterion: visible KPIs, correct monthly line, correctly sorted category/region charts, values matching the CSV, no runtime errors/warnings, and professional appearance. Inspect hover values and date labels. Confirm no filters or unsupported Phase 2 features appeared.
- [ ] Check the app in Chrome, Firefox, Safari, and Edge. Record browser/version, date, outcome, and any unavailable browser in `docs/verification/sales-dashboard.md`. An unavailable browser remains an outstanding check; do not mark M6 fully done until required checks are completed.
- [ ] Measure local performance using a browser Performance recording: start recording before navigation, identify page navigation start, the WebSocket update that delivers dashboard elements, and the frame where all metrics/charts are visible. Record navigation-to-visible time against 5 seconds, and element-arrival-to-all-charts-visible against 2 seconds. The second interval measures browser rendering after server-side data work and delivery; it is not an exact Python CSV-load timestamp. Record that limitation explicitly. Repeat three loads, record each result, and distinguish first load from warm loads. Do not substitute server startup time for browser rendering time.
- [ ] Record all actual results in `docs/verification/sales-dashboard.md`: environment/versions, test command and result, seven acceptance outcomes, error-path outcomes, four browser outcomes, timing method and measurements, unresolved checks. Include a PRD-to-evidence table; use observed results, never prefilled passing claims.
- [ ] Review code for small readable functions, helpful comments, and correct app-relative paths. Verify `git diff -- data/sales-data.csv` is empty. Fix observed defects with a failing data test first when appropriate; rerun affected checks after fixes.
- [ ] Update README to describe the finished layout, sample totals, CSV requirements, explicit error-and-stop policy, monthly grouping, test command, and the fact that the data is a static snapshot. Remove the temporary M1 note saying only the title exists.
- [ ] Commit the checked result with `M6: verify dashboard acceptance and document results`. Stage only changed project files. Record the commit and close M6 only when its checks are complete; otherwise report the specific outstanding checks. Stop for user review.

## Task 7 — Review and prepare the deployment handoff [M7 preparation]

**Files:** Update `README.md`, `TASKS.md`; review the verification record and branch diff. **Interfaces:** Produces a reviewed handoff; does not publish the app.

- [ ] Review `git diff main...HEAD` and the M1–M6 evidence with the user, explaining what each application module does. Resolve actual review findings and rerun checks affected by changes. Use the repository's actual base branch if it differs from `main`, resolving that discrepancy before deployment.
- [ ] Add README deployment instructions: user signs in to Streamlit Community Cloud, chooses this GitHub repository, `main`, and entry point `app.py`, selects a Python runtime matching the tested supported local version, deploys, verifies the public URL, and records it on the board. Explain that `requirements.txt` and `data/sales-data.csv` must be committed. Follow the [official deployment guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app).
- [ ] Confirm `venv/`, test caches, and secrets are untracked; commit the handoff documentation with `M7: document user deployment handoff`. Leave M7 deployment checkboxes unchecked.
- [ ] Report branch readiness and let the user control review/merge/push using the tutorial's workflow. Do not merge or push merely because this plan exists. After that workflow, verify the reviewed changes are present on remote `main` before the user starts Task 8.

## Task 8 — Deploy and verify the public dashboard [M7, USER-EXECUTED FINAL STEP]

**Owner:** User. **Files/records:** Public app URL, `TASKS.md`, and deployment observations. **Prerequisite:** Reviewed implementation merged and pushed to `main`.

**Agent handoff:** Stop automated execution here. The user performs the following deployment actions with their own accounts.

- [ ] In Streamlit Community Cloud, deploy the repository's `main` branch with `app.py` as the entry point and the tested supported Python runtime. Confirm dependencies install and the deployed app reads the committed CSV.
- [ ] Open the shareable URL in a private/logged-out browser window. Confirm public access, `$116,500.21`, `482` orders, monthly trend, five categories, four regions, descending bars, and working hover values. Check deployment logs for errors/warnings.
- [ ] Check hosted load behavior and record observed startup/network delays separately from local timings. Resolve deployment failures before marking M7 done.
- [ ] Record the public URL and deployed Git commit under M7, mark its accepted criteria complete, and commit/push the board update using the tutorial workflow. This finishes the plan.

## Review checklist for the user

- Every plan task identifies its M1–M7 milestone, independently of task numbering.
- Tasks 2–5 follow failing test → minimal implementation → passing test.
- M2 stays open until its calculations and layout are actually complete.
- The board records deliverables; this plan records implementation steps.
- Your deployment is the last step, after review and merge.
- Approval of this plan alone does not begin coding; give a separate go-ahead for the milestone you want to start.
