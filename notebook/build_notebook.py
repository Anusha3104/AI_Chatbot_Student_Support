import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []

def md(text):
    cells.append(nbf.v4.new_markdown_cell(text))

def code(text):
    cells.append(nbf.v4.new_code_cell(text))

# ------------------------------------------------------------------
md("""# AI Chatbot for Student Support Services

**A Minor Project (B.Tech)**

This notebook builds a rule-based, offline **NLP chatbot** that answers common student
questions (Admissions, Fees, Hostel, Library, Examination, Placements, Scholarships,
Faculty, Academic Calendar, College Timings, and general Student Support).

**Approach used:** TF-IDF (Term Frequency – Inverse Document Frequency) vectorization +
Cosine Similarity to find the most similar question in our dataset to the user's input,
and return its stored answer. No paid APIs or internet connection are required.

---
### Table of Contents
1. Import Libraries
2. Download NLTK Resources
3. Load the Dataset
4. Text Preprocessing
5. TF-IDF Vectorization
6. Similarity Matching Function
7. Greeting / Farewell Detection
8. Query Logging
9. The Chatbot Loop
10. Testing the Chatbot
""")

# ------------------------------------------------------------------
md("""## 1. Import Libraries

We use:
- **pandas** – to load and handle the CSV dataset
- **numpy** – for numerical operations
- **nltk** – for stopword removal and text tokenization
- **scikit-learn (sklearn)** – for TF-IDF vectorization and cosine similarity
- **re, string** – for cleaning text (removing punctuation, extra spaces)
- **datetime, csv, os** – for logging user queries with timestamps
""")

code("""# Core data-handling libraries
import pandas as pd
import numpy as np

# Text-cleaning libraries
import re
import string

# NLP libraries
import nltk
from nltk.corpus import stopwords

# Machine Learning libraries (used purely for text similarity, NOT for training a model)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Utility libraries
import os
import csv
from datetime import datetime

print("All libraries imported successfully.")""")

# ------------------------------------------------------------------
md("""## 2. Download NLTK Resources

NLTK needs a small one-time download of the **stopwords** list (common words like
"is", "the", "a" that carry little meaning) and the **punkt** tokenizer (used to split
sentences into words). This only downloads once; later runs will skip it if already present.
""")

code("""# Download required NLTK data (only downloads if not already present)
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

# Load English stopwords into a set for fast lookup
STOPWORDS = set(stopwords.words('english'))
print("Number of English stopwords loaded:", len(STOPWORDS))""")

# ------------------------------------------------------------------
md("""## 3. Load the Dataset

The knowledge base is stored in `student_queries.csv`, which contains three columns:

| category | question | answer |
|---|---|---|

This file has 120 rows covering 11 categories of student queries plus common greetings.
""")

code("""# Load the dataset
DATA_PATH = "student_queries.csv"   # place this file in the same folder as the notebook
df = pd.read_csv(DATA_PATH)

print("Dataset shape:", df.shape)
print("Categories covered:", df['category'].unique())
df.head(10)""")

# ------------------------------------------------------------------
md("""## 4. Text Preprocessing

Before comparing texts, we normalize them so that small differences (capitalisation,
punctuation, common filler words) don't affect matching. Our `preprocess_text()`
function performs 3 steps:

1. **Lowercasing** – "Hostel" and "hostel" should be treated the same.
2. **Removing punctuation** – "fees?" becomes "fees".
3. **Removing stopwords** – words like "is", "the", "a" are dropped because they do
   not help distinguish one question from another.

We apply this function to every question in the dataset once, and later apply the
same function to every new user input.
""")

code("""def preprocess_text(text: str) -> str:
    \"\"\"
    Cleans and normalizes input text for NLP processing.
    Steps: lowercase -> remove punctuation -> remove stopwords.
    \"\"\"
    # 1. Convert to lowercase
    text = text.lower()

    # 2. Remove punctuation using str.translate (fast and clean)
    text = text.translate(str.maketrans('', '', string.punctuation))

    # 3. Remove extra whitespace
    text = re.sub(r'\\s+', ' ', text).strip()

    # 4. Tokenize (split into words) and remove stopwords
    words = text.split()
    filtered_words = [word for word in words if word not in STOPWORDS]

    return ' '.join(filtered_words)


# Quick test of the preprocessing function
sample = "What is the LAST date for Admission?"
print("Original :", sample)
print("Processed:", preprocess_text(sample))""")

code("""# Apply preprocessing to every question in the dataset and store it in a new column
df['processed_question'] = df['question'].apply(preprocess_text)
df[['question', 'processed_question']].head(10)""")

# ------------------------------------------------------------------
md("""## 5. TF-IDF Vectorization

**TF-IDF (Term Frequency - Inverse Document Frequency)** converts text into numeric
vectors so that similarity can be computed mathematically.

- **Term Frequency (TF)**: how often a word appears in a sentence.
- **Inverse Document Frequency (IDF)**: gives less weight to words that appear in
  many questions (common words) and more weight to rare, distinguishing words.

We fit a single `TfidfVectorizer` on **all** preprocessed questions in our dataset.
This vectorizer will later be reused (not re-fitted) to transform the user's live input,
so that both are represented in the same vector space and can be compared.
""")

