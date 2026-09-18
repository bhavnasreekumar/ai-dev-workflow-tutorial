# ShopSmart Sales Dashboard — Design

Date: 2026-09-15

Status: Written specification approved by the user. Implementation is complete.

## Purpose and scope

Build the Phase 1 dashboard described in [the PRD](../../../prd/ecommerce-analytics.md), tracked in [TASKS.md](../../../TASKS.md), following Section 2 of [the Part 2 tutorial](../../../workshop-build-deploy.md).

Finance, marketing, regional managers, and executives should be able to see overall sales, monthly trends, and category/region performance without training. The dashboard reports the supplied CSV snapshot; it does not provide live data or automated refresh.

## Approved decisions

- Aggregate the trend by calendar month.
- Show a clear error and stop when the CSV is missing or invalid. Never silently discard invalid rows or display partial totals.
- Use two application modules: `app.py` for presentation and `sales_data.py` for data loading, validation, and calculations.
- Use the layout and testing approach below.

## Architecture and project constraints

Use Python 3.11+, Streamlit, Pandas, and Plotly, with pytest for calculation and validation tests. Use a plain virtual environment in `venv/` and record dependencies in `requirements.txt`; do not use uv or conda.

Work in the existing checkout on `feature/sales-dashboard`; do not create a worktree. Keep functions small and readable, with comments explaining decisions where needed.

| File | Responsibility |
| --- | --- |
| `app.py` | Configure the page, load data through the data module, show errors, format metrics, and render Plotly charts with Streamlit. |
| `sales_data.py` | Load and validate CSV data; calculate KPI, monthly, category, and region totals without depending on Streamlit. |
| `tests/test_sales_data.py` | Check data calculations and failure cases using small, understandable fixtures and the supplied CSV. |
| `data/sales-data.csv` | Existing source data; preserve it. |
| `requirements.txt` | Dependencies needed to run and test the project. |
| `.gitignore` | Exclude the virtual environment and generated Python/test files. |
| `README.md` | Preserve tutorial content and add concise setup, run, test, and deployment instructions. |

Data flow: CSV → load and validate → calculate summaries → format metrics and render charts.

The data module accepts a CSV path and returns validated data. Calculation functions accept that data and return totals or chart-ready tables. The app resolves the CSV path relative to its own location so launching from another directory does not break loading.

## Layout and presentation

- Title: **ShopSmart Sales Dashboard**, following the company name in the PRD text rather than the inconsistent SHOPMART label in its wireframe.
- Show the source data's earliest and latest transaction dates beneath the title.
- Top row: prominent Total Sales and Total Orders metrics.
- Middle: a full-width monthly sales line chart, ordered chronologically, with clearly labeled month and sales axes.
- Bottom row: horizontal category and region bar charts side by side, with the largest sales values at the top.
- Use standard Streamlit components, consistent colors, readable text, and clear labels suitable for executive presentations.
- Format Total Sales with a dollar sign, thousands separators, and two decimal places; format orders as a whole number with separators. Chart tooltips show exact sales values to two decimal places.
- Include every category and region present in valid input; do not hard-code the sample labels into calculations.

## Data contract and calculations

Required columns are `date`, `order_id`, `product`, `category`, `region`, `quantity`, `unit_price`, and `total_amount`. Extra columns may be ignored.

Validation must reject unreadable or malformed CSV files, missing required columns, no transaction rows, blank required cells, invalid dates, and invalid or non-finite numeric values. Dates follow the source's `YYYY-MM-DD` format. Quantity must be an integer; prices and amounts must be numeric. Text identifiers remain strings. Validation reports the field and row where practical.

`total_amount` is the source of truth for sales; do not substitute `quantity × unit_price`. Total Orders means transaction count, as specified by the PRD, rather than distinct order IDs. Do not add deduplication or silently change the source data.

