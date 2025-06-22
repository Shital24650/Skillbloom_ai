import streamlit as st
from agents.ats_resume_agent.base import ATSResumeAI  # ✅ Use dedicated agent
from adk.type_defs import Message
from PyPDF2 import PdfReader

st.set_page_config(page_title="ATS Resume Analyzer", page_icon="📊")

# Initialize agent
if "ats_agent" not in st.session_state:
    st.session_state.ats_agent = ATSResumeAI()

st.title("📊 Resume Analyzer & ATS Score Checker")
st.caption("Upload your resume and get AI-powered feedback with ATS score and recommendations.")

uploaded_file = st.file_uploader("📄 Upload Your Resume (PDF only)", type=["pdf"])

if uploaded_file:
    # === Read PDF Content ===
    with st.spinner("🔍 Extracting your resume text..."):
        reader = PdfReader(uploaded_file)
        resume_text = "\n".join(page.extract_text() or "" for page in reader.pages)

    st.subheader("🧠 AI Feedback")
    st.info("We’re analyzing your resume based on ATS best practices and job relevance...")

    prompt = (
        f"Here is a resume:\n\n{resume_text}\n\n"
        f"Please rate this resume for ATS-friendliness on a scale of 0 to 100.\n"
        f"Also suggest improvements to boost the ATS score.\n"
        f"Be detailed and explain how to rewrite specific sections if needed."
    )

    msg = Message(payload={"text": prompt}, sender="user", receiver="ATSResumeAI")
    response = st.session_state.ats_agent.execute(msg)

    ats_feedback = response.payload["text"]
    st.success("✅ Analysis Complete")
    st.markdown("### 📈 ATS Score & Recommendations")
    st.markdown(ats_feedback)
    st.toast("📌 Use the feedback to enhance your resume!")

else:
    st.info("👆 Upload your resume to begin analysis.")
