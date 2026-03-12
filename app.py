import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# Configure Gemini API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Use supported model
model = genai.GenerativeModel("gemini-1.5-flash")

st.title("AI Medical Report Simplifier")

uploaded_file = st.file_uploader("Upload PDF Report", type=["pdf"])

def extract_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

if uploaded_file:
    report_text = extract_pdf(uploaded_file)

    st.subheader("Extracted Text")
    st.write(report_text[:2000])  # preview only

    if st.button("Analyze Report"):
        prompt = f"""
        Explain this medical report in simple language.

        Also include:
        - meaning of values
        - possible diseases
        - simple health advice

        Report:
        {report_text}
        """

        try:
            response = model.generate_content(prompt)
            st.subheader("AI Explanation")
            st.write(response.text)
        except Exception as e:
            st.error(e)
