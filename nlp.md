NLP Lab Examination — Complete Study Guide
For each topic: Concept (viva) → Code (to write on paper) → Expected Output

All code uses Python + NLTK (and scikit-learn / spaCy where noted). Assume these run once at the top of your script/session:

import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('omw-1.4')
1. Tokenization and Sentence Segmentation
Concept: Tokenization splits raw text into smaller units (tokens) — words or sentences. NLTK's word_tokenize uses the Punkt algorithm, a pre-trained unsupervised model that detects sentence/word boundaries using punctuation and abbreviation rules, not just whitespace splitting (so "Mr." isn't split at the period).

Code:

from nltk.tokenize import word_tokenize, sent_tokenize

text = "Natural Language Processing is fascinating. It enables machines to understand human language."

sentences = sent_tokenize(text)
words = word_tokenize(text)

print("Sentences:", sentences)
print("Words:", words)
Output:

Sentences: ['Natural Language Processing is fascinating.', 'It enables machines to understand human language.']
Words: ['Natural', 'Language', 'Processing', 'is', 'fascinating', '.', 'It', 'enables', 'machines', 'to', 'understand', 'human', 'language', '.']
2. Text Pre-processing: Stop Word Removal, Stemming, Lemmatization
Concept: Stop words (the, is, and…) carry little meaning and are removed to reduce noise. Stemming chops word endings using fixed rules (Porter algorithm) — fast but crude, may produce non-words ("runn"). Lemmatization uses vocabulary + POS to return the dictionary root ("run") — slower but linguistically correct.

Code:

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer

text = "The runners were running rapidly towards the finishing line"
words = word_tokenize(text)

stop_words = set(stopwords.words('english'))
filtered = [w for w in words if w.lower() not in stop_words]

stemmer = PorterStemmer()
stemmed = [stemmer.stem(w) for w in filtered]

lemmatizer = WordNetLemmatizer()
lemmatized = [lemmatizer.lemmatize(w, pos='v') for w in filtered]

print("Filtered:", filtered)
print("Stemmed:", stemmed)
print("Lemmatized:", lemmatized)
Output:

Filtered: ['runners', 'running', 'rapidly', 'towards', 'finishing', 'line']
Stemmed: ['runner', 'run', 'rapidli', 'toward', 'finish', 'line']
Lemmatized: ['runner', 'run', 'rapidly', 'towards', 'finish', 'line']
3. Regex-based Extraction (Emails, Phones, Dates, URLs, Hashtags)
Concept: Regular expressions define search patterns to pull structured entities out of unstructured text — useful as a fast, rule-based alternative to full NLP pipelines for well-formatted data.

Code:

import re

text = """Contact us at info@marian.edu or call 9876543210.
Visit https://www.marian.edu on 25/09/2026. #NLP #AI"""

emails = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', text)
phones = re.findall(r'\b\d{10}\b', text)
dates = re.findall(r'\b\d{2}/\d{2}/\d{4}\b', text)
urls = re.findall(r'https?://\S+', text)
hashtags = re.findall(r'#\w+', text)

print("Emails:", emails)
print("Phones:", phones)
print("Dates:", dates)
print("URLs:", urls)
print("Hashtags:", hashtags)
Output:

Emails: ['info@marian.edu']
Phones: ['9876543210']
Dates: ['25/09/2026']
URLs: ['https://www.marian.edu']
Hashtags: ['#NLP', '#AI']
4. Corpus Loading and Corpus Statistics using NLTK
Concept: A corpus is a large structured collection of text (e.g., Gutenberg books). NLTK provides ready-made corpora and tools (FreqDist) to compute statistics like word counts, vocabulary size, and lexical diversity (unique words / total words).

Code:

import nltk
nltk.download('gutenberg')
from nltk.corpus import gutenberg
from nltk import FreqDist

file_id = 'austen-emma.txt'
words = gutenberg.words(file_id)

print("Total words:", len(words))
print("Unique words:", len(set(words)))
print("Lexical diversity:", len(set(words)) / len(words))

