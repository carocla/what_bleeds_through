# What Bleeds Through: An Embedding-Based Case Study of Conceptual Associations in Translated Fiction

**Caro Claeson - Independent Research Project**

---

## Motivation

In R.F. Kuang's *Babel*, translation is an act of loss. The gap between a word and its closest equivalent in another language 
is where meaning gets left behind. When a Chinese novel is translated into English, the English words we end up with are influenced
not just by English literary conventions, but by the culture of the source language.

This project asks whether that weight is measurable. If *tiān*, heaven, in Chinese fiction carries associations of cosmic order, fate, 
and celestial power, what happens when it is translated simply as "heaven" in English? Does that English word occupy a different semantic
neighborhood than it would in fiction originally written in English? Does the translated "heaven" pull closer to the 
transcendent and the fated, while the native English "heaven" lands closer to the mundane and the theological?

**Hypothesis:** Selected words in translated Chinese fantasy will show systematically different conceptual associations than the 
same words in original English fantasy, reflecting source-language influence, genre conventions, or both.

---

## Research Question

**Do selected English words in translated Chinese fantasy fiction occupy different semantic neighborhoods than the same words 
in original English fantasy fiction?**

---

## Corpora

**Corpus A — Translated Chinese Fiction**
Chinese-origin webnovels translated into English, drawn from the xianxia and xuanhuan genres. Likely source: WuxiaWorld and
similar platforms, which offer large volumes of freely available translated text. These genres are ideal because they are dense
with culturally-loaded vocabulary — cosmic hierarchy, sworn brotherhood, fate, spiritual cultivation — making source-language 
influence especially plausible to observe.
* Lord of the Mysteries
* Reverend Insanity
* I Shall Seal the Heavens
* Way of Choices / Ze Tian Ji

**Corpus B — Original English Fiction**
Epic or high fantasy fiction originally written in English, matched approximately for genre conventions: high stakes, world-building,
martial themes, questions of fate and power. The goal is to isolate *cultural and linguistic origin* as the variable of interest,
controlling as much as possible for genre.
* Shadow Slave
* The Wandering Inn
* Jackal Among Snakes
* A Practical Guide to Evil

**Scope:** A focused subset of approximately 1-2M tokens per corpus. Sufficient to train stable embeddings and produce
a complete, presentable set of findings. Methodology is designed to scale.

---

## Target Words

Words chosen for their cultural weight — each carries distinct connotations in Chinese cosmological, social, or philosophical contexts
that may or may not survive translation intact:

| Word                  | Axis of interest                                 |
|-----------------------|--------------------------------------------------|
| `heaven`              | cosmic order vs. theological or physical sky     |
| `fate`                | cosmic, mandate of heaven vs. personal destiny   |
| `heart`               | emotional/spiritual core vs. physical organ      |
| `face`                | social status/shame vs. physical appearance      |
| `brother`             | chosen kinship vs. literal family relation       |
| `immortal and mortal` | literal human mortality vs ascension/immortality |
| `power`               | individual ascension vs institutional authority  |
| `pill`                | medicinal vs spiritual                           |





---

## Methodology

### Step 1 — Corpus Collection and Preprocessing
Collect and clean both corpora: tokenize, lowercase, remove formatting artifacts. No domain-specific stop list.

### Step 2 — Word2Vec Training
Train separate word2vec models on each corpus from scratch using standard hyperparameters.
The axis comparison method is robust to the non-comparability of independently trained vectors, since it compares 
*relative distances within each model* rather than absolute coordinates across models. Both corpora share the same target 
and anchor words, which serve as internal reference points.

### Step 3 — Top-k Neighbor Comparison (Supplementary)
For each target word, extract the top-k nearest neighbors in each model and compare across corpora.

Measures:
- Degree of overlap between neighbor lists
- Words appearing only in one corpus's neighborhood
- Whether corpus-specific neighbors cluster into a meaningful semantic domain

