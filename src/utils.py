from difflib import SequenceMatcher

def normalize_text(text):
    return text.lower().strip()

def compute_similarity(text, traits):
    keys = ' '.join(traits.keys())
    ratio = SequenceMatcher(None, text, keys).ratio()
    return round(ratio, 2)

def check_speech_patterns(text, patterns):
    matches = [p for p in patterns if p in text]
    return matches