| Output | Calculation and ordering |
| --- | --- |
| Total Sales | Sum `total_amount` across all transactions. |
| Total Orders | Count transaction rows. |
| Monthly trend | Sum `total_amount` by year and month, sorted chronologically. Include intervening months with no transactions as zero; do not combine the same month across different years. |
| Category sales | Sum `total_amount` by category, descending by sales; alphabetical label order breaks ties. |
| Region sales | Sum `total_amount` by region, descending by sales; alphabetical label order breaks ties. |

Preserve numeric precision during calculations and format currency only for display. Numeric tests should allow ordinary floating-point representation tolerance, while verifying cent-level results.

## Error behavior

The data module raises understandable errors for expected loading and validation failures. The app displays a concise message identifying the problem and how to correct it, then stops before rendering KPIs or charts. Missing files, empty files, malformed rows, missing columns, and bad values must not result in a misleading zero-sales dashboard.

Unexpected programming errors should remain visible during development rather than being disguised as data problems.

## Verification and acceptance

Use pytest with small fixtures whose expected results can be checked by hand. Follow test-first development for data logic during implementation.

Tests cover valid loading, required-column checks, missing/empty/malformed files, blank values, invalid dates and numeric values, transaction counts, sales sums, monthly ordering across years, missing months, and descending category/region totals. Check that grouped totals reconcile with Total Sales.

The existing CSV was inspected during design without modifying it:

| Check | Observed value |
| --- | --- |
| Transactions | 482 |
| Total Sales | $116,500.21 |
| Date range | January 3–December 31, 2024 |
| Top category | Electronics ($42,683.67) |
| Categories | Electronics, Accessories, Audio, Wearables, Smart Home |
| Regions | North, South, East, West |

Manual verification must confirm the seven PRD acceptance criteria: prominent KPIs, correct trend, sorted category chart, sorted region chart, values matching the CSV, no errors or warnings on valid input, and professional appearance. Also verify tooltips, a clear error screen with bad input, and Chrome/Firefox/Safari/Edge compatibility without end-user plugins.

Measure dashboard load against the PRD's 5-second target and chart rendering against its 2-second target after data load. Record conditions and distinguish local timings from hosted startup/network delays. Record any checks that cannot be performed rather than claiming they passed.

## Milestones and completion standard

The existing task board uses M1–M7. Keep these IDs in the implementation plan and commit messages; plan step numbers will be separate. They serve the same traceability purpose as the tutorial's example TASK-1 labels.

| Board milestone | Design coverage |
| --- | --- |
| M1 | Virtual environment, dependencies, readable project structure, and run instructions. |
| M2 | CSV loading, validation, calculation module, and basic app layout. |
| M3 | Formatted KPI cards. |
| M4 | Monthly sales chart. |
| M5 | Sorted category and region charts. |
| M6 | Tests, manual acceptance checks, performance, compatibility, and refinement. |
| M7 | User-executed deployment and public URL verification. |

Follow the tutorial's shared Definition of Done during implementation: milestone acceptance criteria met, the app runs locally with `streamlit run app.py`, and changes are committed with the milestone ID in the message. Record completion commits on the board. No implementation milestone is complete merely because this design exists.

## Deployment and handoff

The implementation plan must end with deployment marked as **user-executed**. After implementation, review, and merge to `main`, the user deploys `app.py` from `main` to Streamlit Community Cloud, verifies the public dashboard, and records its shareable URL. The agent prepares instructions and hands off before this publishing step.

## Out of scope

Authentication/access control, database integration, exports, alerts, filters and date selection, transaction drill-down, dedicated mobile-responsive design, and automated refresh are Phase 2 work. No browser visual companion is needed for this tutorial.

## Review sequence

Review this written specification before creating the implementation plan. After approval, write the plan to `docs/superpowers/plans/2026-09-15-sales-dashboard.md`, mapping every step to a board milestone and marking data-logic tasks for test-first development. Keep execution inline for learning and wait for an explicit implementation go-ahead after plan review.
