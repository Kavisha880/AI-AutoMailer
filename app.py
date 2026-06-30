import streamlit as st
import re

from utils.excel_reader import read_excel
from utils.jd_parser import (
    extract_email,
    extract_company,
    extract_role
)
from utils.mail_generator import generate_mail
from utils.mail_sender import send_email

# ======================================
# SESSION STATE
# ======================================

if "generated_mail" not in st.session_state:
    st.session_state.generated_mail = ""

if "email" not in st.session_state:
    st.session_state.email = ""

if "subject" not in st.session_state:
    st.session_state.subject = ""

# ======================================
# PAGE CONFIG
# ======================================

st.set_page_config(
    page_title="AI AutoMailer",
    page_icon="📧",
    layout="wide"
)

st.title("📧 AI AutoMailer")

# ======================================
# INPUTS
# ======================================

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

# ======================================
# JD INPUT
# ======================================

if contact_source == "JD Paste":

    jd_text = st.text_area(
        "Paste Job Description",
        height=250
    )

# ======================================
# CONTACT LIST
# ======================================

elif contact_source == "Contact List Paste":

    contacts = st.text_area(
        "Paste Emails",
        height=250,
        placeholder="""
hr@company.com
jobs@company.com
careers@company.com
"""
    )

# ======================================
# EXCEL
# ======================================

elif contact_source == "Excel Upload":

    uploaded_file = st.file_uploader(
        "Upload Excel",
        type=["xlsx", "xls"]
    )

# ======================================
# CONTINUE BUTTON
# ======================================

if st.button("Continue"):

    # ---------------- JD ----------------

    if contact_source == "JD Paste":

        company = extract_company(jd_text)
        email = extract_email(jd_text)
        jd_role = extract_role(jd_text)

        st.subheader("📋 Detected Information")

        st.write("🏢 Company:", company)
        st.write("💼 Role:", jd_role)
        st.write("📧 Email:", email)

        try:

            generated_mail = generate_mail(
                role=role,
                company=company or "",
                jd=jd_text
            )

            st.session_state.generated_mail = generated_mail
            st.session_state.email = email

        except Exception as e:

            st.error(
                f"Mail generation failed: {str(e)}"
            )

    # ---------------- CONTACT LIST ----------------

    elif contact_source == "Contact List Paste":

        emails = re.findall(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            contacts
        )

        if emails:

            st.success(
                f"{len(emails)} emails found."
            )

            for email in emails:
                st.write(email)

        else:

            st.warning(
                "No valid email found."
            )

    # ---------------- EXCEL ----------------

    elif contact_source == "Excel Upload":

        if uploaded_file:

            df = read_excel(uploaded_file)

            st.success(
                f"{len(df)} records found."
            )

            st.dataframe(df.head())

        else:

            st.warning(
                "Please upload an Excel file."
            )
# ======================================
# GENERATED MAIL
# ======================================

if st.session_state.generated_mail:

    st.subheader("✉️ Generated Mail")

    st.text_area(
        "Mail Draft",
        st.session_state.generated_mail,
        height=450
    )

    if st.button("📨 Send Mail"):

        try:

            mail_text = st.session_state.generated_mail

            lines = mail_text.split("\n")

            # -----------------------------
            # Extract Subject
            # -----------------------------

            subject_line = "AI/ML Opportunity"

            for i, line in enumerate(lines):

                if line.lower().startswith("subject:"):

                    subject_line = (
                        line.replace("Subject:", "")
                        .strip()
                    )

                    body_text = "\n".join(
                        lines[i + 2:]
                    )

                    break

            else:

                body_text = mail_text

            send_email(
                recipient_email=st.session_state.email,
                subject=subject_line,
                body=body_text
            )

            st.success(
                f"✅ Mail sent successfully to {st.session_state.email}"
            )

        except Exception as e:

            st.error(
                f"❌ Mail sending failed:\n\n{e}"
            )