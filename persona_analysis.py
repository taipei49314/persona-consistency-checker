def analyze_tone(user_input):
    if not user_input.strip():
        return 0, []

    traits = []
    score = 80

    if any(word in user_input.lower() for word in ["我認為", "根據", "因此"]):
        traits.append("理性")
        score += 5
    if any(word in user_input.lower() for word in ["不妥協", "堅持", "原則"]):
        traits.append("堅定")
        score += 5
    if any(word in user_input.lower() for word in ["你覺得呢", "我們", "可以一起"]):
        traits.append("協作")
        score -= 10
    if any(word in user_input.lower() for word in ["爛", "廢", "笑死"]):
        traits.append("諷刺")
        score -= 15

    score = min(max(score, 0), 100)
    if not traits:
        traits = ["中性"]

    return score, traits
