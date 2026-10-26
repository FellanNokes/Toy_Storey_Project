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

    