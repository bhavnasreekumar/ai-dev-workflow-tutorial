# How to work with me

I'm learning. Before you change anything, say in a sentence or two what
you're about to do and why. After each change, explain what you did in
plain language and point out anything I should read or decide. Keep code
simple and readable.

# ShopSmart Sales Dashboard

This repository contains the Phase 1 ShopSmart sales dashboard from the
e-commerce analytics PRD. It is a Streamlit app backed by the static CSV
snapshot at `data/sales-data.csv`.

## Run and test

Use Python 3.11 or newer. From the repository root:

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
python -m pytest -q -W error
```

The app runs locally at the URL printed by Streamlit. The public deployment is
available at:

https://bhavnasreekumar-ai-dev-workflow-tutorial-app-bixwct.streamlit.app/

## Project structure

- `app.py` owns the Streamlit page, layout, KPI cards, charts, and user-facing
  error display.
- `sales_data.py` loads and validates the CSV and calculates KPI, monthly,
  category, and region summaries.
- `tests/test_sales_data.py` tests validation and calculations independently of
  the Streamlit interface.
- `data/sales-data.csv` is the source snapshot and must remain unchanged unless
  the requirements explicitly change.
- `TASKS.md` records milestone status, verification evidence, and commit links.
- `docs/verification/sales-dashboard.md` records acceptance and Chrome review
  evidence.
- `docs/superpowers/specs/` and `docs/superpowers/plans/` contain the approved
  design and implementation plan.

## Data and behavior

The required CSV columns are `date`, `order_id`, `product`, `category`,
`region`, `quantity`, `unit_price`, and `total_amount`. Dates use `YYYY-MM-DD`;
numeric fields must be finite, quantity must be a whole number, and required
cells cannot be blank. Extra columns are ignored and text identifiers remain
text.

Sales use the recorded `total_amount`. Total Orders counts transaction rows,
including repeated order IDs. Monthly totals keep years separate and fill
intervening months with zero. Category and region bars include every group and
are sorted by descending sales with alphabetical tie breaks.

Invalid, missing, empty, or malformed input must show a clear error and stop the
app before any metrics or charts render. Do not silently drop invalid rows or
show partial results. Resolve the CSV path relative to `app.py`.

## Lessons

- Preserve the supplied CSV and verify calculations independently from the UI;
  the recorded `total_amount` and transaction-row count are the source of truth.
- Keep validation and calculations in `sales_data.py`, and keep Streamlit
  presentation and error handling in `app.py`.
- Check the rendered dashboard in a browser after automated tests; tests alone
  do not prove chart order, labels, hover values, or layout.
- Keep deployment user-controlled: deploy the reviewed implementation from
  GitHub `main` with `requirements.txt` and `data/sales-data.csv` committed.
- Treat the supplied data as a static snapshot; do not add filters, refresh,
  authentication, exports, alerts, or other Phase 2 features without a new
  requirement.
