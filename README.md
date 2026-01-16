# 📧 AI Cold Email Generator

An AI-powered Cold Email Generator that automatically creates **personalized, professional cold emails** by analyzing job descriptions from URLs and matching them with a user’s portfolio.

This project is designed to help **XYZ Company** to quickly refer candidate with high-quality outreach emails tailored to specific roles or companies.

---

## 🚀 Features

* 🔗 **Job URL Parsing** – Extracts role details directly from job posting links
* 🤖 **LLM-Powered Email Generation** – Uses an LLM to write structured, professional cold emails
* 🧠 **Portfolio Matching** – Aligns skills and projects from a CSV-based portfolio
* 🧹 **Text Cleaning & Preprocessing** – Removes noise from scraped job descriptions
* 🖥️ **Streamlit Web App** – Simple UI for fast interaction

---

## 🛠️ Tech Stack

* **Python 3.10+**
* **Streamlit** – Web interface
* **LangChain** – LLM orchestration
* **LLM API (GROQ)** – Email generation
* **WebBaseLoader** – Job description scraping
* **Pandas** – Portfolio handling (CSV)

---

## 📂 Project Structure

```
Email_Generator/
│
├── app/
|   ├── main.py                # Streamlit app entry point
│   ├── chains.py              # LLM prompt & chain logic
│   ├── portfolio.py           # Portfolio loading & matching
│   ├── utils.py               # Text cleaning utilities
│   └── resource/
│       └── my_portfolio.csv   # Portfolio data
│
├── Email_generator.ipynb      # Experimentation notebook
├── Chromadb.ipynb             # Vector DB experiments
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/Taniyachouhaniitm/Email_Generator.git
cd Email_Generator
```

### 2️⃣ Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Set API Keys

Create a `.env` file or set environment variables:

```bash
GROQ_API_KEY=your_api_key_here
```

---

## ▶️ Running the App

```bash
streamlit run .\app\main.py
```

Then open the browser URL shown in the terminal.

---

## 🧪 How It Works

1. User pastes a **job posting URL**
2. App scrapes and cleans the job description
3. Portfolio are loaded from CSV
4. LLM generates a **custom cold email** following a professional structure
5. Email is displayed and ready to send

---


## 👩‍💻 Author

**Taniya Chouhan**
B.S. Data Science, IIT Madras
Aspiring Data Scientist / Product & AI Engineer

GitHub: [https://github.com/Taniyachouhaniitm](https://github.com/Taniyachouhaniitm)

---

## ⭐ If you like this project

Give it a star ⭐ and feel free to fork or contribute!

