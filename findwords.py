from gensim.models import Word2Vec

model_a = Word2Vec.load("models/model_a_2.w2v")
model_b = Word2Vec.load("models/model_b_2.w2v")

# Get words sorted by frequency (Sanity check to verify preprocessing)
def get_vocab_freq(model, topn=500):
    vocab = [(word, model.wv.get_vecattr(word, 'count'))
             for word in model.wv.key_to_index]
    return sorted(vocab, key=lambda x: x[1], reverse=True)[:topn]

print("=== CORPUS A TOP 500 ===")
for word, count in get_vocab_freq(model_a):
    print(f"{word}: {count}")

print("\n=== CORPUS B TOP 500 ===")
for word, count in get_vocab_freq(model_b):
    print(f"{word}: {count}")