fdist = FreqDist(words)
print("Most common 5 words:", fdist.most_common(5))
Output (approximate — real numbers on your machine):

Total words: 192427
Unique words: 7811
Lexical diversity: 0.0406
Most common 5 words: [(',', 11454), ('.', 6928), ('to', 5183), ('the', 4844), ('and', 4672)]
5. WordNet Exploration — Synonyms, Antonyms, Hypernyms, Hyponyms
Concept: WordNet is a lexical database organizing words into "synsets" (sets of synonymous meanings) linked by semantic relations: hypernym (is-a, more general), hyponym (is-a, more specific), antonym (opposite), meronym/holonym (part-whole).

Code:

from nltk.corpus import wordnet as wn

synsets = wn.synsets("good")
syn = synsets[0]
print("Synset:", syn.name(), "-", syn.definition())

synonyms, antonyms = [], []
for s in wn.synsets("good"):
    for lemma in s.lemmas():
        synonyms.append(lemma.name())
        if lemma.antonyms():
            antonyms.append(lemma.antonyms()[0].name())

print("Synonyms:", set(synonyms))
print("Antonyms:", set(antonyms))
print("Hypernyms:", syn.hypernyms())
print("Hyponyms:", syn.hyponyms())
Output (abridged):

Synset: good.n.01 - benefit
Synonyms: {'good', 'well', 'ripe', 'skillful', 'unspoiled', ...}
Antonyms: {'bad', 'evil', 'evilness', 'ill'}
Hypernyms: [Synset('advantage.n.01')]
Hyponyms: [Synset('common_good.n.01'), Synset('gain.n.02'), ...]
6. Bag-of-Words and TF-IDF Representation
Concept: BoW represents each document as a vector of raw word counts, ignoring order. TF-IDF (Term Frequency–Inverse Document Frequency) reweights counts: it boosts words frequent in one document but rare across the corpus, and downweights common words — highlighting terms that best distinguish a document.

Code:

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

docs = ["I love natural language processing",
        "Language processing is a subfield of AI",
        "I love AI"]

cv = CountVectorizer()
bow = cv.fit_transform(docs)
print("BoW vocabulary:", cv.get_feature_names_out())
print("BoW matrix:\n", bow.toarray())

tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(docs)
print("TF-IDF matrix:\n", tfidf_matrix.toarray().round(2))
Output (abridged):

BoW vocabulary: ['ai' 'is' 'language' 'love' 'natural' 'of' 'processing' 'subfield']
BoW matrix:
 [[0 0 1 1 1 0 1 0]
  [1 1 1 0 0 1 1 1]
  [1 0 0 1 0 0 0 0]]
TF-IDF matrix:
 [[0.   0.   0.42 0.55 0.55 0.   0.42 0.  ]
  [0.36 0.46 0.35 0.   0.   0.46 0.35 0.46]
  [0.6  0.   0.   0.8  0.   0.   0.   0.  ]]
7. N-gram Generation and Frequency Analysis
Concept: An n-gram is a contiguous sequence of n tokens. Bigrams (n=2) and trigrams (n=3) capture local word order and are used in language modeling, autocomplete, and collocation detection.

Code:

from nltk import ngrams, FreqDist
from nltk.tokenize import word_tokenize

text = "the quick brown fox jumps over the lazy dog"
tokens = word_tokenize(text)

bigrams = list(ngrams(tokens, 2))
trigrams = list(ngrams(tokens, 3))

print("Bigrams:", bigrams)
print("Trigrams:", trigrams)

fdist = FreqDist(bigrams)
print("Bigram frequencies:", fdist.most_common(3))
Output:

Bigrams: [('the', 'quick'), ('quick', 'brown'), ('brown', 'fox'), ('fox', 'jumps'), ('jumps', 'over'), ('over', 'the'), ('the', 'lazy'), ('lazy', 'dog')]
Trigrams: [('the', 'quick', 'brown'), ('quick', 'brown', 'fox'), ...]
Bigram frequencies: [(('the', 'quick'), 1), (('quick', 'brown'), 1), (('brown', 'fox'), 1)]
8. Word Frequency Visualization (Bar Chart / Word Cloud)
Concept: Visualizing word frequencies helps quickly spot dominant terms in a text. Bar charts show ranked counts; word clouds encode frequency as font size.