code("""# Create and fit the TF-IDF vectorizer on the dataset's processed questions
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df['processed_question'])

print("TF-IDF matrix shape:", tfidf_matrix.shape)
print("(rows = number of questions, columns = number of unique vocabulary words)")""")

# ------------------------------------------------------------------
md("""## 6. Similarity Matching Function

To find the best answer for a user's question, we:

1. Preprocess the user's input the same way as the dataset.
2. Transform it into a TF-IDF vector using the **same** vectorizer (`transform`, not `fit_transform`).
3. Compute **Cosine Similarity** between the user's vector and every question vector in the dataset.
4. Pick the row with the **highest similarity score**.
5. If the highest score is below a threshold (meaning nothing in our dataset is a close
   match), we return the fallback message instead of a wrong answer.

**Cosine Similarity** measures the angle between two vectors — the smaller the angle
(closer to 1.0), the more similar the sentences are, regardless of sentence length.
""")

code("""# Minimum similarity score required to trust a match (tune this for spelling-mistake tolerance)
SIMILARITY_THRESHOLD = 0.30

FALLBACK_MESSAGE = "Sorry, I couldn't find an answer. Please contact the Student Support Office."


def get_best_match(user_input: str):
    \"\"\"
    Given a raw user input string, returns (answer, confidence_score, matched_question).
    If no good match is found, returns the fallback message with score 0.
    \"\"\"
    # Step 1: preprocess the user's input exactly like the dataset questions
    processed_input = preprocess_text(user_input)

    # Guard against empty input after cleaning (e.g. user typed only punctuation)
    if processed_input.strip() == "":
        return FALLBACK_MESSAGE, 0.0, None

    # Step 2: convert user input into the SAME TF-IDF vector space as the dataset
    user_vector = vectorizer.transform([processed_input])

    # Step 3: compute cosine similarity between user vector and every dataset question
    similarity_scores = cosine_similarity(user_vector, tfidf_matrix)

    # Step 4: find the index of the highest similarity score
    best_index = np.argmax(similarity_scores)
    best_score = similarity_scores[0, best_index]

    # Step 5: apply threshold check
    if best_score < SIMILARITY_THRESHOLD:
        return FALLBACK_MESSAGE, float(best_score), None

    matched_question = df.iloc[best_index]['question']
    answer = df.iloc[best_index]['answer']
    return answer, float(best_score), matched_question


# Quick test
answer, score, matched_q = get_best_match("wat is da last date 4 addmision")
print("Matched question :", matched_q)
print("Confidence score :", round(score, 3))
print("Answer           :", answer)""")

# ------------------------------------------------------------------
md("""### Note on handling spelling mistakes

TF-IDF + Cosine Similarity is naturally a little tolerant of minor typos when the
sentence has multiple words (because *some* words still match correctly), but it will
struggle with single heavily-misspelled keywords. As a lightweight, offline improvement,
we add a simple **word-level spelling correction** step using `difflib.get_close_matches`
(part of Python's standard library — no extra download needed) that snaps each input
word to the closest known vocabulary word before vectorizing.
""")

code("""import difflib

# Build a vocabulary list from all words seen in the dataset questions
VOCAB = set()
for q in df['processed_question']:
    VOCAB.update(q.split())
VOCAB = list(VOCAB)


def correct_spelling(text: str) -> str:
    \"\"\"
    Attempts to correct minor spelling mistakes by matching each word
    to the closest word in our known vocabulary (difflib uses the
    Ratcliff-Obershelp algorithm to measure string similarity).
    \"\"\"
    corrected_words = []
    for word in text.split():
        matches = difflib.get_close_matches(word, VOCAB, n=1, cutoff=0.8)
        corrected_words.append(matches[0] if matches else word)
    return ' '.join(corrected_words)


# Update get_best_match to use spelling correction before vectorizing
def get_best_match(user_input: str):
    processed_input = preprocess_text(user_input)
    if processed_input.strip() == "":
        return FALLBACK_MESSAGE, 0.0, None

    # Apply spelling correction on top of normal preprocessing
    processed_input = correct_spelling(processed_input)

    user_vector = vectorizer.transform([processed_input])
    similarity_scores = cosine_similarity(user_vector, tfidf_matrix)

    best_index = np.argmax(similarity_scores)
    best_score = similarity_scores[0, best_index]

    if best_score < SIMILARITY_THRESHOLD:
        return FALLBACK_MESSAGE, float(best_score), None

    matched_question = df.iloc[best_index]['question']
    answer = df.iloc[best_index]['answer']
    return answer, float(best_score), matched_question


# Re-test with spelling correction enabled
answer, score, matched_q = get_best_match("libary timmings")
print("Matched question :", matched_q)
print("Confidence score :", round(score, 3))
print("Answer           :", answer)""")

# ------------------------------------------------------------------
md("""## 7. Greeting and Farewell Detection

We keep a small list of common greeting/farewell keywords so the bot can respond
naturally to "hi", "hello", "bye", etc. without relying purely on the CSV match
(although our dataset also includes greeting rows as a backup).
""")