This supplementary analysis helps identify corpus-specific neighbors that can then be interpreted qualitatively. 

### Step 4 — Conceptual Axis Comparison (Primary)
For each target word, define two conceptual poles using hand-selected anchor words grounded in the cultural hypothesis. Measure cosine 
distance from the target word to each pole, and compare the resulting orientation across corpora.

**How it works:**
For each pole, compute the average cosine similarity between the target word and each anchor word in that pole. The difference in
pole-scores across corpora quantifies the semantic shift as axis score difference.

**Example: `heart`**
- Body pole: `body`, `blood`, `flesh`, `chest`, `organ`
- Spirit pole: `spirit`, `soul`, `mind`, `emotion`, `love`
- Prediction: In Corpus A, *heart* leans toward the spirit pole. In Corpus B, *heart* leans toward the body pole.

**Example: `heaven`**
- Cosmic pole: `divine`, `immortal`, `celestial`, `transcendent`, `mandate`
- Mundane pole: `sky`, `god`, `afterlife`, `above`, `prayer`
- Prediction: In Corpus A, *heaven* leans cosmic. In Corpus B, *heaven* leans mundane or theological.

**Example: `face`**
- Social pole: `shame`, `honor`, `status`, `reputation`, `dignity`
- Physical pole: `eyes`, `smile`, `expression`, `appearance`, `look`
- Prediction: In Corpus A, *face* leans social. In Corpus B, *face* leans physical.

Anchor word selection is documented and justified for each axis. Sensitivity testing, substituting alternate anchors, included
as a robustness check.

---

## Expected Contributions

1. **A case-study framework** for comparing conceptual neighborhoods in translated and non-translated English fiction to detect
cultural fingerprints using axis-based embedding analysis.
2. **Exploratory evidence for the cultural bleed-through hypothesis** — cultural context measurably shapes the semantic 
neighborhoods of translated words, even after full translation into English
3. **A humanistic interpretation of geometric findings** — *this is what it looks like when tiān becomes "heaven" and brings 
its cosmology with it*

---

## Limitations

- **Genre confound:** Observed differences may reflect xianxia genre conventions rather than translation effects alone; 
acknowledged throughout, and a motivating reason to expand the corpus in future work
- **Translator effects:** Individual translators make distinct lexical choices that may shape neighborhoods independently
of source-language influence
- **Small-corpus instability:** Embedding neighborhoods can be unstable in smaller datasets; findings are treated as suggestive 
rather than conclusive
- **Anchor word subjectivity:** Hand-selected axes/anchors introduce researcher judgment, partially mitigated through 
documentation and sensitivity checks
---

## Roadmap

**Phase 1 — This Semester**
Corpus collection and cleaning, word2vec training, full axis analysis across all target words, qualitative neighbor analysis 
for selected words, written report and presentation(?).

**Phase 2 — Post-Semester (Tenative)**
Expand corpus size; add machine-translated Chinese fiction as a third condition to isolate translation method as a variable;
explore vector space alignment methods for more direct cross-model comparison; consider submission to a venue such as the 
ACL Student Research Workshop.
** submit to OUR journal? oregon undergrad research


## Notes
**Data collection, cleaning, preprocessing**
1. Find texts in epub format
2. Convert epubs to txt
3. Manual review: add to stopwords list, skip line list, etc.
4. Clean:
   * Remove headers, watermarks, maps, book titles, translator notes texts, etc.
   * Fix contractions, suffixes, exclamations
5. Lemmatize
   * Manually replace words that aren't picked up by lemmatizer (i.e. bro -> brother)
6. Find minimum tokens count, cut all texts at that minimum
7. Concatenate together all four samples

**Model Training**

Parameters:
* Vector Size: 100
* Window: 100
* Minimum Count: 10
* Epochs: 20
* Skip-Gram
* Negative: 5
* Sample: 1e-3

**Model Assessment**
* 

**Analysis**

**Misc notes**
* originally had energy as a focus word