Code (bar chart):

import matplotlib.pyplot as plt
from nltk import FreqDist
from nltk.tokenize import word_tokenize

text = "data science data analysis data visualization python data"
tokens = word_tokenize(text)
fdist = FreqDist(tokens)

words, counts = zip(*fdist.most_common(5))
plt.bar(words, counts)
plt.xlabel("Words"); plt.ylabel("Frequency"); plt.title("Word Frequency")
plt.show()
Code (word cloud):

from wordcloud import WordCloud
import matplotlib.pyplot as plt

wc = WordCloud(width=600, height=400, background_color='white').generate(text)
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.show()
Output: A bar chart with "data" tallest (4), or a word cloud image with "data" rendered largest. (No text output — a plot window/image is displayed.)

9. Document and Sentence Similarity using Cosine Similarity
Concept: Cosine similarity measures the angle between two TF-IDF vectors, giving a score between 0 (unrelated) and 1 (identical direction/topic) — independent of document length.

Code:

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

doc1 = "Machine learning is a subset of artificial intelligence"
doc2 = "Artificial intelligence includes machine learning"
doc3 = "I love eating pizza"

docs = [doc1, doc2, doc3]
tfidf = TfidfVectorizer().fit_transform(docs)
similarity = cosine_similarity(tfidf[0:1], tfidf)

print("Similarity of doc1 with [doc1, doc2, doc3]:", similarity)
Output:

Similarity of doc1 with [doc1, doc2, doc3]: [[1.         0.68       0.        ]]
10. POS Tagging using NLP Libraries
Concept: Part-of-Speech tagging assigns a grammatical category (noun, verb, adjective…) to each token, based on context and word form, using a statistically trained tagger (Penn Treebank tagset in NLTK).

Code:

from nltk.tokenize import word_tokenize
from nltk import pos_tag

text = "The quick brown fox jumps over the lazy dog"
tokens = word_tokenize(text)
tags = pos_tag(tokens)
print(tags)
Output:

[('The', 'DT'), ('quick', 'JJ'), ('brown', 'NN'), ('fox', 'NN'), ('jumps', 'VBZ'), ('over', 'IN'), ('the', 'DT'), ('lazy', 'JJ'), ('dog', 'NN')]
11. Noun Phrase and Multiword Expression Extraction
Concept: A noun phrase groups a noun with its modifiers (e.g., "the quick brown fox"). It's extracted via chunking — applying a regex grammar over POS tags. Multiword expressions (MWEs, e.g., "New York") are fixed phrases treated as a single token using MWETokenizer.

Code:

from nltk import pos_tag, RegexpParser
from nltk.tokenize import word_tokenize, MWETokenizer

text = "The quick brown fox jumps over the lazy dog"
tags = pos_tag(word_tokenize(text))

grammar = "NP: {<DT>?<JJ>*<NN>}"
parser = RegexpParser(grammar)
tree = parser.parse(tags)
print(tree)

mwe = MWETokenizer([('New', 'York'), ('United', 'States')])
print(mwe.tokenize("I live in New York in the United States".split()))
Output:

(S
  (NP The/DT quick/JJ brown/NN)
  (NP fox/NN)
  jumps/VBZ
  over/IN
  (NP the/DT lazy/JJ dog/NN))
['I', 'live', 'in', 'New_York', 'in', 'the', 'United_States']
12. Handling Unknown Words in NLP Processing
Concept: Real text always contains words absent from the training vocabulary (OOV — out-of-vocabulary): typos, new terms, names. Common handling strategies: (1) map rare/unseen words to a special <UNK> token, (2) subword tokenization (BPE/WordPiece) to break unknown words into known sub-units, (3) smoothing techniques (Laplace/add-one) in probabilistic models so unseen n-grams don't get zero probability.

Code (UNK substitution based on a known vocabulary):

from nltk.tokenize import word_tokenize

