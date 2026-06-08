import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. Page Setup ---
st.set_page_config(page_title="Trader Sentiment Dashboard", layout="wide")
st.title("📊 Hyperliquid Performance vs. Sentiment")

# --- 2. Robust Data Loading ---
@st.cache_data
def load_and_process_data():
    # Files load karna
    df_s = pd.read_csv('fear_greed_index.csv')
    df_t = pd.read_csv('historical_data.csv')
    
    # Column names cleaning
    df_s.columns = df_s.columns.str.strip().str.lower()
    df_t.columns = df_t.columns.str.strip().str.lower()
    
    # Dynamic Column Detection (Taaki 'account' error na aaye)
    # Hum dhoond rahe hain ki kaunsa column account/user hai
    acc_col = next((c for c in df_t.columns if 'account' in c or 'user' in c or 'address' in c), None)
    pnl_col = next((c for c in df_t.columns if 'pnl' in c), None)
    date_col_t = next((c for c in df_t.columns if 'time' in c or 'date' in c), None)
    class_col = next((c for c in df_s.columns if 'class' in c or 'sentiment' in c), None)

    if not acc_col or not pnl_col:
        st.error(f"Columns not found! Available: {list(df_t.columns)}")
        st.stop()

    # Data Formatting
    df_s['date_only'] = pd.to_datetime(df_s['date']).dt.date
    df_t['date_only'] = pd.to_datetime(df_t[date_col_t], errors='coerce').dt.date
    df_t[pnl_col] = pd.to_numeric(df_t[pnl_col], errors='coerce').fillna(0)
    
    # Aggregation
    daily = df_t.groupby([acc_col, 'date_only']).agg({
        pnl_col: 'sum',
        date_col_t: 'count' # Trade count
    }).reset_index()
    daily.columns = ['account', 'date', 'pnl', 'trades']
    
    # Final Merge
    df = pd.merge(daily, df_s[['date_only', class_col]], 
                  left_on='date', right_on='date_only', how='inner')
    df.rename(columns={class_col: 'sentiment'}, inplace=True)
    return df

# --- 3. Execution ---
try:
    df_final = load_and_process_data()
    
    # Simple UI
    st.success("Data loaded successfully!")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Avg PnL", f"${df_final['pnl'].mean():.2f}")
    with col2:
        st.metric("Total Trades", df_final['trades'].sum())

    # Chart
    fig = px.box(df_final, x='sentiment', y='pnl', color='sentiment', title="PnL by Sentiment")
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(df_final.head(20))

except Exception as e:
    st.error(f"Detailed Error: {e}")

