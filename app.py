
import streamlit as st
import json
import yaml
from src.utils import normalize_text, compute_similarity, check_speech_patterns

st.set_page_config(page_title="PersonaChain Analyzer", layout="centered")
st.title("🧠 Persona Consistency Checker")

# 語言選單
lang = st.selectbox("請選擇語言 / Select Language", ["zh", "en", "ja", "ko"], index=0)

# 載入對應的 persona & pattern
persona_file = f"data/base_persona_{lang}.json"
pattern_file = f"data/patterns_{lang}.yaml"

with open(persona_file, "r", encoding="utf-8") as f:
    persona = json.load(f)

with open(pattern_file, "r", encoding="utf-8") as f:
    pattern_data = yaml.safe_load(f)
    pattern_hits = pattern_data.get("patterns", [])

st.markdown("請輸入一句或多句話，每行一句。\nPaste one or more sentences below:")

multi_input = st.text_area("語句輸入區", height=200)

if multi_input:
    st.divider()
    st.markdown("## 分析結果 / Analysis Result")
    lines = [line.strip() for line in multi_input.strip().splitlines() if line.strip()]
    drift_count = 0
    total_score = 0

    for i, utt in enumerate(lines, 1):
        utt_norm = normalize_text(utt)
        sim_score = compute_similarity(utt_norm, persona)
        matched = [kw for kw in pattern_hits if kw in utt_norm]
        inconsistent = sim_score < 0.5
        drift_count += int(inconsistent)
        total_score += sim_score

        st.markdown(f"### ✏️ 第 {i} 句 / Sentence {i}")
        st.markdown(f"- 語句 / Text: `{utt}`")
        st.progress(sim_score, text=f"一致性分數 / Score: {sim_score:.2f}")
        st.markdown(f"- 命中語氣特徵 / Patterns: `{matched}`")
        st.markdown(f"- 判定結果 / Consistency: {'❌ 偏離 / Drift' if inconsistent else '✅ 一致 / Consistent'}")
        st.markdown("---")

    avg_score = total_score / len(lines)
    lang_summary = {
        "zh": f"🧠 總體一致性分數：{avg_score:.2f} ／ 偏離句數：{drift_count} ／ 共 {len(lines)} 句",
        "en": f"🧠 Overall consistency score: {avg_score:.2f} ／ {drift_count} drifted out of {len(lines)} sentences",
        "ja": f"🧠 一貫性スコア：{avg_score:.2f} ／ {len(lines)} 文のうち {drift_count} 文が逸脱",
        "ko": f"🧠 일관성 점수: {avg_score:.2f} ／ 총 {len(lines)}문 중 {drift_count}문 일탈"
    }

    st.success(lang_summary[lang])
