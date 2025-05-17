
import streamlit as st
import json
import os
from src.consistency_checker import check_consistency
from src.logger import get_logger

logger = get_logger("StreamlitUI")

st.set_page_config(layout="wide", page_title="Persona Consistency Checker", page_icon="🧠")
st.markdown("# 🧠 Persona Consistency Checker")
st.caption("Analyze persona consistency across dialogues, tests, and identity arenas.")

# Sidebar mode selector
mode = st.sidebar.selectbox("Select analysis mode", ["Multi-Turn Dialogue", "Five-Question Test", "Arena Comparison"])

# Utility functions
def load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def flatten_sessions(data):
    flat = []
    sessions = data.get("sessions", [])
    for session in sessions:
        utterances = session.get("utterances", [])
        for i in range(0, len(utterances)-1, 2):
            flat.append({"user": utterances[i], "bot": utterances[i+1]})
    return flat

def flatten_json(d):
    flat = []
    for k, v in d.items():
        if isinstance(v, list):
            flat.extend([str(i) for i in v])
        else:
            flat.append(str(v))
    return " ".join(flat)

# Mode 1: Multi-Turn Dialogue
if mode == "Multi-Turn Dialogue":
    st.subheader("📂 Multi-Turn Dialogue Input")
    dialogue_data = load_json("./data/test_dialogues.json")
    sessions = flatten_sessions(dialogue_data)
    if sessions:
        for i, pair in enumerate(sessions):
            st.markdown(f"**User {i+1}:** {pair['user']}  
**Bot:** {pair['bot']}")
    else:
        st.warning("No valid session data found.")

    if st.button("🔍 Run Consistency Analysis"):
        result = check_consistency(sessions)
        st.success("Analysis Complete")
        st.metric("Consistency Score", result.get("consistency_score", 0))
        with st.expander("🔬 Detailed Result"):
            st.json(result)

# Mode 2: Five-Question Test
elif mode == "Five-Question Test":
    st.subheader("📝 Answer 5 Fixed Personality Questions")
    qdata = load_json("./data/v22_five_questions.json")
    questions = list(qdata.values()) if isinstance(qdata, dict) else qdata
    answers = []

    for q in questions:
        ans = st.text_area(f"Q{q['id']}: {q['text']}", key=f"q{q['id']}")
        if ans:
            answers.append({"user": q["text"], "bot": ans})

    if st.button("🔍 Analyze My Consistency"):
        result = check_consistency(answers)
        st.success("Test Completed")
        st.metric("Consistency Score", result.get("consistency_score", 0))
        with st.expander("🧾 Test Result Details"):
            st.json(result)

# Mode 3: Arena Comparison
elif mode == "Arena Comparison":
    st.subheader("⚔️ Compare Two Personas")
    persona_a = load_json("./data/base_persona_zh.json")
    persona_b = load_json("./data/base_persona_en.json")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🧠 Persona A (ZH)")
        st.json(persona_a)
    with col2:
        st.markdown("### 🧠 Persona B (EN)")
        st.json(persona_b)

    if st.button("⚖️ Compare Personas"):
        merged = [{"user": flatten_json(persona_a), "bot": flatten_json(persona_b)}]
        result = check_consistency(merged)
        st.metric("Persona Similarity Score", result.get("consistency_score", 0))
        with st.expander("📊 Arena Evaluation Details"):
            st.json(result)
