import streamlit as st
from app.summarize import generate_summary

filing_type = st.selectbox(
    "Filing type 10-K or 10-Q",
    ("10-Q","10-K")
)


ticker = st.text_input(label="Ticker Symbol")

year = st.text_input(label="Year (2000-Present)")
quarters = ["","Q3","Q2","Q1"]
quarter = st.selectbox("Quarters",quarters)

if ticker!="" and year!="" and quarter!="":
    final_summary = generate_summary(ticker, year, filing_type,quarters=quarter)
    # with open('summaries/AAPL_2021_10-Q_Q3.txt', 'r') as f:
    #     final_summary = f.read()

    st.text_area(label="Summary",value=final_summary,height=500)