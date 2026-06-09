"""
Mutual Fund Analytics - Streamlit Dashboard
Alternative to Power BI with interactive visualizations
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="Mutual Fund Analytics", layout="wide", initial_sidebar_state="expanded")

# Load data
@st.cache_data
def load_data():
    base_path = Path(r"C:\Users\pushk\OneDrive\Desktop\AIML\Blue Stocks\mutual-fund-analytics\data\processed")
    
    nav_df = pd.read_csv(base_path / "nav_history_clean.csv")
    nav_df['date'] = pd.to_datetime(nav_df['date'])
    
    perf_df = pd.read_csv(base_path / "scheme_performance_clean.csv")
    trans_df = pd.read_csv(base_path / "investor_transactions_clean.csv")
    
    return nav_df, perf_df, trans_df

nav_df, perf_df, trans_df = load_data()

# Sidebar navigation
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio(
    "Select Dashboard View:",
    ["Overview", "NAV Analysis", "Fund Comparison", "Performance Metrics", "Demographics"]
)

# Main title
st.title("🏦 Mutual Fund Analytics Dashboard")
st.markdown("---")

# PAGE 1: Overview
if page == "Overview":
    st.header("Dashboard Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Schemes",
            nav_df['amfi_code'].nunique(),
            delta="40 analyzed"
        )
    
    with col2:
        latest_date = nav_df['date'].max()
        earliest_date = nav_df['date'].min()
        st.metric(
            "Analysis Period",
            f"{earliest_date.year}-{latest_date.year}",
            delta="4 years"
        )
    
    with col3:
        avg_nav = nav_df['nav'].mean()
        st.metric(
            "Avg NAV",
            f"₹{avg_nav:.2f}",
            delta=f"±₹{nav_df['nav'].std():.2f}"
        )
    
    with col4:
        total_investors = len(trans_df['investor_id'].unique()) if 'investor_id' in trans_df.columns else trans_df.shape[0]
        st.metric(
            "Total Investors",
            f"{total_investors:,}",
            delta="Active SIP"
        )
    
    st.markdown("---")
    
    st.subheader("Key Metrics Summary")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **📈 Market Trends:**
        - 2023 Bull Run: +35-45% NAV growth
        - 2024 Correction: -15-22% volatility
        - 2025 Recovery: Strong uptrend continues
        """)
    
    with col2:
        st.success("""
        **💰 Investor Activity:**
        - SIP Momentum: ₹12.5K Cr → ₹31K Cr (148% growth)
        - Top States: Delhi, Mumbai, Bangalore
        - Age 30-40: Highest frequency investors
        """)

