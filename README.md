# 🌱 SkillBloom AI

SkillBloom is an AI-powered platform built with Google Cloud’s Agent Development Kit (ADK), Streamlit, and Python that helps learners bridge skill gaps, prepare for interviews, enhance resumes, and receive career guidance — all in one place.

---

## 🚀 Features

### 1. 🧠 Skill Enhancer
Personalized suggestions to improve your chosen skill with resource links, project ideas, and learning tracks.

### 2. 💼 AI-Powered Job Board
Smart job listings enhanced with AI-based skill suggestions and role matching.

### 3. 🕳️ Career Gap Filler AI
Enter your current skill level, interests, or gaps — get actionable steps to fill them and pivot careers.

### 4. 📄 Resume Analyzer + ATS Score Checker
Upload your resume and a job description to get feedback and a simulated ATS score to boost your chances.

### 5. 🧭 Your Mentor Dashboard (Alex Rivera)
An AI career mentor who provides personalized support, progress tracking, and weekly growth plans.

---

## 💡 How It Works

SkillBloom uses a custom `SkillAgent` built with ADK and deployed locally via Streamlit. It connects various modules — skill enhancement, job analysis, resume parsing, and career guidance — into one unified dashboard.

---

## 🛠️ Tech Stack

- **Streamlit** (Frontend UI)
- **Python** (Backend logic)
- **Google Cloud ADK** (Agent Development Kit)
- **LangChain** (Agent orchestration)
- **Open-source LLMs** or **Groq/Gemini APIs** (for AI responses)
- **.env config** (for secure key management)

---




## 🏁 How to Run Locally

```bash
git clone https://github.com/YOUR_USERNAME/skillbloom-adk.git
cd skillbloom-adk
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
streamlit run streamlit_app.py

