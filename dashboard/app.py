import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

import os
print("Current working directory:", os.getcwd())  # Should show .../dashboard
print("Looking for data at:", os.path.abspath("../../data_clean/customer_rfm_segmented.csv"))

# === Page Config ===
st.set_page_config(
    page_title="E-Commerce Customer Intelligence",
    page_icon="🛒",
    layout="wide"
)

# === Load Data (Robust path) ===
import os

@st.cache_data
def load_data():
    # __file__ is the full path to app.py
    # dirname twice: go from /dashboard/app.py → /dashboard/ → project root
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(project_root, "data_clean", "customer_rfm_segmented.csv")
    
    df = pd.read_csv(file_path, 
                     parse_dates=['first_purchase_date', 'last_purchase_date', 'analysis_date'])
    return df

df = load_data()

# === Sidebar ===
st.sidebar.header("E-Commerce Customer Dashboard")
st.sidebar.metric("Total Customers", f"{len(df):,}")
st.sidebar.metric("Total Revenue", f"£{df['monetary'].sum():,.0f}")
at_risk = df[df['Segment'].isin(['At Risk', 'Hibernating', 'Lost', "Can't Lose Them"])]
st.sidebar.metric("Revenue at Risk", f"£{at_risk['monetary'].sum():,.0f}", delta=None)

st.sidebar.markdown("---")
st.sidebar.caption("Built with ❤️ using Streamlit • Data: UCI Online Retail")

# === Main Title ===
st.title("🛒 Global E-Commerce Customer Intelligence Dashboard")
st.markdown("""
From 540,000 raw transactions → actionable customer insights  
**Key Finding:** £{:,.0f} in revenue is at risk from vulnerable customers
""".format(at_risk['monetary'].sum()))

# === Layout: Two Columns ===
col1, col2 = st.columns(2)

with col1:
    # Segment Distribution
    segment_counts = df['Segment'].value_counts().reset_index()
    segment_counts.columns = ['Segment', 'Count']
    fig_pie = px.pie(segment_counts, values='Count', names='Segment', title="Customer Segments")
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    # Monetary by Segment
    segment_monetary = df.groupby('Segment')['monetary'].sum().sort_values(ascending=False).reset_index()
    fig_bar = px.bar(segment_monetary, x='Segment', y='monetary', title="Revenue by Segment (£)")
    st.plotly_chart(fig_bar, use_container_width=True)

# === RFM Scatter ===
st.subheader("RFM Scatter: Recency vs Frequency (size = Monetary)")
fig_scatter = px.scatter(
    df, x='recency_days', y='frequency', size='monetary', color='Segment',
    hover_data=['CustomerID'], title="Customer Distribution"
)
st.plotly_chart(fig_scatter, use_container_width=True)

# === Top Customers Table ===
st.subheader("Top 10 Champions")
champions = df[df['Segment'] == 'Champions'].nlargest(10, 'monetary')
st.dataframe(champions[['CustomerID', 'recency_days', 'frequency', 'monetary', 'first_purchase_date']], use_container_width=True)

# === Customer Lookup ===
st.subheader("🔍 Customer 360 Lookup")
customer_id = st.number_input("Enter CustomerID", min_value=int(df['CustomerID'].min()), max_value=int(df['CustomerID'].max()), step=1)
if st.button("Search"):
    cust = df[df['CustomerID'] == customer_id]
    if not cust.empty:
        st.write(cust.T)  # Transposed for nice view
    else:
        st.error("Customer not found")