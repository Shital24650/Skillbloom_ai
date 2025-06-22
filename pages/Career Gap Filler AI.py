import streamlit as st
from adk.type_defs import Message
from agents.gap_filler_agent.base import GapFillerAI  # ✅ Use dedicated agent
import PyPDF2

st.set_page_config(page_title="📉 Career Gap Filler AI", page_icon="🧩", layout="centered")

# Initialize agent
if "gap_agent" not in st.session_state:
    st.session_state.gap_agent = GapFillerAI()

st.title("🧩 Career Gap Filler AI")
st.caption("Upload your resume and enter your dream job. We'll find the skill gaps and build a learning path.")

# === Input Form ===
st.markdown("#### 📝 Upload Resume & Dream Role")
with st.form("gap_form"):
    uploaded_resume = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])
    target_job = st.text_input("Your Target Role", placeholder="e.g., Frontend Developer at Meta")
    submit = st.form_submit_button("🧠 Analyze Gaps")

# === PDF Text Extractor ===
def extract_text_from_pdf(upload):
    reader = PyPDF2.PdfReader(upload)
    all_text = ""
    for page in reader.pages:
        all_text += page.extract_text() or ""
    return all_text.strip()

# === Main Gap Analysis ===
if submit:
    if uploaded_resume and target_job:
        with st.spinner("🔎 Reading your resume and analyzing career gaps..."):
            resume_text = extract_text_from_pdf(uploaded_resume)
            prompt = (
                f"I want to become a {target_job}. Here is my current resume:\n"
                f"{resume_text}\n"
                f"Please analyze the skill and experience gaps I need to fill to become qualified for this role. "
                f"Also suggest a 4-week free learning plan using online resources."
            )
            msg = Message(payload={"text": prompt}, sender="user", receiver="GapFillerAI")
            response = st.session_state.gap_agent.execute(msg)
            output = response.payload["text"]

        st.success("🎯 Gap Analysis Ready!")
        st.markdown("### 📊 Your Skill Gaps & Learning Plan")
        st.markdown(output)
        st.toast("🔥 Use this as your roadmap to upskill!")
    else:
        st.error("❌ Please upload a resume and enter your target role.")
