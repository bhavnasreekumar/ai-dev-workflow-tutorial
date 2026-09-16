from pathlib import Path

import streamlit as st

from sales_data import SalesDataError, load_sales_data

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
