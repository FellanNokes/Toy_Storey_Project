import streamlit as st
from pathlib import Path
from connect_data import load_data


@st.cache_data
def get_data():
    return load_data()

df = get_data()

def layout_home_page():
    st.title("Welcome to Toy Storey overview")
    st.info(body="""
    **What can you find here?**

    This dashboard shows you statistics in sales och inventory and can help 
    decision making when ordering new products.
    """)

    st.divider()

    st.dataframe(df)

    df_customer_chart = df.groupby("customer_id", as_index=False).agg({"total_amount": "sum"}).sort_values(by="total_amount", ascending=False).head(10)
    st.subheader("Sales top 10 by customer")
    st.bar_chart(
        df_customer_chart,
        x="customer_id",
        x_label="Customer ID",
        y="total_amount",
        y_label="Total Amount",
        use_container_width=True,
        sort=False)

if __name__ == "__main__":
    layout_home_page()