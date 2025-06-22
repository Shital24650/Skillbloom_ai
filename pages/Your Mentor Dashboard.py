import streamlit as st
from agents.mentor_agent.base import MentorAgent  # ✅ Use dedicated mentor agent
from adk.type_defs import Message

st.set_page_config(page_title="🧭 Your Mentor Dashboard", layout="centered")

# Initialize AI Agent
if "mentor_agent" not in st.session_state:
    st.session_state.mentor_agent = MentorAgent(config={})

# Mentor Info Section
st.title("🧭 Your Mentor Dashboard")
st.subheader("Stay connected with your AI mentor and track your growth")

st.markdown("### 👤 Your Mentor")
st.markdown("""
**Name:** Alex Rivera  
**Expertise:** Career Strategy, Interview Prep  
**Style:** Supportive, Strategic, Realistic
""")

# Weekly Plan
st.markdown("### 📅 Weekly Check-In Plan")
checklist = [
    "Week 1: Define your learning path & daily habit",
    "Week 2: Build a portfolio project",
    "Week 3: Improve resume + LinkedIn",
    "Week 4: Practice mock interviews",
    "Week 5: Apply to real roles & review results"
]
for item in checklist:
    st.checkbox(item, key=item)

# Ask Your Mentor
st.markdown("### 🤖 Ask Your Mentor")
user_query = st.text_area("💬 Your Question:", placeholder="e.g. How can I switch to a career in data science?")

# Display Chat History
if "mentor_chat" not in st.session_state:
    st.session_state.mentor_chat = []

if st.button("📩 Send to Mentor") and user_query.strip():
    with st.spinner("Thinking..."):
        prompt = f"""
Your name is Alex Rivera. You are a warm, friendly, and experienced AI career mentor in the SkillBloom app.

Speak conversationally and supportively. Give advice, encouragement, and suggestions based on what the user asks.

Only suggest career paths if the user asks **explicitly** for:
- how to become [X]
- career roadmap
- job options
- what career suits me
- learning path for a goal

If the user just says hi or something casual, greet them politely and ask a follow-up question to understand their goal.

User: {user_query.strip()}
Alex:
"""
        msg = Message(payload={"text": prompt}, sender="user", receiver="MentorAgent")
        response = st.session_state.mentor_agent.execute(msg)
        reply = response.payload["text"].strip()

        # Save chat
        st.session_state.mentor_chat.append(("You", user_query.strip()))
        st.session_state.mentor_chat.append(("Alex (Mentor)", reply))

# Chat History Display
if st.session_state.mentor_chat:
    st.markdown("### 🧠 Mentor Chat History")
    for sender, message in st.session_state.mentor_chat:
        st.markdown(f"**{sender}:** {message}")
