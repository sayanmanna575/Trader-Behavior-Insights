# Data Science Assignment: Trader Behavior vs Market Sentiment Analysis

## Project Structure

```
ds_candidate/
├── notebook_1.ipynb               # Main analysis notebook
├── notebook_2.ipynb               # Advanced analysis notebook
├── csv_files/                     # Raw data files
│   ├── fear_greed_index.csv       # Bitcoin market sentiment data
│   └── historical_data.csv        # Hyperliquid trader data
├── outputs/                       # Visualization outputs
│   ├── trader_behavior_analysis.png
│   └── advanced_trader_behavior_analysis.png
├── ds_report.pdf                  # Final report (to be generated)
└── README.md                      # This file
```

## Overview

This project analyzes the relationship between trader behavior on Hyperliquid and Bitcoin market sentiment using two key datasets:

1. **Bitcoin Market Sentiment Dataset** - Daily Fear & Greed Index values
2. **Historical Trader Data from Hyperliquid** - Transaction records with details on profitability, risk, volume, and leverage

## Key Findings

### Counterintuitive Trading Patterns

1. **Activity During Fear vs Greed**
   - Trading volume is **highest during extreme fear** ($8.2M daily avg) and **lowest during extreme greed** ($1.1M daily avg)
   - Trade frequency follows the same pattern: 1,528 trades/day during extreme fear vs 260 trades/day during greed

2. **Profitability Patterns**
   - Average daily profits are highest during extreme fear periods ($52,793)
   - Win rates (percentage of profitable days) are actually highest during extreme greed periods (87.72%)
   - Risk-adjusted returns are best during extreme greed (0.021037)

3. **Statistical Correlations**
   - Sentiment vs Trading Volume: -0.274 (negative correlation)
   - Sentiment vs Trade Count: -0.247 (negative correlation)
   - Sentiment vs Profitability: -0.096 (slight negative correlation)

## Notebooks

### notebook_1.ipynb
Contains the main analysis including:
- Data loading and preprocessing
- Basic statistical analysis
- Initial visualizations
- Key findings summary

### notebook_2.ipynb
Contains advanced analysis including:
- Time series visualizations
- Correlation analysis
- Distribution analysis
- Risk-adjusted performance metrics

## Data Files

### fear_greed_index.csv
Bitcoin Fear & Greed Index data from February 2018 to May 2025

### historical_data.csv
Hyperliquid trader transaction data from December 2024 to April 2025

## Outputs

Visualization outputs from the analysis:
- trader_behavior_analysis.png
- advanced_trader_behavior_analysis.png

## Instructions

1. Run `notebook_1.ipynb` for the main analysis
2. Run `notebook_2.ipynb` for advanced analysis
3. View outputs in the `outputs/` directory
4. Generate `ds_report.pdf` with final summarized insights

## Requirements

- Python 3.x
- pandas
- numpy
- matplotlib
- seaborn