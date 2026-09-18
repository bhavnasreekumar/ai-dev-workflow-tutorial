# E-Commerce Analytics Task Board

Source: [Product requirements](prd/ecommerce-analytics.md). Scope: Phase 1 sales dashboard.

All tasks start as **To do**. Mark a task `[x]` when its checks pass; add **In progress** beside the task you are working on.

## Definition of Done

A milestone is complete when its acceptance criteria are met, the app runs locally with `streamlit run app.py`, and changes are committed with the milestone ID in the commit message.

## M1 — Environment setup and project initialization — Done

Commit: `6e79b35` — M1: set up runnable Streamlit project

Notes: Installation and dependency checks passed; the local Streamlit server
and headless Chrome health check confirmed the rendered dashboard title and
heading without app errors or warnings.

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

## M2 — Data loading and basic structure — Done

Commit: `bd81731` — M5 M2: complete breakdown charts and dashboard structure

Notes: The loader and dashboard structure passed 18 tests; Chrome confirmed the
date caption and no app errors or warnings, and the source CSV remained unchanged.

Earlier loading commit: `27cac03` — M2: load and validate sales CSV

- [x] Load `data/sales-data.csv`; validate the required columns and parse dates, numeric values, and categorical values correctly.
- [x] Prepare sales totals, transaction counts, and time/category/region aggregations from the CSV.
- [x] Create the dashboard layout: prominent KPI cards, a sales trend chart, and category/region charts side by side.

Task 2 verification (2026-09-16): the initial pytest run failed with
`ModuleNotFoundError: No module named 'sales_data'`, as expected before implementation.
After adding the loader and connecting the app, `venv/bin/python -m pytest -q`
passed all 18 tests. Headless Chrome confirmed the caption
"Sales recorded from January 03, 2024 to December 31, 2024" with no app error
or warning elements. The source CSV is unchanged. The local server and temporary
browser were stopped after verification. Starting the server required approval
to open a local port; Streamlit printed its optional Watchdog performance suggestion.

M2 is **Done**: Task 2 provides loading and validation.
Task 3 adds sales totals, transaction counts, and KPI cards.
Task 4 adds monthly aggregation and the sales trend.
Task 5 adds category/region aggregations and charts, completing the required structure.

## M3 — KPI cards implementation — Done

Commit: `121fa74` — M3: calculate and display sales KPIs

Notes: The KPI checks passed 19 tests; Chrome confirmed Total Sales of
`$116,500.21` and Total Orders of `482` in side-by-side cards.

- [x] Display Total Sales (sum of `total_amount`) and Total Orders (transaction count) prominently, with currency formatting and thousands separators. **Acceptance: KPIs visible.**

Task 3 verification (2026-09-16): the KPI test first failed because
`calculate_kpis` did not exist. After implementation, `venv/bin/python -m pytest -q`
passed all 19 tests. The new test confirms duplicate order IDs still count as
separate transactions and sales use recorded amounts rather than quantity × price.
Headless Chrome confirmed Total Sales `$116,500.21` and Total Orders `482`
in side-by-side cards with 36px values and no app error or warning elements.
The source CSV is unchanged. The local server and temporary browser were stopped.
The server required approval to open its local port and printed the optional
Watchdog performance suggestion. Stopped before Task 4 for user review.

## M4 — Sales trend chart — Done

Commit: `daa61fa` — M4: add monthly sales trend

Notes: The trend checks passed 20 tests; Chrome confirmed 12 chronological
monthly points, labeled axes, and hover values matching independent CSV sums.

- [x] Show correctly aggregated daily or monthly sales in a line chart, with time and sales axes, clear labels, and tooltips showing exact values. **Acceptance: Trend chart works.**

Task 4 verification (2026-09-16): the monthly test first failed because
`monthly_sales` did not exist. After implementation, `venv/bin/python -m pytest -q`
passed all 20 tests, including chronological grouping across years, zero-filled
intervening months, and preservation of total sales.
Headless Chrome confirmed 12 points from January through December 2024, labeled
Month and Sales ($) axes, and no app error or warning elements. All 12 plotted
values and mouse-hover dollar/cents labels matched independent CSV sums using
Python's standard-library CSV reader and Decimal arithmetic.
The source CSV is unchanged. The local server and temporary browser were stopped.
Starting the server required approval to open its local port; Streamlit printed
the optional Watchdog performance suggestion. Stopped before Task 5 for review.

## M5 — Category and region breakdowns — Done

Commit: `bd81731` — M5 M2: complete breakdown charts and dashboard structure

Notes: The breakdown checks passed 22 tests; Chrome confirmed five categories,
four regions, descending order, exact hover values, and totals reconciling to
`$116,500.21`.

- [x] Show every category in a sales bar chart, sorted highest to lowest, with clear labels and exact-value tooltips. **Acceptance: Category chart works.**
- [x] Show every region in a sales bar chart, sorted highest to lowest, with clear labels and exact-value tooltips. **Acceptance: Region chart works.**

