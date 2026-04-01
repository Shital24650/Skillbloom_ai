```python
import streamlit as st
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# === PIPELINE IMPORTS ===
from pipeline.context_model import extract_context
from pipeline.task_decomposer import decompose_tasks
from pipeline.agent_executor import execute_tasks
from pipeline.plan_synthesizer import synthesize_plan

# === EVALUATION IMPORTS ===
from evaluation.baseline_llm import baseline
from evaluation.evaluator import evaluate

# === PAGE CONFIG ===
st.set_page_config(page_title="SkillBloom AI", page_icon="🌱", layout="centered")

# === UI STYLING (KEEP THIS) ===
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

# === HEADER ===
st.markdown("""
<div class="welcome-box">
    <div class="welcome-heading">⚔️ SkillBloom AI</div>
    <p class="welcome-text">
        Structured Career Intelligence System<br>
        Transforming vague queries into actionable career plans using multi-step reasoning.
    </p>
</div>
""", unsafe_allow_html=True)

# === INPUT SECTION ===
st.markdown("### 🎯 Enter Your Career Query")

interest_area = st.selectbox(
    "Select a broad interest area:",
    ["AI", "Web Development", "Design", "Data Science", "Cybersecurity", "Marketing", "Other"]
)

experience_level = st.radio(
    "What's your experience level?",
    ["Beginner", "Intermediate", "Advanced"]
)

custom_input = st.text_input("Or type your specific interest or goal")

# === EXECUTION BUTTON ===
if st.button("⚔️ Generate Structured Plan"):

    query = custom_input.strip() or interest_area

    if not query:
        st.warning("Please enter a query.")
        st.stop()

    with st.spinner("Running structured reasoning pipeline..."):

        # STEP 1: Context Extraction
        context = extract_context(query)

        # STEP 2: Task Decomposition
        tasks = decompose_tasks(context)

        # STEP 3: Agent Execution
        results = execute_tasks(tasks, context)

        # STEP 4: Plan Synthesis
        final_output = synthesize_plan(results)

        # STEP 5: Baseline LLM
        baseline_output = baseline(query)

        # STEP 6: Evaluation
        scores = evaluate(final_output, baseline_output)

        # SAVE TO SESSION
        st.session_state.final_output = final_output
        st.session_state.scores = scores
        st.session_state.context = context
        st.session_state.tasks = tasks

        # === LOGGING ===
        os.makedirs("logs", exist_ok=True)

        with open("logs/run.json", "w") as f:
            json.dump({
                "query": query,
                "context": context,
                "tasks": tasks,
                "output": final_output,
                "scores": scores
            }, f, indent=4)

# === OUTPUT DISPLAY ===
if "final_output" in st.session_state:

    st.subheader("📌 Structured Career Plan")
    st.json(st.session_state.final_output)

    st.subheader("📊 Evaluation Scores")
    st.json(st.session_state.scores)

    with st.expander("🔍 Debug: Pipeline Details"):
        st.write("Context:", st.session_state.context)
        st.write("Tasks:", st.session_state.tasks)

    st.success("✅ Pipeline executed successfully and logged!")
```
