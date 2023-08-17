import streamlit as st
from app.summarize import generate_summary

filing_type = st.selectbox(
    "Filing type 10-K or 10-Q",
    ("10-K","10-Q")
)


ticker = st.text_input(label="Ticker Symbol")

year = st.text_input(label="Year (2000-Present)")

if ticker!="" and year!="":
    final_summary = generate_summary(ticker, year, filing_type)
    # with open('summaries/AAPL_2021_10-K.txt', 'r') as f:
    #     final_summary = f.read()

    st.text_area(label="Summary",value=final_summary,height=500)