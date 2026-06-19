import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================================
# ORIGINAL ELT PIPELINE (COMMENTED OUT FOR DEPLOYMENT)
# =====================================================================
# from sqlalchemy import create_engine
# engine = create_engine('mysql+mysqlconnector://user:password@localhost/db_name')
# query = """
#     SELECT user_id, MAX(transaction_date) as last_transaction,
#     DATEDIFF(CURRENT_DATE, MAX(transaction_date)) as value_exchange_latency,
#     SUM(capital_balance) as idle_capital,
#     CASE 
#         WHEN DATEDIFF(CURRENT_DATE, MAX(transaction_date)) > 30 THEN 'High Risk'
#         WHEN DATEDIFF(CURRENT_DATE, MAX(transaction_date)) > 15 THEN 'Medium Risk'
#         ELSE 'Low Risk'
#     END as churn_risk_segment
#     FROM user_ledgers GROUP BY user_id
# """
# df_live = pd.read_sql(query, engine)
# df_live.to_csv('final_segmentation.csv', index=False)
# =====================================================================

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Churn Risk Dashboard", page_icon="🔄", layout="wide")

st.title("🔄 User Lifecycle Stagnation & Churn Analysis")
st.markdown("Isolating high-risk users based on Value-Exchange Latency and Idle Capital.")
st.divider()

# --- 2. SAFE DATA LOADING ---
@st.cache_data
def load_data():
    # MEMORY FIX: nrows=1000 prevents the free cloud server from crashing if the CSV is massive.
    # It will only load the top 1000 rows for the resume demo.
    df = pd.read_csv('final_segmentation.csv', nrows=1000)
    return df

# --- 3. DASHBOARD DISPLAY ---
try:
    with st.spinner('Loading data...'):
        df = load_data()
    
    st.success("✅ Data loaded successfully!")
    
    # Display the data table
    st.subheader("High-Risk User Roster (Preview)")
    st.dataframe(df, use_container_width=True)
    
    # Check if expected columns exist before trying to plot
    # Update these column names if they are different in your actual CSV!
    if 'churn_risk_segment' in df.columns and 'idle_capital' in df.columns:
        st.subheader("Capital at Risk by Segment")
        fig = px.bar(df, x='churn_risk_segment', y='idle_capital', color='churn_risk_segment')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("💡 Data loaded, but chart columns ('churn_risk_segment', 'idle_capital') were not found in the CSV. Adjust the column names in app.py to match your data to see the chart.")

except FileNotFoundError:
    st.error("🚨 Error: Could not find 'final_segmentation.csv'. Please ensure it is uploaded to the GitHub repository.")
except Exception as e:
    st.error(f"🚨 An unexpected error occurred: {e}")
