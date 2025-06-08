# 📈 Market Pulse AI

Market Pulse AI is a real-time financial insight engine that combines stock feature engineering with AI-powered news summarization and sentiment analysis — all accessible via an interactive Streamlit dashboard.

---

## 🚀 Features

### 🔍 Stock Data & Financial Features
- Pulls historical stock data (mock or live)
- Computes key indicators like:
  - Daily returns
  - Volatility
  - Momentum
  - Moving averages
  - RSI

### 📰 News Sentiment Analysis
- Fetches recent news headlines via Yahoo Finance RSS
- Uses Hugging Face's **BART** model to summarize news
- Applies **FinBERT** for sentiment classification
- Displays results in a clean, readable format

### 📊 Market Pulse Score
- Calculates a weighted composite sentiment score across the latest news
- Gives users a quick "market mood" snapshot


---

## 🛠 Tech Stack

| Layer        | Tool/Library                  |
|--------------|-------------------------------|
| Language     | Python 3.9+                   |
| Frontend     | Streamlit                     |
| AI Models    | Hugging Face Transformers     |
| PDF Export   | fpdf                          |
| Data Sources | Yahoo Finance RSS             |

---

## 📦 Installation

```bash
git clone https://github.com/your-username/market-pulse-ai.git
cd market-pulse-ai
pip install -r requirements.txt
streamlit run app.py
