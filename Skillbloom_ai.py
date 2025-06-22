import streamlit as st
from agents.skillbloom_agent.base import SkillAgent
from adk.type_defs import Message
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="SkillBloom AI", page_icon="🌱", layout="centered")

# === Branding & Welcome Section ===
st.markdown("""
    <style>
    .centered-title {
        text-align: center;
        margin-top: -40px;
    }
    .welcome-box {
        background-color: #F0FFF0;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0px 0px 12px rgba(0,0,0,0.1);
        margin-bottom: 30px;
    }
    .welcome-heading {
        font-size: 28px;
        font-weight: bold;
        color: #228B22;
        text-align: center;
    }
    .welcome-text {
        font-size: 18px;
        text-align: center;
        color: #444;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="welcome-box">
    <div class="welcome-heading">🌱 Welcome to SkillBloom AI</div>
    <p class="welcome-text">
        Ready to discover your perfect career path? <br>
        Powered by AI, SkillBloom helps you turn your interests into action.<br>
        Select your area of interest and let us guide you with tailored suggestions, skills, and free learning resources.
    </p>
</div>
""", unsafe_allow_html=True)

# === Setup SkillAgent only once ===
if "agent" not in st.session_state:
    st.session_state.agent = SkillAgent(config={})

# === Career Input Section ===
st.markdown("### 🎯 Tell us about your goals")

interest_area = st.selectbox(
    "Select a broad interest area:",
    ["AI", "Web Development", "Design", "Data Science", "Cybersecurity", "Marketing", "Other"]
)

experience_level = st.radio(
    "What's your experience level?",
    ["Beginner", "Intermediate", "Advanced"]
)

custom_input = st.text_input("Or type your specific interest or skill")

# === Run AI Logic ===
if st.button("🌱 Suggest Careers"):
    user_text = custom_input.strip() or interest_area

    prompt = f"""
User interest: {user_text}
Stage: {experience_level}

Please provide **in-depth AI-powered career guidance**:
- Suggest 3 suitable career paths.
- For each career path, include:
    - A short job role description (2–3 lines)
    - 3–4 essential skills
    - 1 free course/resource with title and URL
    - A brief growth path (e.g., Junior → Mid-Level → Senior)

Format cleanly in Markdown with bullet points and headings. Avoid generic advice. Only give relevant and detailed info.
"""

    with st.spinner("Thinking... 🔍"):
        message = Message(
            payload={"text": prompt, "context": "career_mentor"},
            sender="user",
            receiver="SkillAgent"
        )
        response = st.session_state.agent.execute(message)
        st.session_state.last_result = response.payload["text"]

# === Display Output Safely ===
if "last_result" in st.session_state:
    st.markdown("### 🔍 AI Career Suggestions:")
    try:
        cleaned_output = st.session_state.last_result[:4000]
        st.markdown(cleaned_output, unsafe_allow_html=False)
    except Exception:
        st.error("⚠️ Could not display suggestions. Showing as plain text.")
        st.code(st.session_state.last_result)

    st.download_button(
        label="📥 Download Suggestions as .txt",
        data=st.session_state.last_result,
        file_name="skillbloom_career_suggestions.txt",
        mime="text/plain"
    )
