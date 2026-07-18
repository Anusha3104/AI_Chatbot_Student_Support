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

## Project Structure

```
AI-Chatbot-Student-Support/
│
├── notebook/
│   └── AI_Chatbot_Student_Support.ipynb   # Main chatbot notebook
│
├── dataset/
│   ├── make_dataset.py                     # Script that generates the CSV dataset
│   └── student_queries.csv                 # 120 Q&A pairs (knowledge base)
│
├── logs/
│   └── chat_log.csv                        # Auto-generated conversation log
│
├── docs/
│   ├── Project_Report.docx                 # Full project report
│   ├── Presentation.pptx                   # PowerPoint presentation
│   └── Viva_Questions.md                   # Viva Q&A preparation
│
├── images/
│   ├── flowchart.png                       # Chatbot working flowchart
│   ├── architecture.png                    # System architecture diagram
│   └── screenshot_*.png                    # Notebook run screenshots
│
├── requirements.txt
└── README.md
```

## Getting Started

### 1. Clone / download this repository

```bash
git clone <your-repo-url>
cd AI-Chatbot-Student-Support
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Launch Jupyter Notebook

```bash
jupyter notebook
```

Open `notebook/AI_Chatbot_Student_Support.ipynb`, make sure `student_queries.csv` is in the same folder as the notebook (or update `DATA_PATH`), then **Run All Cells**.

### 4. Chat with the bot

In the "The Chatbot Loop" section, uncomment and run:

```python
run_chatbot()
```

Type your question and press Enter. Type `exit` to end the conversation.

## Example Conversation

```
You: hi
Bot: Hello! I am your Student Support Assistant. How can I help you today?

You: How can I apply for admission?
Bot: You can apply online through the official college admission portal by filling
     the application form and uploading the required documents.
     (confidence: 0.83)

You: what is the library timing
Bot: The library is open from 8:00 AM to 8:00 PM on all working days and 9:00 AM
     to 5:00 PM on Saturdays.
     (confidence: 1.00)

You: bye
Bot: Thank you for using the Student Support Chatbot. Goodbye! Have a great day.
```

## Algorithms Used

- **TF-IDF (Term Frequency–Inverse Document Frequency)** — converts text into weighted numeric vectors.
- **Cosine Similarity** — measures the angle between two vectors to score how similar two sentences are.
- **Difflib close-match (Ratcliff/Obershelp algorithm)** — lightweight offline spelling correction.

## Limitations

- Cannot understand queries far outside its trained dataset (returns a fallback message).
- Matching quality depends on the size and diversity of the CSV dataset.
- No deep contextual/conversation memory across turns (each question is handled independently).

## Future Scope

- Expand the dataset with more institution-specific FAQs.
- Add a simple web front-end (Flask/Streamlit) instead of the notebook `input()` loop.
- Integrate a small offline intent-classification model for better multi-turn context.
- Add multilingual support (Hindi + regional languages) for wider accessibility.
- Voice input/output using offline speech libraries.

## Author

B.Tech Minor Project — AI Chatbot for Student Support Services.

## License

This project is created for academic purposes and may be freely used/modified for learning.
