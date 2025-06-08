# news_pipeline.py
from typing import List, Dict
from transformers.pipelines import pipeline
import feedparser

# Load actual Hugging Face models
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
sentiment_model = pipeline("text-classification", model="ProsusAI/finbert", return_all_scores=False)

def summarize(text: str) -> str:
    """
    Summarizes the input text using a transformer model.
    """
    if len(text.split()) < 30:
        return text
    summary = summarizer(text, max_length=60, min_length=20, do_sample=False)
    summary_text = summary[0]['summary_text'] if isinstance(summary, list) and 'summary_text' in summary[0] else str(summary)
    return str(summary_text)

def analyze_sentiment(text: str) -> Dict:
    """
    Performs sentiment analysis using FinBERT model.
    """
    model_output = sentiment_model(text)
    if model_output is None:
        return {"label": "NEUTRAL", "score": 0.0}
    results = list(model_output)
    if not results:
        return {"label": "NEUTRAL", "score": 0.0}
    from typing import Any
    result: Any = results[0]
    return {"label": result['label'], "score": round(result['score'], 2)}

def process_news(news_items: List[str]) -> List[Dict]:
    """
    Processes a list of news items: summarizes and assigns sentiment.
    """
    results = []
    for item in news_items:
        summary = summarize(item)
        sentiment = analyze_sentiment(summary)
        results.append({
            "original": item,
            "summary": summary,
            "sentiment": sentiment["label"],
            "confidence": sentiment["score"]
        })
    return results

def fetch_rss_news(ticker: str) -> List[str]:
    """
    Fetch news headlines for the given ticker from Yahoo Finance RSS.
    """
    url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US"
    feed = feedparser.parse(url)
    headlines = [entry.title for entry in feed.entries if hasattr(entry, "title") and isinstance(entry.title, str)]
    return headlines


if __name__ == "__main__":
    headlines = fetch_rss_news("AAPL")
    processed = process_news(headlines[:3])  # limit for quick demo
    for item in processed:
        print(item)
