def summarize_results(responses):
    total_score = 0
    deviation_count = 0
    trait_counter = {}

    for r in responses:
        score = r["score"]
        total_score += score
        if score < 70:
            deviation_count += 1

        for trait in r["traits"]:
            trait_counter[trait] = trait_counter.get(trait, 0) + 1

    avg_score = round(total_score / len(responses), 1)
    sorted_traits = sorted(trait_counter.items(), key=lambda x: x[1], reverse=True)
    tone_label = sorted_traits[0][0] if sorted_traits else "中性"

    return avg_score, deviation_count, tone_label
