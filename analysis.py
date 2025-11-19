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

print("Datasets loaded and processed.")
print(f"Fear/Greed data date range: {fear_greed_df['date'].min()} to {fear_greed_df['date'].max()}")
print(f"Trading data date range: {trading_df['date'].min()} to {trading_df['date'].max()}")

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

# Analysis 1: Volume vs Sentiment
print("\n1. Analyzing trading volume vs market sentiment...")
volume_by_sentiment = merged_df.groupby('classification')['Size USD'].mean().reset_index()
volume_by_sentiment = volume_by_sentiment.sort_values('Size USD', ascending=False)

print("Average trading volume by sentiment:")
for _, row in volume_by_sentiment.iterrows():
    print(f"  {row['classification']}: ${row['Size USD']:,.2f}")

# Analysis 2: Profitability vs Sentiment
print("\n2. Analyzing profitability vs market sentiment...")
profit_by_sentiment = merged_df.groupby('classification')['Closed PnL'].mean().reset_index()
profit_by_sentiment = profit_by_sentiment.sort_values('Closed PnL', ascending=False)

print("Average profit/loss by sentiment:")
for _, row in profit_by_sentiment.iterrows():
    print(f"  {row['classification']}: ${row['Closed PnL']:,.2f}")

# Analysis 3: Trade frequency vs Sentiment
print("\n3. Analyzing trade frequency vs market sentiment...")
trades_by_sentiment = merged_df.groupby('classification')['trade_count'].mean().reset_index()
trades_by_sentiment = trades_by_sentiment.sort_values('trade_count', ascending=False)

print("Average number of trades by sentiment:")
for _, row in trades_by_sentiment.iterrows():
    print(f"  {row['classification']}: {row['trade_count']:.1f} trades")

# Correlation analysis
print("\n4. Correlation analysis...")
correlation_sentiment_volume = merged_df['sentiment_score'].corr(merged_df['Size USD'])
correlation_sentiment_profit = merged_df['sentiment_score'].corr(merged_df['Closed PnL'])
correlation_sentiment_trades = merged_df['sentiment_score'].corr(merged_df['trade_count'])

print(f"Correlation between sentiment and trading volume: {correlation_sentiment_volume:.3f}")
print(f"Correlation between sentiment and profitability: {correlation_sentiment_profit:.3f}")
print(f"Correlation between sentiment and trade count: {correlation_sentiment_trades:.3f}")

# Create visualizations
print("\n5. Creating visualizations...")

# Set up the plotting style
plt.style.use('seaborn-v0_8')
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('Trader Behavior vs Market Sentiment Analysis', fontsize=16)

# 1. Volume by sentiment
sns.barplot(data=volume_by_sentiment, x='classification', y='Size USD', ax=axes[0,0])
axes[0,0].set_title('Average Trading Volume by Market Sentiment')
axes[0,0].set_ylabel('Volume (USD)')
axes[0,0].tick_params(axis='x', rotation=45)

# 2. Profitability by sentiment
sns.barplot(data=profit_by_sentiment, x='classification', y='Closed PnL', ax=axes[0,1])
axes[0,1].set_title('Average Profit/Loss by Market Sentiment')
axes[0,1].set_ylabel('Profit/Loss (USD)')
axes[0,1].tick_params(axis='x', rotation=45)

# 3. Trade count by sentiment
sns.barplot(data=trades_by_sentiment, x='classification', y='trade_count', ax=axes[1,0])
axes[1,0].set_title('Average Number of Trades by Market Sentiment')
axes[1,0].set_ylabel('Number of Trades')
axes[1,0].tick_params(axis='x', rotation=45)

# 4. Scatter plot of sentiment score vs volume
sns.scatterplot(data=merged_df, x='sentiment_score', y='Size USD', ax=axes[1,1])
axes[1,1].set_title('Trading Volume vs Sentiment Score')
axes[1,1].set_xlabel('Sentiment Score (1=Extreme Fear, 5=Extreme Greed)')
axes[1,1].set_ylabel('Volume (USD)')

# Adjust layout
plt.tight_layout()
plt.savefig('trader_behavior_analysis.png', dpi=300, bbox_inches='tight')
print("Visualization saved as 'trader_behavior_analysis.png'")

# Additional insights
print("\n6. Key Insights:")
print(f"  - Data covers {len(merged_df)} days from {merged_df['date'].min().strftime('%Y-%m-%d')} to {merged_df['date'].max().strftime('%Y-%m-%d')}")
print(f"  - Total trading volume: ${merged_df['Size USD'].sum():,.2f}")
print(f"  - Overall profit/loss: ${merged_df['Closed PnL'].sum():,.2f}")
print(f"  - Total number of trades: {merged_df['trade_count'].sum():,}")

# Find the most common sentiment
sentiment_counts = merged_df['classification'].value_counts()
most_common_sentiment = sentiment_counts.index[0]
print(f"  - Most common market sentiment: {most_common_sentiment} ({sentiment_counts.iloc[0]} days)")

# Find best performing sentiment
best_sentiment = profit_by_sentiment.loc[profit_by_sentiment['Closed PnL'].idxmax(), 'classification']
worst_sentiment = profit_by_sentiment.loc[profit_by_sentiment['Closed PnL'].idxmin(), 'classification']
print(f"  - Most profitable sentiment: {best_sentiment}")
print(f"  - Least profitable sentiment: {worst_sentiment}")

print("\nAnalysis complete!")