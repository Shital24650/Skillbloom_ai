import streamlit as st
from agents.skill_enhancer_agent.base import SkillEnhancerAI  # ✅ Use dedicated agent
from adk.type_defs import Message

st.set_page_config(page_title="Skill Enhancer", page_icon="📚")

st.title("📚 Skill Enhancer")
st.subheader("Get a complete skill roadmap and career insights for your dream job")

career_goal = st.text_input("🎯 Enter your target career (e.g., Data Analyst, AI Engineer)")

if "enhancer_agent" not in st.session_state:
    st.session_state.enhancer_agent = SkillEnhancerAI()

if st.button("🚀 Enhance My Skills"):
    if career_goal.strip() == "":
        st.warning("⚠️ Please enter a valid career goal.")
    else:
        with st.spinner("Generating personalized roadmap... 🛠️"):
            prompt = f"""
I want to become a {career_goal}.

Please provide a complete skill roadmap structured as follows:

---

## 🗺️ Career Overview
- What this role does
- Key responsibilities
- Future scope

## 🏢 Top Hiring Companies
- 3–5 companies hiring for this role
- What tools/skills/qualifications they expect

## 📆 Weekly Learning Plan (5–6 Weeks)
- Week-by-week structured plan
- Each week: what to learn, what to build/do, and 1 free resource with link

## 🛠️ Final Project Idea
- A project to showcase the learned skills practically

## 🎯 Career Launch Tips
- Portfolio tips
- Where to apply
- How to stand out

---

Make the output professional, clean Markdown, and easy to read.
Do not include general advice or filler text.
"""
            message = Message(payload={"text": prompt}, sender="user", receiver="SkillEnhancer")
            response = st.session_state.enhancer_agent.execute(message)

            st.markdown("### 🧠 Recommended Skills and Roadmap:")
            st.markdown(response.payload["text"])
