import numpy as np
from gensim.models import Word2Vec
import json
from axes_config import axes
import os
model_a = Word2Vec.load("models/model_a_2.w2v")
model_b = Word2Vec.load("models/model_b_2.w2v")

def axis_quality_check(model, axes, name):
    print(f"\n=== {name} AXIS QUALITY CHECK ===")

    for name, config in axes.items():
        valid_p1 = [w for w in config["pole1"] if w in model.wv]
        valid_p2 = [w for w in config["pole2"] if w in model.wv]
        missing_p1 = [w for w in config["pole1"] if w not in model.wv]
        missing_p2 = [w for w in config["pole2"] if w not in model.wv]

        if len(valid_p1) < 2 or len(valid_p2) < 2:
            print(f"{name}: ⚠️ weak (too many missing anchors)")
        else:
            print(f"{name}: OK ({len(valid_p1)} vs {len(valid_p2)} anchors)")

        if missing_p1:
            print(f"    -> Missing from pole1: {', '.join(missing_p1)}")
        if missing_p2:
            print(f"    -> Missing from pole2: {', '.join(missing_p2)}")

def cosine_diagnostic(model, name):
    print(f"\n=== {name} Cosine Distribution ===")

    words = list(model.wv.key_to_index)[:1000]
    sims = []

    for i in range(len(words)-1):
        sims.append(model.wv.similarity(words[i], words[i+1]))

    mean_sim = np.mean(sims)
    print(f"Mean cosine similarity: {mean_sim:.4f}")

# --- diagnostics ---
cosine_diagnostic(model_a, "Corpus A")
cosine_diagnostic(model_b, "Corpus B")

# axis_quality_check(model_a, axes, "Corpus A")
# axis_quality_check(model_b, axes, "Corpus B")

print("Corpus A - Sword & Blade:", model_a.wv.similarity('sword', 'blade'))
print("Corpus A - Sword & Apple:", model_a.wv.similarity('sword', 'apple'))
print("Corpus B - Sword & Blade:", model_b.wv.similarity('sword', 'blade'))
print("Corpus B - Sword & Apple:", model_b.wv.similarity('sword', 'apple'))

# Evaluate model_a
print("\n=== Model A Analogy: King - Man + Woman ===")
result_a = model_a.wv.most_similar(positive=['king', 'woman'], negative=['man'], topn=10)
for word, similarity in result_a:
    print(f"{word}: {similarity:.4f}")

# Evaluate model_b
print("\n=== Model B Analogy: King - Man + Woman ===")
result_b = model_b.wv.most_similar(positive=['king', 'woman'], negative=['man'], topn=10)
for word, similarity in result_b:
    print(f"{word}: {similarity:.4f}")



def pole_score(model, word, anchors):
    """Average cosine similarity from word to anchor words."""
    scores = []
    missing = []
    anchors = [a for a in anchors if a in model.wv]
    for anchor in anchors:
        if anchor in model.wv and word in model.wv:
            scores.append(model.wv.similarity(word, anchor))
        else:
            missing.append(anchor)
    if missing:
        print(f"  [!] missing anchors: {missing}")
    return float(np.mean(scores)) if scores else None

def analyze_word(word, config, model_a, model_b):
    p1, p2 = config["pole1_name"], config["pole2_name"]
    print(f"\n{'='*55}")
    print(f"  WORD: '{word.upper()}'")
    print(f"  Axis: [{p1}] <-----> [{p2}]")
    print(f"{'='*55}")

    results = {}
    for label, model in [("Corpus A (translated)", model_a),
                          ("Corpus B (original)",  model_b)]:

        if word not in model.wv:
            print(f"\n  {label}: '{word}' not in vocabulary — skipping")
            results[label] = None
            continue

        s1 = pole_score(model, word, config["pole1"])
        s2 = pole_score(model, word, config["pole2"])

        if s1 is None or s2 is None:
            results[label] = None
            continue

        diff = s1 - s2
        lean = p1 if diff > 0 else p2
        strength = abs(diff)

        results[label] = {
            "pole1": float(s1),
            "pole2": float(s2),
            "diff": float(diff)
        }

        print(f"\n  {label}:")
        print(f"    {p1:<20} score: {s1:.4f}")
        print(f"    {p2:<20} score: {s2:.4f}")
        print(f"    difference:          {diff:+.4f}")
        print(f"    --> leans [{lean}]  (strength: {strength:.4f})")

        # Top 5 neighbors for qualitative texture
        neighbors = [w for w, _ in model.wv.most_similar(word, topn=8)
                     if w not in config["pole1"] + config["pole2"]][:5]
        print(f"    top neighbors: {neighbors}")

    # Cross-corpus comparison
    a = results.get("Corpus A (translated)")
    b = results.get("Corpus B (original)")
    if a and b:
        shift = a["diff"] - b["diff"]
        print(f"\n  AXIS SHIFT (A minus B): {shift:+.4f}")
        if abs(shift) < 0.02:
            print(f"  --> minimal difference between corpora")
        elif shift > 0:
            print(f"  --> Corpus A pulls '{word}' more toward [{p1}]")
        else:
            print(f"  --> Corpus B pulls '{word}' more toward [{p1}]")

    return results

all_results = {}
for word, config in axes.items():
    all_results[word] = analyze_word(word, config, model_a, model_b)

# Summary table
print(f"\n\n{'='*55}")
print("  SUMMARY — axis lean by corpus")
print(f"{'='*55}")
print(f"  {'word':<12} {'A leans':<20} {'B leans':<20} {'shift':>8}")
print(f"  {'-'*58}")
for word, config in axes.items():
    res = all_results[word]
    a = res.get("Corpus A (translated)")
    b = res.get("Corpus B (original)")
    p1, p2 = config["pole1_name"], config["pole2_name"]
    a_lean = p1 if (a and a["diff"] > 0) else p2 if a else "N/A"
    b_lean = p1 if (b and b["diff"] > 0) else p2 if b else "N/A"
    shift = (a["diff"] - b["diff"]) if (a and b) else float("nan")
    print(f"  {word:<12} {a_lean:<20} {b_lean:<20} {shift:>+8.4f}")

os.makedirs("results", exist_ok=True)
with open("results/axis_results.json", "w") as f:
    json.dump(all_results, f, indent=2)
print("Saved results to results/axis_results.json")