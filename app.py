
import streamlit as st
import json
import yaml
from datetime import datetime
from src.utils import normalize_text, compute_similarity, check_speech_patterns

st.set_page_config(page_title="PersonaChain v2.2", layout="centered")
st.title("🧠 PersonaChain v2.2｜五題語氣測驗")

# 輸入綽號
nickname = st.text_input("請輸入你的綽號 / Your Persona Nickname", max_chars=20)
if not nickname:
    st.warning("請先輸入綽號才能進行測驗。")
    st.stop()
else:
    st.success(f"🎯 現在測驗角色：{nickname}")

# 語言選單
lang = st.selectbox("請選擇語言 / Language", ["zh", "en", "ja", "ko"], index=0)

# 載入語氣設定
with open(f"data/base_persona_{lang}.json", "r", encoding="utf-8") as f:
    persona = json.load(f)

with open(f"data/patterns_{lang}.yaml", "r", encoding="utf-8") as f:
    pattern_data = yaml.safe_load(f)
    pattern_hits = pattern_data.get("patterns", [])

# 載入題庫
with open("data/v22_five_questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

st.divider()
st.markdown("## 📝 五題語言挑戰")

records = []
total_score = 0
drift_count = 0

for i, q in enumerate(questions, 1):
    st.markdown(f"### ❓ 題目 {i}：({q['type']})")
    st.markdown(f"{q['prompt']}")
    user_input = st.text_input(f"你會怎麼說？", key=f"q{i}")

    if user_input:
        norm = normalize_text(user_input)
        score = compute_similarity(norm, persona)
        matched = [kw for kw in pattern_hits if kw in norm]
        drift = score < 0.5
        drift_count += int(drift)
        total_score += score

        st.progress(score, text=f"一致性分數：{score:.2f}")
        st.markdown(f"- 命中語氣特徵：{matched}")
        st.markdown(f"- 判定：{'❌ 偏離語氣' if drift else '✅ 一致'}")

        records.append({
            "nickname": nickname,
            "question_id": q["id"],
            "type": q["type"],
            "prompt": q["prompt"],
            "input": user_input,
            "score": round(score, 3),
            "patterns_hit": matched,
            "drift": drift,
            "timestamp": datetime.now().isoformat()
        })

# 結果彙總
if len(records) == 5:
    st.divider()
    st.markdown("## 📊 測驗總結")

    avg_score = total_score / 5
    st.metric("總平均一致性分數", f"{avg_score:.2f}")
    st.metric("偏離語氣句數", f"{drift_count} / 5")

    if avg_score >= 0.85:
        summary = "你語氣高度一致，具備明確人格風格與語言穩定性。"
    elif avg_score >= 0.65:
        summary = "你語氣有一定一致性，但在特定場景下會有所波動。"
    else:
        summary = "你語氣較多變，可能受情緒、語境影響顯著。"

    st.success(f"🧠 語氣人格分析：{summary}")

    st.download_button(
        label="📥 下載本次 5 題測驗結果",
        data=json.dumps(records, ensure_ascii=False, indent=2),
        file_name=f"{nickname}_v22_five_test.json",
        mime="application/json"
    )