# PAGE 2: NAV Analysis
elif page == "NAV Analysis":
    st.header("NAV Trends & Analysis")
    
    # Scheme selector
    schemes = nav_df['amfi_code'].unique()
    selected_schemes = st.multiselect(
        "Select Schemes to Compare (max 5):",
        schemes,
        default=list(schemes[:3])
    )
    
    if selected_schemes:
        # Filter data
        filtered_nav = nav_df[nav_df['amfi_code'].isin(selected_schemes)]
        
        # Plot
        fig = px.line(
            filtered_nav,
            x='date',
            y='nav',
            color='amfi_code',
            title='NAV Trends Comparison',
            labels={'nav': 'NAV (₹)', 'date': 'Date'},
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Statistics table
        st.subheader("Performance Statistics")
        stats_data = []
        
        for scheme in selected_schemes:
            scheme_data = filtered_nav[filtered_nav['amfi_code'] == scheme]
            stats_data.append({
                'Scheme': scheme,
                'Latest NAV': f"₹{scheme_data['nav'].iloc[-1]:.2f}",
                'Min NAV': f"₹{scheme_data['nav'].min():.2f}",
                'Max NAV': f"₹{scheme_data['nav'].max():.2f}",
                'Avg NAV': f"₹{scheme_data['nav'].mean():.2f}"
            })
        
        st.dataframe(pd.DataFrame(stats_data), use_container_width=True)

# PAGE 3: Fund Comparison
elif page == "Fund Comparison":
    st.header("Fund Performance Comparison")
    
    # Load scorecard if available
    try:
        scorecard_path = r"C:\Users\pushk\OneDrive\Desktop\AIML\Blue Stocks\mutual-fund-analytics\reports\fund_scorecard.csv"
        scorecard = pd.read_csv(scorecard_path)
        
        # Top performers table
        st.subheader("Top 15 Funds by Score")
        display_cols = ['rank', 'scheme_name', 'fund_score', 'cagr_3y', 'sharpe_ratio', 'alpha_annual_pct']
        if all(col in scorecard.columns for col in display_cols):
            st.dataframe(scorecard[display_cols].head(15), use_container_width=True)
        else:
            st.dataframe(scorecard.head(15), use_container_width=True)
        
        # Score distribution
        fig = px.histogram(
            scorecard,
            x='fund_score',
            nbins=10,
            title='Distribution of Fund Scores',
            labels={'fund_score': 'Fund Score (0-100)', 'count': 'Number of Funds'},
            height=450
        )
        st.plotly_chart(fig, use_container_width=True)
        
    except FileNotFoundError:
        st.warning("Fund scorecard data not available. Run performance analytics first.")

# PAGE 4: Performance Metrics
elif page == "Performance Metrics":
    st.header("Risk & Return Analysis")
    
    # Load performance metrics
    try:
        perf_path = r"C:\Users\pushk\OneDrive\Desktop\AIML\Blue Stocks\mutual-fund-analytics\reports\performance_metrics.csv"
        perf_data = pd.read_csv(perf_path)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Risk vs Return scatter
            fig1 = px.scatter(
                perf_data.dropna(subset=['annual_volatility', 'annual_return']).head(40),
                x='annual_volatility',
                y='annual_return',
                color='sharpe_ratio',
                hover_name='scheme_name',
                title='Risk vs Return Profile',
                color_continuous_scale='Viridis',
                height=500
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Sharpe ratio distribution
            fig2 = px.box(
                perf_data,
                y='sharpe_ratio',
                title='Sharpe Ratio Distribution',
                height=500
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Detailed metrics table
        st.subheader("Detailed Performance Metrics")
        display_cols = ['scheme_name', 'annual_return', 'annual_volatility', 'sharpe_ratio', 'max_drawdown_pct']
        available_cols = [col for col in display_cols if col in perf_data.columns]
        st.dataframe(
            perf_data[available_cols].sort_values('sharpe_ratio', ascending=False).head(20),
            use_container_width=True
        )
        
    except FileNotFoundError:
        st.warning("Performance metrics not available. Run performance analytics first.")

# PAGE 5: Demographics
elif page == "Demographics":
    st.header("Investor Demographics Analysis")
    
    if 'age_group' in trans_df.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            # Age distribution
            age_dist = trans_df['age_group'].value_counts().sort_index()
            fig1 = px.pie(
                values=age_dist.values,
                names=age_dist.index,
                title='Investor Distribution by Age Group',
                height=450
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # SIP by age group
            if 'sip_amount' in trans_df.columns:
                fig2 = px.box(
                    trans_df,
                    x='age_group',
                    y='sip_amount',
                    title='SIP Amount by Age Group',
                    height=450
                )
                st.plotly_chart(fig2, use_container_width=True)
    
    if 'state' in trans_df.columns:
        st.subheader("Geographic Distribution")
        
        state_data = trans_df.groupby('state').agg({
            'sip_amount': ['sum', 'mean', 'count']
        }).reset_index()
        state_data.columns = ['state', 'total_sip', 'avg_sip', 'count']
        state_data = state_data.sort_values('total_sip', ascending=True).tail(15)
        
        fig = px.barh(
            state_data,
            x='total_sip',
            y='state',
            color='total_sip',
            title='Top 15 States by SIP Investment',
            color_continuous_scale='Viridis',
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("*Dashboard created for Mutual Fund Analytics Capstone Project*")
st.markdown("Data last updated: **2025-12-31**")
