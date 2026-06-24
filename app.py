import streamlit as st
import re
import pandas as pd
from utils.excel_reader import read_excel

st.set_page_config(
    page_title="AI AutoMailer",
    page_icon="📧",
    layout="wide"
)

st.title("📧 AI AutoMailer")

role = st.text_input(
    "Enter Role",
    placeholder="AI/ML Intern"
)

contact_source = st.radio(
    "Choose Contact Source",
    [
        "JD Paste",
        "Contact List Paste",
        "Excel Upload"
    ]
)

if contact_source == "JD Paste":
    jd_text = st.text_area(
        "Paste Job Description",
        height=250
    )

elif contact_source == "Contact List Paste":
    contacts = st.text_area(
        "Paste Emails",
        height=250,
        placeholder="""
hr@adobe.com
jobs@microsoft.com
hiring@wipro.com
"""
    )

elif contact_source == "Excel Upload":
    uploaded_file = st.file_uploader(
        "Upload Excel File",
        type=["xlsx", "xls"]
    )

if st.button("Continue"):

    if contact_source == "JD Paste":

        emails = re.findall(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            jd_text
        )

        st.subheader("Detected Emails")

        if emails:
            for email in emails:
                st.write(email)
        else:
            st.warning("No email found")

    elif contact_source == "Contact List Paste":

        emails = re.findall(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            contacts
        )

        st.subheader("Detected Emails")

        for email in emails:
            st.write(email)

    elif contact_source == "Excel Upload":

        if uploaded_file:

            df = read_excel(uploaded_file)

            st.success(
                f"{len(df)} records found"
            )

            st.dataframe(df.head())
    