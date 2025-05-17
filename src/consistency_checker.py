import json
from src.utils import normalize_text, compute_similarity, check_speech_patterns

def load_data(persona_path, dialogue_path):
    with open(persona_path, 'r') as f:
        persona = json.load(f)
    with open(dialogue_path, 'r') as f:
        dialogues = json.load(f)
    return persona, dialogues

def analyze_consistency(persona, dialogues):
    results = []
    traits = persona['traits']
    patterns = persona['speech_patterns']
    print(f"Analyzing consistency for traits: {traits}\n")

    for session in dialogues['sessions']:
        session_result = {
            "id": session['id'],
            "utterances": []
        }
        print(f"Session: {session['id']}")
        for utt in session['utterances']:
            norm_utt = normalize_text(utt)
            sim_score = compute_similarity(norm_utt, traits)
            pattern_hits = check_speech_patterns(norm_utt, patterns)
            out = {
                "text": utt,
                "similarity_score": sim_score,
                "pattern_matched": pattern_hits,
                "inconsistency_flag": sim_score < 0.4
            }
            session_result['utterances'].append(out)
            print(f'- "{utt}" => Score: {sim_score:.2f}, Patterns: {pattern_hits}, Inconsistent: {out["inconsistency_flag"]}')
        results.append(session_result)

    return results

if __name__ == "__main__":
    persona, dialogues = load_data('data/base_persona.json', 'data/test_dialogues.json')
    report = analyze_consistency(persona, dialogues)
    with open('reports/consistency_report.json', 'w') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)


def check_consistency(dialogues):
    if not dialogues or not isinstance(dialogues, list):
        return {"error": "Invalid dialogue format"}

    consistency_score = 0
    for d in dialogues:
        u = d.get("user", "")
        b = d.get("bot", "")
        if u and b:
            diff = abs(len(u) - len(b))
            consistency_score += max(0, 100 - diff)

    avg_score = consistency_score / len(dialogues) if dialogues else 0
    return {
        "consistency_score": round(avg_score, 2),
        "dialogue_count": len(dialogues),
        "summary": "Mock consistency score based on length difference"
    }
