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


# === Customer Count and Revenue by Segment (Stacked, Same Order) ===
st.subheader("📊 Customer Distribution and Revenue Impact by Segment")

# Calculate revenue per segment and sort descending (highest revenue at top)
segment_rev = df.groupby('Segment')['monetary'].sum().reset_index()
segment_rev = segment_rev.sort_values('monetary', ascending=False)  # Highest revenue first
segment_order = segment_rev['Segment'].tolist()  # Save the order

# === Chart 2: Total Revenue per Segment ===
st.markdown("**Total Revenue per Segment**")

# Use the same ordered segment_rev
fig_rev = px.bar(
    segment_rev,
    x='monetary',
    y='Segment',
    orientation='h',
    color='Segment',
    height=600,
    text=segment_rev['monetary'].apply(lambda x: f"£{x:,.0f}")
)

fig_rev.update_traces(textposition='outside', cliponaxis=False)
fig_rev.update_layout(
    showlegend=False,
    xaxis_title="Total Revenue (£)",
    yaxis_title="Customer Segment",
    margin=dict(l=150, r=200, t=80, b=60)
)

st.plotly_chart(fig_rev, use_container_width=True)

# === Chart 1: Number of Customers per Segment ===
st.markdown("**Number of Customers per Segment**")

segment_count = df['Segment'].value_counts().reset_index()
segment_count.columns = ['Segment', 'Customer Count']
# Reorder to match revenue order
segment_count['Segment'] = pd.Categorical(segment_count['Segment'], categories=segment_order)
segment_count = segment_count.sort_values('Segment')

fig_count = px.bar(
    segment_count,
    x='Customer Count',
    y='Segment',
    orientation='h',
    color='Segment',
    height=600,
    text='Customer Count'
)

fig_count.update_traces(textposition='outside', cliponaxis=False)
fig_count.update_layout(
    showlegend=False,
    xaxis_title="Number of Customers",
    yaxis_title="Customer Segment",
    margin=dict(l=150, r=200, t=80, b=60)
)

st.plotly_chart(fig_count, use_container_width=True)

# === Key Insight ===
total_customers = len(df)
total_rev = df['monetary'].sum()
champions_customers = len(df[df['Segment'] == 'Champions'])
champions_rev_share = (df[df['Segment'] == 'Champions']['monetary'].sum() / total_rev) * 100 if total_rev > 0 else 0

st.markdown(
    f"**Key Insight:** Champions represent only **{champions_customers:,} customers** "
    f"({(champions_customers / total_customers * 100):.1f}% of total) "
    f"but generate **{champions_rev_share:.1f}%** of all revenue."
)


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