code("""GREETING_INPUTS = ("hi", "hello", "hey", "good morning", "good afternoon", "good evening")
GREETING_RESPONSE = "Hello! I am your Student Support Assistant. How can I help you today?"

FAREWELL_INPUTS = ("bye", "goodbye", "exit", "quit", "see you")
FAREWELL_RESPONSE = "Thank you for using the Student Support Chatbot. Goodbye! Have a great day."


def is_greeting(text: str) -> bool:
    text = text.lower().strip()
    return any(text == g or text.startswith(g) for g in GREETING_INPUTS)


def is_farewell(text: str) -> bool:
    text = text.lower().strip()
    return any(text == f for f in FAREWELL_INPUTS)

print("Greeting/Farewell detection functions ready.")""")

# ------------------------------------------------------------------
md("""## 8. Query Logging

Every question a user asks (and the chatbot's response) is appended to
`chat_log.csv` with a timestamp. This is useful for the Student Support Office to
review what students are asking about most, and to identify questions the chatbot
could not answer (so the dataset can be improved later).
""")

code("""LOG_PATH = "chat_log.csv"

def log_interaction(user_input: str, bot_response: str, score: float):
    \"\"\"Appends one row (timestamp, user_input, bot_response, confidence) to the log file.\"\"\"
    file_exists = os.path.isfile(LOG_PATH)
    with open(LOG_PATH, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "user_input", "bot_response", "confidence_score"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_input, bot_response, round(score, 3)])

print("Logging function ready. Logs will be saved to:", LOG_PATH)""")

# ------------------------------------------------------------------
md("""## 9. The Chatbot Loop

This is the main driver function. It:

1. Prints a welcome message.
2. Repeatedly reads user input.
3. Checks for farewell -> ends conversation.
4. Checks for greeting -> responds with a greeting.
5. Otherwise -> uses `get_best_match()` to find and print the best answer with its
   confidence score.
6. Logs every interaction to `chat_log.csv`.

> **Note:** `input()` works interactively when you run this cell in Jupyter. If you are
> reading this notebook as a static document, see Section 10 for a scripted demo that
> does not require typing.
""")

code("""def run_chatbot():
    print("=" * 60)
    print(" AI CHATBOT FOR STUDENT SUPPORT SERVICES")
    print(" Type your question below. Type 'exit' to end the chat.")
    print("=" * 60)

    while True:
        user_input = input("You: ").strip()

        if user_input == "":
            print("Bot: Please type a question.")
            continue

        if is_farewell(user_input):
            print("Bot:", FAREWELL_RESPONSE)
            log_interaction(user_input, FAREWELL_RESPONSE, 1.0)
            break

        if is_greeting(user_input):
            print("Bot:", GREETING_RESPONSE)
            log_interaction(user_input, GREETING_RESPONSE, 1.0)
            continue

        answer, score, matched_q = get_best_match(user_input)
        print(f"Bot: {answer}")
        print(f"     (confidence: {score:.2f}" + (f", matched: '{matched_q}')" if matched_q else ")"))
        log_interaction(user_input, answer, score)


# Uncomment the line below to chat interactively inside Jupyter:
# run_chatbot()""")

# ------------------------------------------------------------------
md("""## 10. Testing the Chatbot (Scripted Demo)

Since interactive `input()` cannot be auto-run in every environment (e.g. when a
notebook is exported to a report), the cell below feeds a list of sample questions
through the same pipeline used by `run_chatbot()`, so you can see example
input/output pairs immediately.
""")

code("""test_questions = [
    "hi",
    "How can I apply for admission?",
    "wat is da libary timing",
    "when do placements start",
    "Can I get a scholarship for SC ST students?",
    "how is the weather today",   # out-of-scope question -> should trigger fallback
    "bye"
]

for q in test_questions:
    if is_farewell(q):
        print(f"You: {q}\\nBot: {FAREWELL_RESPONSE}\\n")
        log_interaction(q, FAREWELL_RESPONSE, 1.0)
        continue
    if is_greeting(q):
        print(f"You: {q}\\nBot: {GREETING_RESPONSE}\\n")
        log_interaction(q, GREETING_RESPONSE, 1.0)
        continue
    answer, score, matched_q = get_best_match(q)
    print(f"You: {q}")
    print(f"Bot: {answer}")
    print(f"     (confidence: {score:.2f})\\n")
    log_interaction(q, answer, score)""")

code("""# View the logged conversation history
log_df = pd.read_csv(LOG_PATH)
log_df""")

md("""## Conclusion

This notebook implements a complete, offline, rule-based NLP chatbot for student
support services using **TF-IDF vectorization** and **Cosine Similarity** matching,
with added spelling-correction, greeting/farewell handling, and query logging.

To use it yourself: place `student_queries.csv` in the same folder as this notebook,
run all cells in order, and call `run_chatbot()` in Section 9 for an interactive chat
session inside Jupyter.
""")

nb['cells'] = cells

with open("AI_Chatbot_Student_Support.ipynb", "w") as f:
    nbf.write(nb, f)

print("Notebook created successfully.")
