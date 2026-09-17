# Sales dashboard verification

Task 6 / M6. Checks performed September 16–17, 2026, America/Los_Angeles.
Application under review: `bd81731`; Task 6 adds a regression test and documentation.
M6 remains **In progress**. Firefox, Safari, Edge, and complete painted-frame
performance verification remain outstanding. Task 7 has not started.

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

## Browser compatibility

| Browser/version | Date | Outcome |
| --- | --- | --- |
| Chrome 153.0.8010.47, headless | Sept 16–17 | Functional checks passed using an isolated temporary profile, with no extensions; layout and hover evidence above. |
| Firefox, version unavailable | Sept 16 | Not installed in `/Applications`; outstanding. |
| Safari 16.5 | Sept 16 | Driver refused to create a session because Develop → Allow Remote Automation is disabled; outstanding. Browser settings were not changed. |
| Edge, version unavailable | Sept 16 | Not installed in `/Applications`; outstanding. |

Complete the same KPI, chart-order, hover, date-label, and error checks in
Firefox, Safari, and Edge and record their versions and results before closing M6.

## Local performance

The final recording used Chrome's DevTools timeline and screenshot trace,
started before navigation to `http://127.0.0.1:8501/`. Viewport: 1440 × 1500,
device scale 1, no CPU/network throttling. The server was already running.
Load 1 used a fresh temporary browser profile (first browser load, not a cold
Python/server start); loads 2 and 3 reused that profile.

The recorder identified document navigation start and decoded binary WebSocket
ForwardMsg messages containing new dashboard elements. Each load received ten
element messages. It marked readiness after two animation frames once both
metrics and the 12-point, 5-bar, and 4-bar charts existed in the DOM.

| Load | Navigation to readiness | First element to readiness | Last element to readiness |
| --- | ---: | ---: | ---: |
| 1, fresh profile | 2.4267 s | 1.4267 s | 0.7101 s |
| 2, warm | 0.3762 s | 0.3123 s | 0.0410 s |
| 3, warm | 0.3659 s | 0.3048 s | 0.0466 s |

The first load's inspected trace frame shows the complete dashboard 0.011481 s
after the readiness mark: **2.4382 s** from navigation and **1.4382 s** from the
first element delivery, within the 5-second and 2-second targets for that load.
Warm-load trace images did not provide reliable visual confirmation when
inspected. Their readiness intervals are **provisional**, not verified paint
times. Leave the overall performance criterion unchecked until three loads
have reliable painted-frame evidence.

Element delivery follows server-side data work; it is not the precise Python
CSV-load timestamp. These are local observations, not hosted startup/network
measurements, and server startup time was not substituted for browser rendering.

An earlier recorder download exceeded its WebSocket message-size limit;
smaller trace chunks resolved that tool issue. Earlier recordings without
per-load screenshots were superseded by the measurements above.
Temporary raw evidence is in `/private/tmp/shopsmart-m6/` (three compressed
trace JSON files, per-load PNGs, and `results.json`); recorder script:
`/private/tmp/shopsmart-m6-check.py`. These temporary files are not committed
and may be cleaned by the operating system. The method and observations are
preserved here; repeat using a browser Performance recording for the remaining
painted-frame checks.

## Code review and remaining work

Reviewed `app.py` and `sales_data.py`: presentation and calculations are separate,
functions are small, grouping is shared, text IDs are preserved, errors stop
before results, and the CSV path is relative to the app. Names and the existing
error-class docstring explain the current code; no additional comments or
production changes were needed. `git diff -- data/sales-data.csv` is empty.

Outstanding: Firefox/Safari/Edge compatibility and three fully confirmed
painted-frame performance recordings. M6 stays open; M7/deployment are untouched.