Task 5 verification (2026-09-16): the breakdown test first failed because the
new functions did not exist. After implementation, `venv/bin/python -m pytest -q`
passed all 22 tests, covering all groups, descending totals, and alphabetical ties.
Headless Chrome confirmed five categories (Electronics first) and four regions
(North first), descending visual order, labeled axes, consistent blue bars, and
side-by-side charts beneath the trend. All nine mouse-hover dollar/cents amounts
matched independent CSV sums using the standard-library CSV reader and Decimal.
Both breakdown totals reconcile to `$116,500.21`. The existing KPI cards and
12-point monthly trend remain visible, with no app error or warning elements.
These checks, together with the loader and aggregation tests, satisfy M2's
loading, aggregation, and layout criteria. The source CSV is unchanged.
The local server and temporary browser were stopped after verification. Starting
the server required approval to open its local port; Streamlit printed its optional
Watchdog performance suggestion. Stopped before Task 6 for review.

## M6 — Testing and refinement — Done

Commit: `4d662f8` — M6: verify dashboard acceptance and document results

Notes: Chrome manual verification completed successfully. The tutorial does not
require separate Firefox, Safari, Edge, or multi-load performance checks.

- [x] Verify every KPI and chart aggregation against calculations from the CSV. Sample expectations: 482 orders, approximately $116,500 in sales, Electronics as top category, five categories, and North/South/East/West regions. Use CSV calculations for exact values. **Acceptance: Data loads correctly.**
- [x] Run the dashboard and resolve errors and warnings. **Acceptance: No errors.**
- [x] Review labels, formatting, and layout for clear, training-free usage and executive presentation. **Acceptance: Professional appearance.**
- [x] Verify the dashboard renders successfully in Google Chrome, the browser used for the manual tutorial check.
- [x] Review code for readable, modular Python and helpful comments.

Task 6 evidence: [verification record](docs/verification/sales-dashboard.md).
23 tests pass with warnings treated as errors; dependencies are compatible.
Both error paths stop before results. Chrome functional and desktop appearance
checks pass. The tutorial's manual browser check was completed successfully in
Google Chrome; separate Firefox, Safari, and Edge checks are not required for
this review.

User review on 2026-09-17: the dashboard rendered correctly in Google Chrome,
including Total Sales, Total Orders, monthly trend, category sales, and region
sales. The user explicitly approved the dashboard. This confirms the Chrome
visual review; all M6 acceptance checks are complete.

## M7 — Deployment to Streamlit Community Cloud — Done

Commit: `e4d4e8a` — M7: document user deployment handoff (preparation only)

Notes: The user-reported deployment verification confirmed the public dashboard
in Chrome with `$116,500.21`, `482` orders, five categories, and four regions.

- [x] Deploy the dashboard to Streamlit Community Cloud with the required dependencies and CSV available.
- [x] Verify the public dashboard loads and its KPIs and charts work; record the shareable URL for stakeholder review.

Task 7 handoff prepared on 2026-09-17:
[review and deployment instructions](README.md#review-and-deploy-the-sales-dashboard).
Reviewed `git diff main...HEAD` and M1–M6 evidence. The base branch is `main`.
No new code defect was identified; all 23 tests pass with warnings treated as
errors, `pip check` reports no conflicts, and the branch diff passes whitespace
checks. The CSV is unchanged. Tracked-file inspection confirmed no virtual
environment, test caches, `.env`, or Streamlit secrets file is committed;
their ignore rules are effective.

`sales_data.py` owns validation and calculations; `app.py` owns presentation
and error display. The user approved the rendered dashboard in Chrome on
2026-09-17. M6's acceptance evidence is complete under the tutorial scope.
The handoff documentation is ready for review; deployment readiness remains
conditional on the user's review/merge/push workflow. No merge, push, or
deployment was performed. After that workflow, verify the reviewed implementation
on remote `main` before Task 8. Stopped before user-executed deployment.

Read-only GitHub check on 2026-09-17: remote `main` is
`06d88f522926f227d1de1234ba938fe0d22e14d8`; the dashboard implementation is
not present there, and no remote `feature/sales-dashboard` branch was returned.
At that review checkpoint, merge/push authorization was still pending.

Merge/push update on 2026-09-17: the user explicitly authorized merging and
pushing while retaining the browser and performance limitations. After fetching
GitHub's latest state, `main` was fast-forwarded to `feature/sales-dashboard`
at `f5826f5d28c8675447826f6580cf3e2cd86a3ede`. All 23 tests passed on the merged
result with warnings treated as errors, and `pip check` found no conflicts.
The push succeeded; `git ls-remote origin refs/heads/main` confirmed that exact
commit on GitHub, satisfying the remote-implementation check before Task 8.
At that checkpoint, deployment had not been performed and required separate user
approval. The feature
branch is retained locally as a review reference.

Deployment verification (user-reported, 2026-09-17): after approving the
user-executed deployment step, the user successfully deployed the dashboard to
Streamlit Community Cloud and verified it in Google Chrome. Total Sales is
`$116,500.21`, Total Orders is `482`, the monthly sales trend displays correctly,
and all five categories and four regions display correctly. M7's deployment
criteria are complete. M6's Chrome acceptance evidence remains the verification
record for this review.

Public URL: https://bhavnasreekumar-ai-dev-workflow-tutorial-app-bixwct.streamlit.app/

Deployed Git commit: Not reported in the deployment confirmation.

Hosted Python runtime: Not reported in the deployment confirmation.

Hosted startup/performance observations: Deployment succeeded and the dashboard
rendered correctly in Chrome, as reported by the user. No measured timings were provided.

## Out of scope

Phase 2 work: authentication/access control, database integration, exports, email alerts, filtering/date selection, transaction drill-down, mobile-responsive design, and automated refresh.
