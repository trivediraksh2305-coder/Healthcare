import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader
from docx import Document

# Page Title
st.title("AI Medical Report Simplifier")

# Configure Gemini API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Use free Gemini model
model = genai.GenerativeModel("gemini-pro")

st.write("Upload your medical report and AI will explain it in simple terms.")

# File uploader
uploaded_file = st.file_uploader(
    "Upload Report",
    type=["pdf", "docx"]
)

# Function to read PDF
def read_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

# Function to read DOCX
def read_docx(file):
    doc = Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text
    return text


if uploaded_file:

    file_type = uploaded_file.name.split(".")[-1]

    if file_type == "pdf":
        report_text = read_pdf(uploaded_file)

    elif file_type == "docx":
        report_text = read_docx(uploaded_file)

    else:
        report_text = ""

    st.subheader("Extracted Text")
    st.write(report_text)

    if st.button("Analyze Report"):

        prompt = f"""
        Explain this medical report in very simple language.

        Also tell:
        - what the report means
        - possible diseases
        - simple health advice

        Medical Report:
        {report_text}
        """

        try:
            response = model.generate_content(prompt)

            st.subheader("AI Explanation")
            st.write(response.text)

        except Exception as e:
            st.error("Error connecting to AI. Please check API key.")
            st.write(e)
