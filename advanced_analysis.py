import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Load the datasets
print("Loading datasets...")
fear_greed_df = pd.read_csv('fear_greed_index.csv')
trading_df = pd.read_csv('historical_data.csv')

# Convert date formats
print("Processing fear and greed data...")
fear_greed_df['date'] = pd.to_datetime(fear_greed_df['date'])
fear_greed_df['classification'] = fear_greed_df['classification'].astype('category')

# Convert trading data timestamp
print("Processing trading data...")
trading_df['Timestamp IST'] = pd.to_datetime(trading_df['Timestamp IST'], format='%d-%m-%Y %H:%M')
trading_df['date'] = trading_df['Timestamp IST'].dt.date
trading_df['date'] = pd.to_datetime(trading_df['date'])

# Map fear/greed classifications to numerical values for correlation analysis
fear_greed_mapping = {
    'Extreme Fear': 1,
    'Fear': 2,
    'Neutral': 3,
    'Greed': 4,
    'Extreme Greed': 5
}
fear_greed_df['sentiment_score'] = fear_greed_df['classification'].map(fear_greed_mapping)

# Aggregate trading data by date
print("Aggregating trading data...")
daily_trading = trading_df.groupby('date').agg({
    'Size USD': 'sum',  # Total trading volume
    'Fee': 'sum',       # Total fees
    'Closed PnL': 'sum' # Total profit/loss
}).reset_index()

# Add trade count
trade_counts = trading_df.groupby('date').size().reset_index(name='trade_count')
daily_trading = daily_trading.merge(trade_counts, on='date', how='left')

# Add average leverage (if available)
if 'Leverage' in trading_df.columns:
    avg_leverage = trading_df.groupby('date')['Leverage'].mean().reset_index(name='avg_leverage')
    daily_trading = daily_trading.merge(avg_leverage, on='date', how='left')

# Merge with sentiment data
print("Merging datasets...")
merged_df = daily_trading.merge(fear_greed_df[['date', 'classification', 'sentiment_score', 'value']], on='date', how='inner')

print(f"Merged dataset has {len(merged_df)} days of data")

# Create advanced visualizations
print("\nCreating advanced visualizations...")

# Set up the plotting style
plt.style.use('seaborn-v0_8')
fig = plt.figure(figsize=(20, 15))

# 1. Time series of sentiment score and trading volume
ax1 = plt.subplot(3, 2, 1)
ax1.plot(merged_df['date'], merged_df['value'], label='Fear/Greed Index', color='blue')
ax1.set_ylabel('Fear/Greed Index', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.set_title('Fear/Greed Index Over Time')

ax2 = ax1.twinx()
ax2.plot(merged_df['date'], merged_df['Size USD'], label='Trading Volume', color='red', alpha=0.7)
ax2.set_ylabel('Trading Volume (USD)', color='red')
ax2.tick_params(axis='y', labelcolor='red')

# 2. Scatter plot with trend line
ax3 = plt.subplot(3, 2, 2)
sns.scatterplot(data=merged_df, x='value', y='Size USD', hue='classification', ax=ax3)
ax3.set_title('Trading Volume vs Fear/Greed Index')
ax3.set_xlabel('Fear/Greed Index Value')
ax3.set_ylabel('Trading Volume (USD)')

# Add trend line
z = np.polyfit(merged_df['value'], merged_df['Size USD'], 1)
p = np.poly1d(z)
ax3.plot(merged_df['value'], p(merged_df['value']), "r--", alpha=0.8)

# 3. Box plot of volume by sentiment category
ax4 = plt.subplot(3, 2, 3)
sns.boxplot(data=merged_df, x='classification', y='Size USD', ax=ax4)
ax4.set_title('Distribution of Trading Volume by Sentiment')
ax4.tick_params(axis='x', rotation=45)
ax4.set_ylabel('Trading Volume (USD)')

# 4. Profitability over time
ax5 = plt.subplot(3, 2, 4)
ax5.plot(merged_df['date'], merged_df['Closed PnL'], color='green')
ax5.set_title('Daily Profit/Loss Over Time')
ax5.set_ylabel('Profit/Loss (USD)')
ax5.axhline(y=0, color='black', linestyle='-', alpha=0.3)

# 5. Correlation heatmap
ax6 = plt.subplot(3, 2, 5)
correlation_data = merged_df[['value', 'sentiment_score', 'Size USD', 'Closed PnL', 'trade_count']]
correlation_matrix = correlation_data.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, ax=ax6)
ax6.set_title('Correlation Matrix')

# 6. Sentiment distribution
ax7 = plt.subplot(3, 2, 6)
sentiment_counts = merged_df['classification'].value_counts()
ax7.pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%')
ax7.set_title('Distribution of Market Sentiments')

# Adjust layout
plt.tight_layout()
plt.savefig('advanced_trader_behavior_analysis.png', dpi=300, bbox_inches='tight')
print("Advanced visualization saved as 'advanced_trader_behavior_analysis.png'")

# Additional detailed analysis
print("\nPerforming detailed analysis...")

# Calculate metrics by sentiment
detailed_analysis = merged_df.groupby('classification').agg({
    'Size USD': ['mean', 'median', 'std'],
    'Closed PnL': ['mean', 'median', 'std'],
    'trade_count': ['mean', 'median', 'std']
}).round(2)

print("\nDetailed metrics by sentiment:")
print(detailed_analysis)

# Calculate win rate by sentiment
merged_df['is_profitable'] = merged_df['Closed PnL'] > 0
win_rate_by_sentiment = merged_df.groupby('classification')['is_profitable'].mean().reset_index()
win_rate_by_sentiment.columns = ['classification', 'win_rate']
win_rate_by_sentiment = win_rate_by_sentiment.sort_values('win_rate', ascending=False)

print("\nWin rate by sentiment:")
for _, row in win_rate_by_sentiment.iterrows():
    print(f"  {row['classification']}: {row['win_rate']:.2%}")

# Risk-adjusted returns (Profit/Volatility)
merged_df['risk_adjusted'] = merged_df['Closed PnL'] / merged_df['Size USD']
risk_adj_by_sentiment = merged_df.groupby('classification')['risk_adjusted'].mean().reset_index()
risk_adj_by_sentiment = risk_adj_by_sentiment.sort_values('risk_adjusted', ascending=False)

print("\nRisk-adjusted returns by sentiment:")
for _, row in risk_adj_by_sentiment.iterrows():
    print(f"  {row['classification']}: {row['risk_adjusted']:.6f}")

print("\nAdvanced analysis complete!")