vocab = {"the", "fox", "jumps", "over", "dog", "quick", "brown", "lazy"}
text = "the quick brown fox leapfrogs over the lazy dog"
tokens = word_tokenize(text)

processed = [w if w in vocab else "<UNK>" for w in tokens]
print(processed)
Output:

['the', 'quick', 'brown', 'fox', '<UNK>', 'over', 'the', 'lazy', 'dog']
13. Shallow Parsing and Chunking
Concept: Shallow parsing (chunking) identifies flat, non-recursive phrase structures (NP, VP chunks) from POS-tagged text without building a full parse tree — faster than deep syntactic parsing and sufficient for many information-extraction tasks.

Code:

from nltk import pos_tag, RegexpParser
from nltk.tokenize import word_tokenize

text = "He quickly finished his homework before dinner"
tags = pos_tag(word_tokenize(text))

grammar = r"""
  NP: {<DT>?<JJ>*<NN.*>}
  VP: {<VB.*><RB>?}
"""
parser = RegexpParser(grammar)
tree = parser.parse(tags)
print(tree)
Output:

(S
  He/PRP
  (VP quickly/RB)
  (VP finished/VBD)
  his/PRP$
  (NP homework/NN)
  before/IN
  (NP dinner/NN))
(Grammar/output shape may vary slightly by NLTK version's tagger.)

14. Dependency Parsing and Sentence Structure Analysis
Concept: Dependency parsing represents a sentence as a tree of binary head–dependent grammatical relations (subject, object, modifier) rather than phrase brackets — showing which word governs which. NLTK has no built-in trained dependency parser, so spaCy is standard for this.

Code:

import spacy
nlp = spacy.load("en_core_web_sm")

doc = nlp("The cat sat on the mat")
for token in doc:
    print(token.text, "->", token.dep_, "->", token.head.text)
Output:

The -> det -> cat
cat -> nsubj -> sat
sat -> ROOT -> sat
on -> prep -> sat
the -> det -> mat
mat -> pobj -> on
15. TreeBank Data Exploration using NLTK
Concept: The Penn Treebank corpus provides manually annotated parse trees for real sentences — used as gold-standard training/evaluation data for parsers and taggers.

Code:

import nltk
nltk.download('treebank')
from nltk.corpus import treebank

print("Number of parsed sentences:", len(treebank.parsed_sents()))
print(treebank.parsed_sents()[0])
print("Tagged words sample:", treebank.tagged_words()[:10])
Output (abridged):

Number of parsed sentences: 3914
(S
  (NP-SBJ (NNP Pierre) (NNP Vinken) ...)
  (VP (MD will) (VP (VB join) ...))
  (. .))
Tagged words sample: [('Pierre', 'NNP'), ('Vinken', 'NNP'), (',', ','), ('61', 'CD'), ...]
16. Sentence Meaning Representation (Logical Forms / Semantic Roles)
Concept: Semantic representation captures meaning rather than surface syntax — e.g., translating a sentence into First-Order Logic (predicate–argument structure), or labeling semantic roles (who did what to whom: Agent, Patient, Instrument). NLTK's nltk.sem module supports simple FOL construction and evaluation via feature-based grammars.

Code:

import nltk
from nltk import load_parser

grammar = nltk.data.load('grammars/book_grammars/sem2.fcfg')
parser = load_parser('grammars/book_grammars/sem2.fcfg', trace=0)

sentence = "Angus gives a bone to every dog".split()
for tree in parser.parse(sentence):
    print(tree.label()['SEM'])
Output (example logical form):

all z2.(dog(z2) -> give(angus, z2, bone))
(Exact output depends on the grammar file available in your NLTK data; explain the concept — mapping syntax to predicate logic — even if the exact grammar isn't installed.)

17. Lexical Semantic Analysis using WordNet Similarity
Concept: WordNet-based similarity measures quantify how semantically close two word senses are, using the structure of the WordNet hierarchy: path similarity (inverse of shortest path length between synsets), Wu-Palmer (based on depth of least common subsumer), Leacock-Chodorow (path length scaled by taxonomy depth).

Code:

from nltk.corpus import wordnet as wn

dog = wn.synset('dog.n.01')
cat = wn.synset('cat.n.01')

print("Path similarity:", dog.path_similarity(cat))
print("Wu-Palmer similarity:", dog.wup_similarity(cat))
print("Leacock-Chodorow similarity:", dog.lch_similarity(cat))
Output:

Path similarity: 0.2
Wu-Palmer similarity: 0.8571428571428571
Leacock-Chodorow similarity: 2.0281482472922856
18. Word Sense Disambiguation using the Lesk Algorithm
Concept: A single word often has multiple senses (e.g., "bank" = riverbank or financial institution). The Lesk algorithm disambiguates by comparing the dictionary definition (gloss) of each candidate sense against the words in the surrounding context, picking the sense with maximum word overlap.

Code:

from nltk.wsd import lesk
from nltk.tokenize import word_tokenize

sentence = "I went to the bank to deposit money"
tokens = word_tokenize(sentence)

sense = lesk(tokens, 'bank')
print("Best sense:", sense)
print("Definition:", sense.definition())
Output:

Best sense: Synset('depository_financial_institution.n.01')
Definition: a financial institution that accepts deposits and channels the money into lending activities
19. WordNet-based Meaning Disambiguation in Context
Concept: This applies the same gloss-overlap idea as Lesk, but manually: compare the context word set with each sense's gloss (and example sentences) word-by-word to choose the best-fitting synset — useful to show the step-by-step working behind Lesk rather than calling the built-in function.

Code:

from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize

def simple_lesk(word, sentence):
    context = set(word_tokenize(sentence.lower()))
    best_sense, max_overlap = None, 0
    for sense in wn.synsets(word):
        gloss_words = set(word_tokenize(sense.definition().lower()))
        overlap = len(gloss_words & context)
        if overlap > max_overlap:
            max_overlap, best_sense = overlap, sense
    return best_sense

result = simple_lesk("bank", "I went to the bank to deposit money")
print(result, "-", result.definition() if result else "No match")
Output:

Synset('depository_financial_institution.n.01') - a financial institution that accepts deposits and channels the money into lending activities
20. Text Coherence Analysis using Sentence Similarity
Concept: Coherence measures how well consecutive sentences in a text connect to each other semantically. One common method: vectorize each sentence (TF-IDF), compute cosine similarity between consecutive sentence pairs, and average — a higher average means smoother topical flow.

Code:

from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

text = """Machine learning is a branch of artificial intelligence.
It focuses on building systems that learn from data.
These systems improve their performance over time without explicit programming."""

sentences = sent_tokenize(text)
tfidf = TfidfVectorizer().fit_transform(sentences)

scores = []
for i in range(len(sentences) - 1):
    sim = cosine_similarity(tfidf[i], tfidf[i+1])[0][0]
    scores.append(sim)
    print(f"Similarity (sent {i+1} - sent {i+2}): {sim:.2f}")

print("Average coherence score:", sum(scores) / len(scores))
Output:

Similarity (sent 1 - sent 2): 0.14
Similarity (sent 2 - sent 3): 0.10
Average coherence score: 0.12
Exam-day tips
The examiner's note says explain the theory, not just recite code — for each topic, be ready to answer: what problem does this solve, and why this algorithm/library call specifically?
Common viva follow-ups to prepare for:
Why Punkt for tokenization, not .split()? (handles abbreviations, punctuation)
Stemming vs lemmatization — which is faster, which is more accurate, and why?
Why TF-IDF over raw BoW counts? (downweights common words, highlights distinctive terms)
What does cosine similarity ignore that Euclidean distance doesn't? (document length/magnitude)
Why does Lesk sometimes fail? (short glosses → low overlap → wrong sense picked)
Difference between shallow parsing and dependency parsing (flat chunks vs full head-dependent tree)
Numbers in "Output" sections (frequencies, similarity scores) will vary slightly with your exact input text/corpus version — the examiner cares about the shape and correctness of your output, not exact decimals.