import streamlit as st
from pathlib import Path
from api_client import get_sales


@st.cache_data
def get_data():
    return get_sales()

df = get_data()



def layout_home_page():
    st.title("Welcome to Toy Storey overview")
    st.info(body="""
    **What can you find here?**

    This dashboard shows you statistics in sales och inventory and can help 
    decision making when ordering new products.
    """)

    unique_methods = df["payment_method"].dropna().unique().tolist()
    nr_of_methods = len(unique_methods)
    checkbox_col = st.columns(nr_of_methods)
    selected_methods = []

    for method in unique_methods:
        with checkbox_col[unique_methods.index(method)]:
            is_checked = st.checkbox(label=method, value=True)
            if is_checked:
                selected_methods.append(method)

    if selected_methods:
        filtered_df = df[df["payment_method"].isin(selected_methods)]
    else:
        filtered_df = df.iloc[0:0]
        st.warning("No payment method selected. Please select at least one payment method to view the data.")

    metric_cols = st.columns([0.30, 0.20, 0.30, 0.20])

    with metric_cols[0]:
        with st.container(border=True):
            st.metric(label="Sum of Sales", value=filtered_df["total_amount"].sum(), format="%.0f kr")

    with metric_cols[1]:
        with st.container(border=True):
            st.metric(label="Nr of Sales", value=filtered_df["total_amount"].count(), format="%.0f")

    with metric_cols[2]:
        with st.container(border=True):
            st.metric(label="Average Sale", value=filtered_df["total_amount"].mean(), format="%.0f kr")

    with metric_cols[3]:
        with st.container(border=True):
            st.metric(label="Nr of Customers", value=filtered_df["customer_id"].nunique())

    with st.container(border=True):
        st.subheader("Sales top 10 by customer")
        st.bar_chart(
            filtered_df.groupby("customer_id", as_index=False).agg({"total_amount": "sum"}).sort_values(by="total_amount", ascending=False).head(10),
            x="customer_id",
            x_label="Customer ID",
            y="total_amount",
            y_label="Total Amount",
            use_container_width=True,
            sort=False)

    with st.container(border=True):
        st.subheader("Payment method distribution")
        st.bar_chart(
            filtered_df.groupby("payment_method", as_index=False).agg({"total_amount": "count"}).sort_values(by="total_amount", ascending=False),
            x="payment_method",
            x_label="Payment Method",
            y="total_amount",
        y_label="Total Amount",
        use_container_width=True,
        sort=False
    )

    st.dataframe(filtered_df)

if __name__ == "__main__":
    layout_home_page()