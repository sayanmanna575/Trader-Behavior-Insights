# Data Science Assignment: Trader Behavior vs Market Sentiment Analysis

## Assignment Overview
This assignment explores and analyzes the relationship between trader behavior and market sentiment using two key datasets:
1. **Bitcoin Market Sentiment Dataset** - Daily Fear & Greed Index values
2. **Historical Trader Data from Hyperliquid** - Transaction records with details on profitability, risk, volume, and leverage

## Approach
I conducted a comprehensive analysis following these steps:
1. **Data Loading and Preprocessing** - Loaded both datasets and converted date formats for consistency
2. **Data Aggregation** - Grouped trading data by date to calculate daily metrics (volume, profit/loss, trade count)
3. **Data Merging** - Combined trading metrics with sentiment data by date
4. **Statistical Analysis** - Calculated correlations and grouped metrics by sentiment categories
5. **Data Visualization** - Created charts to illustrate key findings
6. **Insight Generation** - Interpreted results and derived strategic implications

## Key Findings

### Counterintuitive Trading Patterns
The analysis revealed that trader behavior on Hyperliquid is counterintuitive when compared to traditional market wisdom:

1. **Activity During Fear vs Greed**
   - Trading volume is **highest during extreme fear** ($8.2M daily avg) and **lowest during extreme greed** ($1.1M daily avg)
   - Trade frequency follows the same pattern: 1,528 trades/day during extreme fear vs 260 trades/day during greed
   - This contradicts the common belief that trading activity peaks during bullish markets

2. **Profitability Patterns**
   - Average daily profits are highest during extreme fear periods ($52,793)
   - Win rates (percentage of profitable days) are actually highest during extreme greed periods (87.72%)
   - Risk-adjusted returns are best during extreme greed (0.021037)

3. **Statistical Correlations**
   - Sentiment vs Trading Volume: -0.274 (negative correlation)
   - Sentiment vs Trade Count: -0.247 (negative correlation)
   - Sentiment vs Profitability: -0.096 (slight negative correlation)

## Strategic Implications

### For Individual Traders
1. **Contrarian Approach**: The data suggests opportunities during fearful market periods when activity is high
2. **Risk Management**: Fearful periods require careful risk management despite higher profit potential
3. **Market Timing**: Understanding sentiment cycles can inform trading activity levels

### For Market Observers
1. **Volume Indicators**: High trading volumes may signal fearful rather than greedy market conditions
2. **Behavioral Patterns**: Consistent patterns emerge that can inform market analysis
3. **Predictive Value**: Sentiment data can help predict trading activity patterns

## Technical Implementation

### Files Created
1. **analysis.py** - Main analysis script with basic visualizations
2. **advanced_analysis.py** - Enhanced analysis with additional metrics
3. **trader_behavior_analysis_report.md** - Initial findings report
4. **final_analysis_report.md** - Comprehensive analysis with strategic implications
5. **README.md** - Project overview and usage instructions
6. **Visualizations** - PNG files with charts and graphs

### Key Metrics
- **Analysis Period**: 479 days (May 1, 2023 to May 1, 2025)
- **Total Trading Volume**: $1.19 billion
- **Overall Profit/Loss**: $10.25 million gain
- **Total Number of Trades**: 211,218

## Conclusion

This analysis demonstrates that successful trading on Hyperliquid may require a contrarian approach - being most active when markets are fearful rather than greedy. The strong negative correlations between market sentiment and both trading volume (-0.274) and trade frequency (-0.247) indicate consistent behavioral patterns that could be strategically leveraged.

The findings support the famous Warren Buffett advice to "be fearful when others are greedy and greedy when others are fearful," at least from a trading activity perspective. Traders on Hyperliquid appear to follow this principle, with the highest activity and profitability occurring during fearful market periods.

These insights could inform trading strategies, risk management approaches, and market analysis techniques for both individual traders and financial institutions.