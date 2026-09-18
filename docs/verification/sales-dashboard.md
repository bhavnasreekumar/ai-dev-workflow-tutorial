# Sales dashboard verification

Task 6 / M6. Checks performed September 16–17, 2026, America/Los_Angeles.
Application under review: `bd81731`; Task 6 adds a regression test and documentation.
M6 is **Done**. The tutorial's manual browser check was completed in
Google Chrome; separate Firefox, Safari, and Edge checks are not required for
this review. Task 7's handoff documentation is prepared.

## User review

On September 17, 2026, the user confirmed that Total Sales, Total Orders,
the monthly trend, sales by category, and sales by region rendered correctly
in Google Chrome and explicitly approved the dashboard. This is a user-reported
visual acceptance result; the user did not report a browser version, measured
load times, or results in other browsers. The browser check is complete for the
tutorial's manual Chrome workflow.

## Environment and automated checks

macOS 13.4 (22F66), Python 3.14.7, Streamlit 1.64.0, Pandas 3.0.5,
Plotly 6.9.0, pytest 9.1.1. Plain `venv/`; dependencies pinned in `requirements.txt`.

- `venv/bin/python -m pytest -q -W error`: **23 passed**, latest run 0.85 seconds
  on September 17. This includes the new supplied-CSV regression test; it tests
  existing behavior, so no production-code change or artificial failing cycle was needed.
- `venv/bin/python -m pip --no-cache-dir check`: **No broken requirements found**.
- The regression checks 482 transactions, $116,500.21, January 3–December 31,
  2024, all category/region totals and ordering, 12 months, and reconciliation
  of all three chart totals with Total Sales.
- Task 4 and Task 5 browser checks independently summed the CSV with the
  standard-library CSV reader and Decimal, then checked every plotted month
  and all nine breakdown hover amounts. Those checks passed; app/data code
  has not changed since them.

## PRD acceptance evidence

| Criterion | Result in Chrome | Evidence |
| --- | --- | --- |
| KPIs visible | Pass | Prominent $116,500.21 and 482 cards above the trend. |
| Trend chart works | Pass | Twelve chronological Jan–Dec 2024 points; Month and Sales ($) axes; dollar/cents hover amounts verified in Task 4. |
| Category chart works | Pass | Electronics, Wearables, Audio, Smart Home, Accessories in descending visual order; exact hover amounts verified in Task 5. |
| Region chart works | Pass | North, West, East, South in descending visual order; exact hover amounts verified in Task 5. |
| Data loads correctly | Pass | Regression test and independent CSV sums agree; chart totals reconcile. |
| No errors | Pass for valid input in Chrome | No Streamlit error/warning elements, browser runtime exceptions, or browser log warning/error entries in the recording. |
| Professional appearance | Pass at tested desktop size | Inspected full 1440 × 1500 screenshot: clear title/date caption, readable labels, consistent blue charts, wide trend and side-by-side bars; no clipping observed. |

No filters or other Phase 2 product features were added. The Streamlit Deploy
button is framework chrome. Desktop appearance is verified only at the tested
viewport, not across every browser or screen size.

## Error handling

Ran the plan's temporary check using the
[Streamlit AppTest API](https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest).
It patches `sales_data.load_sales_data` to raise each of:

- `Cannot read sales CSV.`
- `Invalid total_amount in record 2.`

Both produced exactly one matching error, no uncaught exception, no metric,
and no Plotly chart. The real CSV was not modified. Loader tests separately
exercise actual invalid temporary files; the AppTest checks the app's response
to the loader's error contract.

The standalone AppTest harness logged `missing ScriptRunContext`, with its
bare-mode explanation. This was not an app-screen warning. Streamlit also
printed its optional Watchdog performance suggestion on server startup.
Sandbox approval was needed for local server/browser connections.

## Browser verification

| Browser/version | Date | Outcome |
| --- | --- | --- |
| Chrome 153.0.8010.47, headless | Sept 16–17 | Functional checks passed using an isolated temporary profile, with no extensions; layout and hover evidence above. |
| Google Chrome, user session (version not reported) | Sept 17 | User confirmed all dashboard sections rendered correctly and approved the dashboard. |
| Firefox, version unavailable | Sept 16 | Not required for this review. |
| Safari 16.5 | Sept 16 | Not required for this review. |
| Edge, version unavailable | Sept 16 | Not required for this review. |

Separate Firefox, Safari, and Edge checks are out of scope for this review; the
manual Chrome result is the browser acceptance evidence used here.

## Code review and remaining work

Reviewed `app.py` and `sales_data.py`: presentation and calculations are separate,
functions are small, grouping is shared, text IDs are preserved, errors stop
before results, and the CSV path is relative to the app. Names and the existing
error-class docstring explain the current code; no additional comments or
production changes were needed. `git diff -- data/sales-data.csv` is empty.

The M6 acceptance checks are complete under the tutorial scope. M7 handoff
documentation is prepared, and the user's Chrome approval is recorded;
deployment has not occurred.
