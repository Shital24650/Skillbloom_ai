import streamlit as st
import PyPDF2
import os
import sys

# Add path to import JobMatchAI
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.job_match_agent.base import JobMatchAI
from adk.type_defs import Message

st.set_page_config(page_title="💼 AI Job Board", page_icon="💼")

# Initialize agent
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
            resume_text += page.extract_text() or ""
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
    if not resume_text.strip():
        st.warning("⚠️ Please upload your resume first.")
    else:
        with st.spinner("Finding jobs tailored to your profile..."):
            prompt = f"""
You are an AI resume reader and job recommender for SkillBloom.

The user has uploaded the following resume:

--- RESUME START ---
{resume_text.strip()}
--- RESUME END ---

They prefer:
- Location: {location}
- Salary: ${salary_expectation}/year minimum
- Job Type: {job_type}

Provide:
1. 5 job titles relevant to the resume.
2. For each job, give a 1-line reason why it's a good fit.
3. Include the average salary range (USD/year).
4. If the user has only internships or is early-career, mention that the salary may vary and realistic expectations are important.

Be realistic, helpful, and motivational.
"""

            message = Message(payload={"text": prompt}, sender="user", receiver="JobMatchAI")
            response = st.session_state.job_agent.execute(message)

            st.markdown("## 🧠 Job Recommendations")
            st.markdown(response.payload["text"])
