# app.py
import streamlit as st
import pandas as pd
from data_loader import generate_mock_data
from feature_extraction import compute_features
from news_pipeline import fetch_rss_news, process_news

# --- UI Layout ---
st.set_page_config(page_title="Market Pulse AI", layout="wide")
st.title("📈 Market Pulse AI")

# --- Sidebar Inputs ---
st.sidebar.header("Configuration")
ticker = st.sidebar.text_input("Ticker Symbol", value="AAPL")
days = st.sidebar.slider("Days of Data", min_value=30, max_value=180, value=60)

# --- Load & Feature Extract ---
st.subheader(f"Stock Data & Features for {ticker}")
data = generate_mock_data(ticker, days)
features = compute_features(data)
st.line_chart(features.set_index("Date")["Close"], height=200)
st.dataframe(features.tail(10))

# --- News Sentiment ---
st.subheader("📰 News Sentiment Analysis")

pulse_score = None
with st.spinner("Fetching and analyzing news..."):
    headlines = fetch_rss_news(ticker)
    if headlines:
        news_output = process_news(headlines[:5])  # Limit to 5 articles

        total_confidence = 0
        net_sentiment = 0

        for item in news_output:
            st.markdown(f"**Headline:** {item['original']}")
            st.markdown(f"_Summary_: {item['summary']}")
            st.markdown(f"**Sentiment**: {item['sentiment']} ({item['confidence'] * 100:.1f}% confidence)")
            st.markdown("---")

            # Sentiment scoring
            sentiment_weight = {"POSITIVE": 1, "NEUTRAL": 0, "NEGATIVE": -1}
            label = item['sentiment'].upper()
            score = sentiment_weight.get(label, 0)
            net_sentiment += score * item['confidence']
            total_confidence += item['confidence']

        # Compute composite score
        if total_confidence > 0:
            pulse_score = net_sentiment / total_confidence
            st.metric("📊 Market Pulse Score", f"{pulse_score:.2f}", help="Weighted sentiment across recent news")
    else:
        st.info("No news articles found or feed is currently unavailable.")
