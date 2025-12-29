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
""")
# === Info Expanders ===
# st.markdown("---")


# === Project Overview & RFM Methodology ===
st.subheader("📖 About This Project & Methodology")

# Project Overview Expander
with st.expander("📌 What is this project?", expanded=False):
    st.markdown("""
    **Project Overview**  
    This dashboard analyzes ~540,000 real e-commerce transactions from a UK-based online retailer (2010–2011) to deliver actionable customer insights using **RFM analysis** (Recency, Frequency, Monetary value).

    **Key Objectives:**
    - Segment customers based on purchasing behavior
    - Identify high-value and at-risk customers
    - Quantify revenue at risk from churn
    - Provide data-driven recommendations to improve retention and growth

    **Data Source:** Public UCI Online Retail dataset  
    **Tech Stack:** Python, Pandas, SQL (DuckDB), Plotly, Streamlit
    """)

# RFM Methodology Expander
with st.expander("❓ How are RFM Segments Calculated?", expanded=False):
    st.markdown("""
    **RFM Analysis – Simple Explanation**

    RFM = **Recency** (how recent), **Frequency** (how often), **Monetary** (how much spent).

    Customers are divided into **5 equal groups (quintiles)**:
    - Score **5** = top 20% (best)
    - Score **1** = bottom 20%

    | Factor      | Measures                             | Scoring Direction                  |
    |-------------|--------------------------------------|------------------------------------|
    | Recency (R) | Days since last purchase             | Fewer days = higher score          |
    | Frequency (F) | Number of purchases                | More = higher score                |
    | Monetary (M) | Total spend                          | Higher = higher score              |

    Scores combine into an **RFM code** (e.g., 555 = best).

    **Customer Segments** (exact classification rules):

    | Segment                | Typical RFM Pattern       | Key Characteristics                              | Business Action                          |
    |------------------------|---------------------------|--------------------------------------------------|------------------------------------------|
    | **Champions**          | 555, 554, 545, 544        | Recent, frequent, high-spending - your VIPs     | Reward & retain at all costs             |
    | **Loyal Customers**    | High R & F (R≥4, F≥4)     | Very frequent buyers                             | Encourage advocacy & upsell              |
    | **Potential Loyalists**| High Recency (R≥3–5) + moderate F/M | Recent buyers already showing repeat behavior   | Nurture with personalized offers         |
    | **New Customers**      | Very high Recency (R=5) + low F/M         | Just made first/recent purchase - no repeat yet | Welcome series, easy re-purchase path    |
    | **At Risk**            | Previously high F/M, now low R            | Valuable in past but slipping away               | Urgent win-back campaigns                |
    | **Can't Lose Them**    | High F/M but low Recency                  | Big spenders going dormant                       | High-priority re-engagement              |
    | **Hibernating**        | Low Recency & moderate past activity      | Inactive but some history                        | Low-cost re-activation attempts          |
    | **Lost**               | Low scores across all (111–222)           | Long gone, low value                             | Minimal effort or ignore                 |

    **Key Distinction: Potential Loyalists vs New Customers**  
    - **New Customers**: Very recent but only 1–2 purchases and low spend - true beginners  
    - **Potential Loyalists**: Recent AND already showing repeat purchases or higher spend - on track to become loyal

    This segmentation is fully **data-driven** using relative quintiles - no fixed thresholds.
    """)

# st.markdown("---")
# === Key Insights ===
# st.markdown("---")
st.subheader("🔑 Key Insights & Actionable Recommendations")

with st.expander("👑 Elite Customers Drive Nearly Half the Business", expanded=False):
    st.markdown("""
    **Insight:** Champions (top RFM segment) generate **44.9% of total revenue** (£3.86M from £8.6M total).
    
    **Why it matters:** This follows the classic 80/20 rule - a small group of loyal, high-spending customers supports the majority of the business.
    
    **Recommendation:** Protect this group with VIP treatment:
    - Exclusive early access to new products
    - Personalized thank-you offers
    - Dedicated customer support channel
    """)

with st.expander("⚠️ £1.46M Revenue at Risk from Churning Customers", expanded=False):
    st.markdown("""
    **Insight:** Customers in At Risk, Hibernating, and Lost segments contributed **£1.46M** in historical revenue.
    
    **Why it matters:** These customers have stopped or slowed purchasing - without intervention, this revenue will disappear.
    
    **Recommendation:** Launch targeted win-back campaigns:
    - Personalized re-engagement emails with special discounts
    - "We miss you" offers based on past purchases
    - Expected recovery: 15–25% (£220k–£365k annual uplift)
    """)

with st.expander("🇬🇧 UK Dominates but Has Lower Customer Value", expanded=False):
    st.markdown("""
    **Insight:** United Kingdom accounts for **81% of revenue** (£7M) but has lower average customer spend than international markets.
    
    **Why it matters:** The business is heavily reliant on one market with moderate lifetime value.
    
    **Recommendation:** Maintain strong UK retention while shifting growth focus:
    - Continue domestic campaigns
    - Allocate budget to high-value international expansion
    """)

with st.expander("🌍 International Customers Are 5–50x More Valuable", expanded=False):
    st.markdown("""
    **Insight:** Top non-UK customers spend dramatically more:
    - EIRE: £88,515 avg
    - Netherlands: £31,716 avg
    - Australia: £15,546 avg
    
    **Why it matters:** These markets deliver exceptional lifetime value with potentially lower competition.
    
    **Recommendation:** Prioritize expansion here:
    - Localized marketing and website translations
    - Country-specific promotions
    - Highest ROI potential for acquisition spend
    """)

with st.expander("🚀 Geographic Expansion Opportunity", expanded=False):
    st.markdown("""
    **Insight:** Non-UK customers contribute only ~19% of revenue despite having the highest-value segments.
    
    **Why it matters:** Growth is constrained by over-reliance on one market.
    
    **Recommendation:** Strategic international scaling:
    - Double marketing efforts in top 5 high-value countries
    - Leverage existing high-LTV customer behavior for lower acquisition costs
    - Potential for significant revenue growth without entering entirely new regions
    """)

with st.expander("🛡️ Customer Base Is Concentrated and Vulnerable", expanded=False):
    st.markdown("""
    **Insight:** Just 4,337 customers generate £8.6M in revenue - highly dependent on repeat purchases.
    
    **Why it matters:** Any churn in top segments could materially impact the business.
    
    **Recommendation:** Balance retention and acquisition:
    - Strengthen loyalty programs for existing customers
    - Diversify customer base through sustainable acquisition channels
    - Build resilience against individual customer loss
    """)

st.markdown("---")


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


# === Revenue by Segment (Fixed label cutoff) ===
st.subheader("💰 Total Revenue Contribution by Customer Segment")

segment_rev = df.groupby('Segment')['monetary'].sum().sort_values(ascending=True).reset_index()

fig_bar = px.bar(
    segment_rev,
    x='monetary',
    y='Segment',
    orientation='h',
    title="Total Revenue by Customer Segment (£)",
    color='Segment',
    height=600,  # Increased height for better spacing
    text=segment_rev['monetary'].apply(lambda x: f"£{x:,.0f}")
)

# Key fixes for label cutoff
fig_bar.update_traces(
    textposition='outside',  # Keep outside for impact
    cliponaxis=False         # Allows text to extend beyond plot area
)

fig_bar.update_layout(
    showlegend=False,
    xaxis_title="Total Revenue (£)",
    yaxis_title="Customer Segment",
    margin=dict(l=0, r=50, t=80, b=60),  # Extra right margin for long labels
    uniformtext_minsize=10,
    uniformtext_mode='hide'  # Hides text if too small (fallback safety)
)

st.plotly_chart(fig_bar, use_container_width=True)

# Note below chart
total_rev = df['monetary'].sum()
champions_share = (df[df['Segment']=='Champions']['monetary'].sum() / total_rev * 100)
st.markdown(f"**Insight:** Champions alone drive **{champions_share:.1f}%** of total revenue.")

# === Top Customers Table ===
st.subheader("Top 10 Champions")
champions = df[df['Segment'] == 'Champions'].nlargest(10, 'monetary')
st.dataframe(champions[['CustomerID', 'recency_days', 'frequency', 'monetary', 'first_purchase_date']], use_container_width=True)

# # === Customer Lookup ===
# st.subheader("🔍 Customer 360 Lookup")
# customer_id = st.number_input("Enter CustomerID", min_value=int(df['CustomerID'].min()), max_value=int(df['CustomerID'].max()), step=1)
# if st.button("Search"):
#     cust = df[df['CustomerID'] == customer_id]
#     if not cust.empty:
#         st.write(cust.T)  # Transposed for nice view
#     else:
#         st.error("Customer not found")