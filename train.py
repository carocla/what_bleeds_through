from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import numpy as np
import time
import os

# LineSentence streams from disk instead of loading everything into RAM
# cleaner and more memory efficient, doesn't matter much at 3M tokens but good practice
corpus_a = LineSentence("samples_A_clean/corpus_A.txt")
corpus_b = LineSentence("samples_B_clean/corpus_B.txt")
cpu_count = os.cpu_count()

params = {
    "vector_size": 100,
    "window": 10,       # bumped from 5 — broader context for semantic associations
    "min_count": 10,
    "workers": cpu_count,
    "epochs": 20,
    "sg": 1,           # skip-gram better for small dataset
    "negative": 5,    # make false pairs for contrast
    "seed": 42,
    "sample": 1e-3
}

for name, corpus in [("A", corpus_a), ("B", corpus_b)]:
    print(f"\nTraining Corpus {name}...")
    start = time.time()
    model = Word2Vec(corpus, **params)
    print(f"Vocabulary size: {len(model.wv):,} words")
    print(f"Done in {time.time() - start:.1f}s")
    model.save(f"model_{name.lower()}_3.w2v")
    print(f"Model saved as model_{name.lower()}_3.w2v")


def cosine_distribution(model_):
    words = list(model_.wv.key_to_index)[:1000]
    sims = []
    for i in range(len(words)-1):
        sims.append(model_.wv.similarity(words[i], words[i+1]))
    print("Mean cosine:", np.mean(sims))