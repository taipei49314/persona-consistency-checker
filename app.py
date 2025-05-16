
import streamlit as st
import json
import yaml
from src.utils import normalize_text, compute_similarity, check_speech_patterns
from datetime import datetime

st.set_page_config(page_title="PersonaChain v2.0", layout="centered")
st.title("🧠 PersonaChain v2.0｜語言人格分析器")

# 綽號輸入區（角色識別）
nickname = st.text_input("請輸入你的綽號 / Your Persona Nickname", max_chars=20)

if nickname:
    st.success(f"👤 目前分析角色：{nickname}")

    lang = st.selectbox("請選擇語言 / Select Language", ["zh", "en", "ja", "ko"], index=0)

    persona_file = f"data/base_persona_{lang}.json"
    pattern_file = f"data/patterns_{lang}.yaml"

    with open(persona_file, "r", encoding="utf-8") as f:
        persona = json.load(f)

    with open(pattern_file, "r", encoding="utf-8") as f:
        pattern_data = yaml.safe_load(f)
        pattern_hits = pattern_data.get("patterns", [])

    st.markdown("請輸入一句或多句話（每行一句）：")

    multi_input = st.text_area("語句輸入區 / Input Zone", height=200)

    if multi_input:
        st.divider()
        st.markdown("## 分析結果 / Analysis Result")
        lines = [line.strip() for line in multi_input.strip().splitlines() if line.strip()]
        drift_count = 0
        total_score = 0
        records = []

        for i, utt in enumerate(lines, 1):
            utt_norm = normalize_text(utt)
            sim_score = compute_similarity(utt_norm, persona)
            matched = [kw for kw in pattern_hits if kw in utt_norm]
            inconsistent = sim_score < 0.5
            drift_count += int(inconsistent)
            total_score += sim_score

            records.append({
                "nickname": nickname,
                "sentence": utt,
                "language": lang,
                "score": round(sim_score, 3),
                "patterns_hit": matched,
                "drift": inconsistent,
                "timestamp": datetime.now().isoformat()
            })

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

        st.download_button(
            label="📥 下載本次語句分析結果（JSON）",
            data=json.dumps(records, ensure_ascii=False, indent=2),
            file_name=f"{nickname}_persona_records.json",
            mime="application/json"
        )
else:
    st.warning("請先輸入你的綽號才能開始分析 / Please enter your nickname.")

# 載入每日任務題庫
with open("data/daily_missions.json", "r", encoding="utf-8") as f:
    missions = json.load(f)

import random
daily = random.choice(missions)
st.divider()
st.markdown("## 🎯 Persona Daily Mission · 每日任務")
st.markdown(f"**類型：{daily['type']}**")
st.markdown(f"📌 **題目：{daily['prompt']}**")
user_daily_input = st.text_area("請輸入你會怎麼說 / What would you say?", key="daily_input", height=100)

if user_daily_input and nickname:
    utt_norm = normalize_text(user_daily_input)
    sim_score = compute_similarity(utt_norm, persona)
    matched = [kw for kw in pattern_hits if kw in utt_norm]
    inconsistent = sim_score < 0.5

    st.markdown("### 🧪 分析結果")
    st.markdown(f"- 語句內容：`{user_daily_input}`")
    st.progress(sim_score, text=f"一致性分數：{sim_score:.2f}")
    st.markdown(f"- 命中語氣特徵：{matched}")
    st.markdown(f"- 判定：{'❌ 偏離語氣' if inconsistent else '✅ 一致'}")

    mission_record = {
        "nickname": nickname,
        "mission_id": daily["id"],
        "mission_type": daily["type"],
        "mission_prompt": daily["prompt"],
        "input": user_daily_input,
        "language": lang,
        "score": round(sim_score, 3),
        "patterns_hit": matched,
        "drift": inconsistent,
        "timestamp": datetime.now().isoformat()
    }

    st.download_button(
        "📥 下載任務結果（JSON）",
        data=json.dumps(mission_record, ensure_ascii=False, indent=2),
        file_name=f"{nickname}_mission_{daily['id']}.json",
        mime="application/json"
    )
