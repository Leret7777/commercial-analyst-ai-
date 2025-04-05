# 📦 AI-Powered Commercial Analyst App (Beginner Friendly)
# # Features: Upload a PDF/Excel, get a summary, and receive strategy suggestions using Mistral (via Ollama)

import streamlit as st
import pandas as pd
import pdfplumber
import subprocess
import json

# ------------------ HELPER FUNCTIONS ------------------
def extract_text_from_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

def extract_text_from_excel(uploaded_file):
    df = pd.read_excel(uploaded_file)
    return df.to_string(index=False)

def get_summary_and_recommendations(text):
    prompt = f"""
    You are a commercial analyst assistant. Based on the following report, summarize the key insights and suggest:
    1. Sales strategies
    2. Product portfolio recommendations
    3. Resource allocation insights

    Report:
    {text}
    """

    try:
        result = subprocess.run(
            ["ollama", "run", "mistral", prompt],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error calling Mistral via Ollama: {e.stderr}"

# ------------------ STREAMLIT APP ------------------
st.title("📊 Commercial Analyst AI Assistant")
st.write("Upload your commercial report (PDF or Excel) to get a smart summary and strategic recommendations.")

uploaded_file = st.file_uploader("Upload Report", type=["pdf", "xlsx"])

if uploaded_file:
    file_type = uploaded_file.name.split('.')[-1].lower()

    with st.spinner("Reading your file..."):
        try:
            if file_type == "pdf":
                raw_text = extract_text_from_pdf(uploaded_file)
            elif file_type == "xlsx":
                raw_text = extract_text_from_excel(uploaded_file)
            else:
                st.error("Unsupported file format.")
                st.stop()
        except Exception as e:
            st.error(f"Failed to read file: {e}")
            st.stop()

    if raw_text:
        with st.spinner("Generating summary and recommendations..."):
            try:
                output = get_summary_and_recommendations(raw_text)
                st.success("Here are your results:")
                st.markdown(output)
            except Exception as e:
                st.error(f"Error generating output: {e}")
    else:
        st.warning("No text was extracted from the file.")

# ------------------ INSTRUCTIONS TO SET UP ------------------
# 1. Install Ollama and pull the Mistral model: https://ollama.com/
#    > ollama pull mistral
# 2. Make sure Ollama is running locally before you start the app
# 3. Run the app with: streamlit run app.py
# 4. Install required packages:
#    pip install streamlit pandas pdfplumber openpyxl
