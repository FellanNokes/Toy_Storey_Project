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

    metric_cols = st.columns(4)

    with metric_cols[0]:
        st.metric(label="Sum of Sales", value=df["total_amount"].sum(), format="%.0f kr")

    with metric_cols[1]:
        st.metric(label="Nr of Sales", value=df["total_amount"].count(), format="%.0f")

    with metric_cols[2]:
        st.metric(label="Average Sale", value=df["total_amount"].mean(), format="%.0f kr")

    with metric_cols[3]:
        st.metric(label="Nr of Customers", value=df["customer_id"].nunique())

    st.divider()

    st.subheader("Sales top 10 by customer")
    st.bar_chart(
        df.groupby("customer_id", as_index=False).agg({"total_amount": "sum"}).sort_values(by="total_amount", ascending=False).head(10),
        x="customer_id",
        x_label="Customer ID",
        y="total_amount",
        y_label="Total Amount",
        use_container_width=True,
        sort=False)
    
    st.dataframe(df)

if __name__ == "__main__":
    layout_home_page()