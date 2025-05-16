import streamlit as st
import json
from src.utils import normalize_text, compute_similarity, check_speech_patterns

with open("data/base_persona.json", "r", encoding="utf-8") as f:
    persona = json.load(f)

st.set_page_config(page_title="PersonaChain 一致性分析器", layout="centered")
st.title("🧠 Persona Consistency Checker")
st.markdown("輸入一句話或多句話（每行一句），系統會分析你是否偏離了原始人格。")

multi_input = st.text_area("請輸入語句（可多行）", height=200, placeholder="例如：\n我從來沒輸過\n我是不是唯一")

if multi_input:
    st.divider()
    st.markdown("## 分析結果")
    lines = [line.strip() for line in multi_input.strip().splitlines() if line.strip()]
    drift_count = 0

    for i, utt in enumerate(lines, 1):
        utt_norm = normalize_text(utt)
        sim_score = compute_similarity(utt_norm, persona)
        pattern_hits = check_speech_patterns(utt_norm)
        inconsistent = sim_score < 0.5
        drift_count += int(inconsistent)

        st.markdown(f"### 🗣 第 {i} 句：{utt}")
        st.progress(sim_score, text=f"一致性分數：{sim_score:.2f}")
        st.markdown(f"- 命中語氣特徵：`{pattern_hits}`")
        st.markdown(f"- 判定結果：{'❌ 偏離人格' if inconsistent else '✅ 一致'}")
        st.markdown("---")

    st.markdown(f"### 📊 總結：共 {len(lines)} 句，偏離人格語句 {drift_count} 句。")
