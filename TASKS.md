# E-Commerce Analytics Task Board

Source: [Product requirements](prd/ecommerce-analytics.md). Scope: Phase 1 sales dashboard.

All tasks start as **To do**. Mark a task `[x]` when its checks pass; add **In progress** beside the task you are working on.

## M1 — Environment setup and project initialization

- [ ] Set up Python 3.11+ with Streamlit, Pandas, and Plotly; record dependencies and local run instructions.
- [ ] Initialize a simple, readable project structure with a Streamlit entry point.

## M2 — Data loading and basic structure

- [ ] Load `data/sales-data.csv`; validate the required columns and parse dates, numeric values, and categorical values correctly.
- [ ] Prepare sales totals, transaction counts, and time/category/region aggregations from the CSV.
- [ ] Create the dashboard layout: prominent KPI cards, a sales trend chart, and category/region charts side by side.

## M3 — KPI cards implementation

- [ ] Display Total Sales (sum of `total_amount`) and Total Orders (transaction count) prominently, with currency formatting and thousands separators. **Acceptance: KPIs visible.**

## M4 — Sales trend chart

- [ ] Show correctly aggregated daily or monthly sales in a line chart, with time and sales axes, clear labels, and tooltips showing exact values. **Acceptance: Trend chart works.**

## M5 — Category and region breakdowns

- [ ] Show every category in a sales bar chart, sorted highest to lowest, with clear labels and exact-value tooltips. **Acceptance: Category chart works.**
- [ ] Show every region in a sales bar chart, sorted highest to lowest, with clear labels and exact-value tooltips. **Acceptance: Region chart works.**

## M6 — Testing and refinement

- [ ] Verify every KPI and chart aggregation against calculations from the CSV. Sample expectations: 482 orders, approximately $116,500 in sales, Electronics as top category, five categories, and North/South/East/West regions. Use CSV calculations for exact values. **Acceptance: Data loads correctly.**
- [ ] Run the dashboard and resolve errors and warnings. **Acceptance: No errors.**
- [ ] Review labels, formatting, and layout for clear, training-free usage and executive presentation. **Acceptance: Professional appearance.**
- [ ] Verify dashboard load within 5 seconds and chart rendering within 2 seconds of data load.
- [ ] Check Chrome, Firefox, Safari, and Edge compatibility without end-user plugins or installations.
- [ ] Review code for readable, modular Python and helpful comments.

## M7 — Deployment to Streamlit Community Cloud

- [ ] Deploy the dashboard to Streamlit Community Cloud with the required dependencies and CSV available.
- [ ] Verify the public dashboard loads and its KPIs and charts work; record the shareable URL for stakeholder review.

## Out of scope

Phase 2 work: authentication/access control, database integration, exports, email alerts, filtering/date selection, transaction drill-down, mobile-responsive design, and automated refresh.
