# E-Commerce Analytics Task Board

Source: [Product requirements](prd/ecommerce-analytics.md). Scope: Phase 1 sales dashboard.

All tasks start as **To do**. Mark a task `[x]` when its checks pass; add **In progress** beside the task you are working on.

## Definition of Done

A milestone is complete when its acceptance criteria are met, the app runs locally with `streamlit run app.py`, and changes are committed with the milestone ID in the commit message.

## M1 — Environment setup and project initialization — Done

Commit: `6e79b35` — M1: set up runnable Streamlit project

- [x] Set up Python 3.11+ with Streamlit, Pandas, and Plotly; record dependencies and local run instructions.
- [x] Initialize a simple, readable project structure with a Streamlit entry point.

Verification (2026-09-16): Python 3.14.7; Streamlit 1.64.0, Pandas 3.0.5,
Plotly 6.9.0, pytest 9.1.1. Installation succeeded and `pip check` reported
no broken requirements. Git ignores `venv/`, `.pytest_cache/`, and `__pycache__/`.
The local server health check returned `ok`. Headless Chrome opened
`http://127.0.0.1:8501/` and confirmed the document title and rendered heading
were "ShopSmart Sales Dashboard", with no Streamlit error or warning elements.
No project tests exist yet; they arrive in M2. The task's local server and temporary
browser sessions were stopped after verification.

Environment notes: the sandbox initially blocked PyPI access and local server/browser
connections; approved retries succeeded. Pip disabled its unwritable cache inside
the sandbox. Streamlit printed an optional Watchdog performance suggestion.
The first browser capture preceded rendering; the subsequent live DOM check passed.
Chrome's screenshot output was blank, so visual pixel inspection was unavailable;
the heading and absence of app alerts were verified from the rendered DOM.

## M2 — Data loading and basic structure — In progress

Commit: `27cac03` — M2: load and validate sales CSV (Task 2; milestone still in progress)

- [x] Load `data/sales-data.csv`; validate the required columns and parse dates, numeric values, and categorical values correctly.
- [ ] Prepare sales totals, transaction counts, and time/category/region aggregations from the CSV.
- [ ] Create the dashboard layout: prominent KPI cards, a sales trend chart, and category/region charts side by side.

Task 2 verification (2026-09-16): the initial pytest run failed with
`ModuleNotFoundError: No module named 'sales_data'`, as expected before implementation.
After adding the loader and connecting the app, `venv/bin/python -m pytest -q`
passed all 18 tests. Headless Chrome confirmed the caption
"Sales recorded from January 03, 2024 to December 31, 2024" with no app error
or warning elements. The source CSV is unchanged. The local server and temporary
browser were stopped after verification. Starting the server required approval
to open a local port; Streamlit printed its optional Watchdog performance suggestion.

M2 remains **In progress**: Task 2 completes loading and validation only.
Its aggregation and full-layout criteria depend on implementation Tasks 3–5.
Stopped before Task 3 for user review.

## M3 — KPI cards implementation

Commit:

- [ ] Display Total Sales (sum of `total_amount`) and Total Orders (transaction count) prominently, with currency formatting and thousands separators. **Acceptance: KPIs visible.**

## M4 — Sales trend chart

Commit:

- [ ] Show correctly aggregated daily or monthly sales in a line chart, with time and sales axes, clear labels, and tooltips showing exact values. **Acceptance: Trend chart works.**

## M5 — Category and region breakdowns

Commit:

- [ ] Show every category in a sales bar chart, sorted highest to lowest, with clear labels and exact-value tooltips. **Acceptance: Category chart works.**
- [ ] Show every region in a sales bar chart, sorted highest to lowest, with clear labels and exact-value tooltips. **Acceptance: Region chart works.**

## M6 — Testing and refinement

Commit:

- [ ] Verify every KPI and chart aggregation against calculations from the CSV. Sample expectations: 482 orders, approximately $116,500 in sales, Electronics as top category, five categories, and North/South/East/West regions. Use CSV calculations for exact values. **Acceptance: Data loads correctly.**
- [ ] Run the dashboard and resolve errors and warnings. **Acceptance: No errors.**
- [ ] Review labels, formatting, and layout for clear, training-free usage and executive presentation. **Acceptance: Professional appearance.**
- [ ] Verify dashboard load within 5 seconds and chart rendering within 2 seconds of data load.
- [ ] Check Chrome, Firefox, Safari, and Edge compatibility without end-user plugins or installations.
- [ ] Review code for readable, modular Python and helpful comments.

## M7 — Deployment to Streamlit Community Cloud

Commit:

- [ ] Deploy the dashboard to Streamlit Community Cloud with the required dependencies and CSV available.
- [ ] Verify the public dashboard loads and its KPIs and charts work; record the shareable URL for stakeholder review.

## Out of scope

Phase 2 work: authentication/access control, database integration, exports, email alerts, filtering/date selection, transaction drill-down, mobile-responsive design, and automated refresh.
