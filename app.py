import streamlit as st
import json
from src.utils import normalize_text, compute_similarity, check_speech_patterns

# 預設人格（簡化範例）
with open("configs/settings.yaml", "r", encoding="utf-8") as f:
    persona = json.load(open("data/base_persona.json"))

st.set_page_config(page_title="PersonaChain 一致性分析", layout="centered")
st.title("🧠 Persona Consistency Checker")
st.markdown("輸入一句話，檢查它是否與預設人格一致")

utterance = st.text_input("請輸入語句", placeholder="例如：我從來沒輸過")

if utterance:
    utt_norm = normalize_text(utterance)
    sim_score = compute_similarity(utt_norm, persona)
    pattern_hits = check_speech_patterns(utt_norm)
    inconsistency_flag = sim_score < 0.5

    st.markdown("### 分析結果")
    st.markdown(f"- 相似度分數：`{sim_score:.2f}`")
    st.markdown(f"- 命中語言特徵：`{pattern_hits}`")
    st.markdown(f"- 是否偏離人格：{'❌ 是' if inconsistency_flag else '✅ 否'}")
