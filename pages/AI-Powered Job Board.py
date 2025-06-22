import streamlit as st
import PyPDF2
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.job_match_agent.base import JobMatchAI  # ✅ use dedicated agent
from adk.type_defs import Message

st.set_page_config(page_title="AI Job Board", page_icon="💼")

if "job_agent" not in st.session_state:
    st.session_state.job_agent = JobMatchAI()

st.title("💼 AI-Powered Job Board")
st.caption("Upload your resume and get AI-recommended job listings based on your profile.")

# ---------------------
# Resume Upload
# ---------------------
st.header("📄 Upload Your Resume")

uploaded_file = st.file_uploader("Choose your resume file (PDF or TXT)", type=["pdf", "txt"])

resume_text = ""
if uploaded_file:
    if uploaded_file.type == "application/pdf":
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            resume_text += page.extract_text()
    else:
        resume_text = uploaded_file.read().decode("utf-8")

# ---------------------
# User Preferences
# ---------------------
st.header("🎯 Job Preferences")

location = st.text_input("Preferred Location", value="Remote")
salary_expectation = st.slider("Minimum Salary Expectation (USD/year)", 20000, 200000, 50000, step=10000)
job_type = st.selectbox("Job Type", ["Full-time", "Part-time", "Internship", "Contract", "Remote only"])

# ---------------------
# Get AI-Powered Jobs
# ---------------------
if st.button("🔍 Find Matching Jobs"):
    if not resume_text:
        st.warning("⚠️ Please upload your resume first.")
    else:
        with st.spinner("Finding jobs tailored to your profile..."):
            prompt = f"""
Based on this resume and job preferences, recommend 5 realistic and relevant job roles.

Resume:
{resume_text}

Preferences:
- Location: {location}
- Minimum Salary: ${salary_expectation}
- Job Type: {job_type}

For each job, include:
- Job Title
- Company Name (realistic or fictional)
- Location
- Estimated Salary Range
- Key Required Skills
- Short Job Description
- Why this job matches the candidate’s resume

Format the output in clean, readable markdown.
"""
            message = Message(payload={"text": prompt}, sender="user", receiver="JobMatchAI")
            response = st.session_state.job_agent.execute(message)

            st.markdown("## 🧠 Job Recommendations")
            st.markdown(response.payload["text"])
