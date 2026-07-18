# AI Chatbot for Student Support Services

A beginner-friendly, **offline** AI chatbot built in Python (Jupyter Notebook) that answers common student queries related to Admissions, Fees, Hostel, Library, Examination, Placements, Scholarships, Faculty, Academic Calendar, College Timings, and general Student Support.

Built as a B.Tech minor project. No paid APIs, no internet connection, and no external AI services are used — the chatbot works entirely offline using classic Natural Language Processing (NLP) techniques.

## How It Works

1. A CSV knowledge base (`student_queries.csv`) stores 120 question–answer pairs across 11 categories.
2. User input and dataset questions are cleaned (lowercased, punctuation removed, stopwords removed).
3. Both are converted into numeric vectors using **TF-IDF (Term Frequency–Inverse Document Frequency)**.
4. **Cosine Similarity** is used to find the dataset question closest in meaning to the user's input.
5. The corresponding answer is returned along with a confidence score.
6. If no question is similar enough (score below threshold), the bot returns a fallback message directing the student to the Student Support Office.

## Features

- Rule-based, fully offline NLP chatbot (TF-IDF + Cosine Similarity)
- Greeting and farewell detection ("hi", "bye", "exit", etc.)
- Confidence score shown with every answer
- Basic spelling-mistake tolerance using `difflib` close-word matching
- All conversations logged with timestamps to `chat_log.csv`
- Clean, modular, well-commented code — beginner-friendly

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3 |
| IDE | Jupyter Notebook |
| Data handling | pandas, numpy |
| NLP | nltk (stopwords) |
| Vectorization & similarity | scikit-learn (TfidfVectorizer, cosine_similarity) |
| Dataset | CSV file |


