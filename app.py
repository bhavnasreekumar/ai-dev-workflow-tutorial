from pathlib import Path

import plotly.express as px
import streamlit as st

from sales_data import (
    SalesDataError,
    calculate_kpis,
    load_sales_data,
    monthly_sales,
    sales_by_category,
    sales_by_region,
)

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
st.title("ShopSmart Sales Dashboard")

try:
    data = load_sales_data(Path(__file__).resolve().parent / "data" / "sales-data.csv")
except SalesDataError as error:
    st.error(str(error))
    st.stop()

start = data["date"].min().strftime("%B %d, %Y")
end = data["date"].max().strftime("%B %d, %Y")
st.caption(f"Sales recorded from {start} to {end}")

total_sales, total_orders = calculate_kpis(data)
sales_column, orders_column = st.columns(2)
sales_column.metric("Total Sales", f"${total_sales:,.2f}")
orders_column.metric("Total Orders", f"{total_orders:,}")

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
