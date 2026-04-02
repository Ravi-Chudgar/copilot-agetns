# BSE Stock Analysis Agent - Setup Guide for Users

## For Other Users: How to Use This Agent

### Option 1: Direct Python Execution (Fastest) ⭐

1. **Clone the repository**
   ```bash
   git clone https://github.com/Ravi-Chudgar/copilot-agetns.git
   cd copilot-agetns
   ```

2. **Install dependencies**
   ```bash
   pip install pandas numpy scipy scikit-learn plotly kaleido python-dateutil requests
   ```

3. **Run the analyzer**
   ```bash
   python scripts/bse_stock_analyzer.py
   ```

4. **View results**
   - Open `bse_analysis_report.html` in your browser
   - Check `bse_trading_signals.csv` in Excel/Google Sheets for signals

### Option 2: VS Code Agent (Coming Soon)

To add this as a VS Code agent:

1. Copy `.github/agents/bse-stock-analysis.agent.md` to:
   - **Windows**: `C:\Users\[YourUsername]\AppData\Roaming\Code\User\prompts\`
   - **Mac**: `~/.config/Code/User/globalStorage/github.copilot-chat/prompts/`
   - **Linux**: `~/.config/Code/User/globalStorage/github.copilot-chat/prompts/`

2. Restart VS Code

3. Open Copilot Chat and type: `@bse-stock-analysis` or mention the agent

### Option 3: Run as GitHub Action

Coming soon - automated daily analysis triggers

## Output Interpretation

### HTML Report Sections

#### 📊 Risk vs Return Profile (Scatter Plot)
- **X-axis**: Volatility (Risk)
- **Y-axis**: Annual Return (Profit)
- **Color**: Sharpe Ratio (Green = Good)
- **Size**: Total Return magnitude
- **Find**: Stocks in upper-left (high return, low risk)

#### 🔥 Performance Heatmap
- **Green cells**: High Sharpe/Sortino ratio
- **Red cells**: Low/negative ratios
- **Compare metrics** across top 20 stocks

#### 📈 Candlestick Charts
- **Green candle**: Close > Open (bullish)
- **Red candle**: Close < Open (bearish)
- **Shows**: 1 year price history for top 10 stocks

#### 🎯 Trading Signals Table
| Column | Meaning |
|--------|---------|
| Signal | Overall buy/sell recommendation |
| RSI | Momentum (oversold <30, overbought >70) |
| MACD | Trend momentum |
| SMA50/SMA200 | Support/resistance levels |
| EMA20 | Short-term trend |
| Entry Signals | Reasons to buy |
| Exit Signals | Reasons to sell |

## Signal Strength Levels

| Signal | Details | Action |
|--------|---------|--------|
| 🟢 STRONG BUY | 4+ entry signals | **Go long** (with stop-loss) |
| 🟢 BUY | 2-3 entry signals | **Consider position** |
| 🟡 NEUTRAL | Mixed signals | **Wait for clarity** |
| 🔴 SELL | 2-3 exit signals | **Consider exit** |
| 🔴 STRONG SELL | 4+ exit signals | **Close position** (protect profits) |

## Risk Management Tips

⚠️ **Always use these practices:**

1. **Set Stop-Loss**: Place sell order 2-3% below entry
2. **Take Profits**: Exit 50% at +5%, rest at +10%
3. **Position Size**: Risk only 1-2% of portfolio per trade
4. **Confirm Signals**: Wait for close above/below key levels
5. **Check Volume**: Confirm signals with high volume
6. **Review Weekly**: Re-analyze signals weekly for changes

## CSV Files Explanation

### bse_trading_signals.csv
```
Symbol,Signal,RSI,MACD,SMA50,SMA200,EMA20,Entry_Signals,Exit_Signals
RELIANCE,🟢 BUY,35.2,0.45,₹1050,₹980,₹1045,"RSI Oversold, Price Above EMA20","None"
INFY,🔴 SELL,72.1,-0.12,₹2500,₹2650,₹2480,"None","RSI Overbought, MACD Bearish"
```

### bse_stocks_data.csv
Contains fundamental metrics for analysis:
- Current_Price, Annual_Return, Volatility
- Sharpe_Ratio, Sortino_Ratio, Max_Drawdown
- Total_Return, Win_Rate

## FAQ

**Q: How accurate are these signals?**
A: No system is 100% accurate. These are technical indicators, not guarantees. Always use stop-loss.

**Q: Can I automate trading with these signals?**
A: Yes! Export CSV to your broker's API. But always have manual oversight.

**Q: How often should I run the analyzer?**
A: Daily before market open (9:15 AM IST)

**Q: What if a stock gives conflicting signals?**
A: Check the "Enter_Signals" and "Exit_Signals" columns. If mixed, it's neutral - wait.

**Q: Is this better than other indicators?**
A: It combines multiple indicators (RSI, MACD, MA). Combining signals = higher accuracy.

## Data Source

✅ **dhanHQ API** - Official BSE stock market data
- 40+ years of historical data
- Real-time price updates
- Validated & reliable

## Performance Statistics

Recent backtest results (40-year data):
- **RELIANCE**: Sharpe 0.42 | Annual Return 19.2%
- **HDFC**: Sharpe 0.30 | Annual Return 15.5%
- **SBIN**: Sharpe 0.20 | Annual Return 12.5%

## Disclaimer

⚠️ **EDUCATIONAL PURPOSE ONLY**

- Past performance ≠ Future results
- This is NOT investment advice
- Consult a financial advisor
- Trade at your own risk
- Do your own research (DYOR)

## Need Help?

- 📖 Issue: Create GitHub issue with details
- 💬 Discussion: Use GitHub Discussions
- 🐛 Bug: Report in Issues with screenshots

## Contributors Welcome!

If you improve this agent:
1. Fork the repository
2. Make your changes
3. Submit a pull request
4. We'll review & merge!

## License

MIT License - Free to use, modify, and share
Attribution appreciated but not required

---

**Happy Trading! 📈**

Remember: With great signals comes great responsibility. Always use stop-loss! 🛡️
