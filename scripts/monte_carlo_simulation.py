"""
Monte Carlo Simulation for NAV Growth Projection (5 Years)
Bonus Challenge B3 - Projects future NAV with uncertainty bands
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from pathlib import Path

# Load historical NAV data
base_path = Path(r"C:\Users\pushk\OneDrive\Desktop\AIML\Blue Stocks\mutual-fund-analytics\data\processed")
nav_df = pd.read_csv(base_path / "nav_history_clean.csv")
nav_df['date'] = pd.to_datetime(nav_df['date'])

# Configuration
NUM_SIMULATIONS = 1000
PROJECTION_DAYS = 252 * 5  # 5 years
CONFIDENCE_LEVEL = 0.95

def run_monte_carlo_simulation(scheme_code, nav_history, num_sims=NUM_SIMULATIONS, days=PROJECTION_DAYS):
    """
    Run Monte Carlo simulation for NAV projection
    """
    # Calculate historical daily returns
    daily_returns = nav_history['nav'].pct_change().dropna()
    
    # Parameters
    mu = daily_returns.mean()  # Mean return
    sigma = daily_returns.std()  # Volatility
    last_nav = nav_history['nav'].iloc[-1]
    last_date = nav_history['date'].iloc[-1]
    
    # Initialize simulation array
    simulations = np.zeros((days + 1, num_sims))
    simulations[0, :] = last_nav
    
    # Run simulations
    for t in range(1, days + 1):
        Z = np.random.standard_normal(num_sims)
        simulations[t, :] = simulations[t-1, :] * np.exp((mu - 0.5 * sigma ** 2) + sigma * Z)
    
    return simulations, last_date, mu, sigma

# Run simulations for top 5 schemes
top_schemes = nav_df.groupby('amfi_code')['nav'].mean().nlargest(5).index

results = {}
for scheme in top_schemes:
    scheme_data = nav_df[nav_df['amfi_code'] == scheme].sort_values('date')
    simulations, last_date, mu, sigma = run_monte_carlo_simulation(
        scheme, scheme_data, NUM_SIMULATIONS, PROJECTION_DAYS
    )
    results[scheme] = {
        'simulations': simulations,
        'last_date': last_date,
        'mu': mu,
        'sigma': sigma,
        'scheme_name': scheme_data['scheme_name'].iloc[0] if 'scheme_name' in scheme_data.columns else scheme
    }

# Generate visualizations and statistics
report_path = Path(r"C:\Users\pushk\OneDrive\Desktop\AIML\Blue Stocks\mutual-fund-analytics\reports")

# Create summary statistics
summary_stats = []

for scheme, data in results.items():
    sims = data['simulations']
    last_nav = sims[0, 0]
    final_navs = sims[-1, :]
    
    # Calculate statistics
    mean_final = np.mean(final_navs)
    std_final = np.std(final_navs)
    percentile_5 = np.percentile(final_navs, 5)
    percentile_95 = np.percentile(final_navs, 95)
    median_final = np.median(final_navs)
    
    # Expected return over 5 years
    expected_return = ((mean_final / last_nav) ** (1/5) - 1) * 100
    
    summary_stats.append({
        'Scheme': data['scheme_name'],
        'Current NAV': f"₹{last_nav:.2f}",
        'Expected NAV (5Y)': f"₹{mean_final:.2f}",
        'Upside (95%)': f"₹{percentile_95:.2f}",
        'Downside (5%)': f"₹{percentile_5:.2f}",
        'Expected CAGR': f"{expected_return:.2f}%",
        'Confidence Range': f"₹{percentile_5:.2f} - ₹{percentile_95:.2f}"
    })

summary_df = pd.DataFrame(summary_stats)
summary_df.to_csv(report_path / "monte_carlo_projections.csv", index=False)

print("\n" + "="*100)
print("MONTE CARLO SIMULATION RESULTS - 5 YEAR NAV PROJECTIONS")
print("="*100)
print(summary_df.to_string(index=False))
print("="*100)
print(f"Simulations run: {NUM_SIMULATIONS} per scheme")
print(f"Projection period: 5 years ({PROJECTION_DAYS} trading days)")
print(f"Confidence level: {CONFIDENCE_LEVEL*100:.0f}%")

# Create visualization for one scheme (top performer)
top_scheme = list(results.keys())[0]
data = results[top_scheme]
sims = data['simulations']

# Create plotly visualization
dates = pd.date_range(start=data['last_date'], periods=len(sims), freq='D')

# Calculate percentiles for confidence bands
percentile_5 = np.percentile(sims, 5, axis=1)
percentile_25 = np.percentile(sims, 25, axis=1)
percentile_50 = np.percentile(sims, 50, axis=1)
percentile_75 = np.percentile(sims, 75, axis=1)
percentile_95 = np.percentile(sims, 95, axis=1)

fig = go.Figure()

# Add confidence bands
fig.add_trace(go.Scatter(
    x=dates, y=percentile_95,
    name='95% Confidence', mode='lines',
    line=dict(color='rgba(255, 0, 0, 0.3)', width=0),
    showlegend=True
))

fig.add_trace(go.Scatter(
    x=dates, y=percentile_5,
    name='5% Confidence', mode='lines',
    line=dict(color='rgba(255, 0, 0, 0.3)', width=0),
    fill='tonexty',
    fillcolor='rgba(255, 0, 0, 0.1)',
    showlegend=True
))

# Add median and quartiles
fig.add_trace(go.Scatter(
    x=dates, y=percentile_50,
    name='Median Projection', mode='lines',
    line=dict(color='darkblue', width=3)
))

fig.add_trace(go.Scatter(
    x=dates, y=percentile_25,
    name='25-75% Interquartile', mode='lines',
    line=dict(color='rgba(0, 0, 255, 0.3)', width=0),
    showlegend=False
))

fig.add_trace(go.Scatter(
    x=dates, y=percentile_75,
    name='25-75% Interquartile', mode='lines',
    line=dict(color='rgba(0, 0, 255, 0.3)', width=0),
    fill='tonexty',
    fillcolor='rgba(0, 0, 255, 0.1)',
    showlegend=True
))

fig.update_layout(
    title=f'Monte Carlo Simulation: {data["scheme_name"]} NAV Projection (5 Years)',
    xaxis_title='Date',
    yaxis_title='NAV (₹)',
    hovermode='x unified',
    height=600,
    template='plotly_white'
)

fig.write_html(str(report_path / "monte_carlo_projection.html"))

print(f"\n✓ Monte Carlo simulation completed")
print(f"  Projection chart saved: monte_carlo_projection.html")
print(f"  Summary statistics saved: monte_carlo_projections.csv")
