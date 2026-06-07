import streamlit as st

st.set_page_config(
    page_title="Hyperliquid Sentiment Analysis",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Hyperliquid Trader Sentiment Analysis")
st.subheader("Crypto Trade Intelligence Dashboard — Primetrade.ai")

st.markdown("""
Analysis of 35,000+ crypto trades with sentiment data
to identify risk zones and optimize trading strategy.

### Key Findings
- 📉 Highest losses occurred during **Extreme Fear** periods
- ⚠️ Risk-zone dashboard built for trade monitoring
- 📊 Recommended **40% leverage reduction** strategy
- 🔍 Sentiment-based trade pattern analysis
""")

st.info("35,000+ trades analyzed · Built for Primetrade.ai")
