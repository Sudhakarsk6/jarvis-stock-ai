# 🤖 JARVIS STOCK AI

**Elite AI Financial Analyst for Indian Stock Market**

Professional stock analysis system combining technical, fundamental, and risk analysis with zero configuration needed.

---

## ✨ Features

✅ **Technical Analysis**
- RSI, MACD, Bollinger Bands, EMA, SMA
- Support/Resistance Detection
- Trend Analysis (Uptrend/Downtrend/Sideways)
- Volume Analysis
- ATR, Fibonacci, Candlestick Patterns

✅ **Fundamental Analysis**
- PE, PB, ROE, Profit Margins
- Valuation Assessment
- Business Quality Scoring
- Market Cap & Dividend Data

✅ **Risk Management**
- Risk Level Classification
- Position Sizing (based on capital)
- Confidence Scoring (0-100%)
- Risk/Reward Ratio Calculation

✅ **Professional Reports**
- Color-coded output
- Detailed trade recommendations
- Warning alerts
- Entry/Exit strategies

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python main.py
```

### 3. Follow Interactive Menu

```
Enter Stock Symbol (NSE format): RELIANCE.NS
Enter Capital (in ₹): 50000
Select Trading Style: 2 (Swing Trading)
```

---

## 📊 Supported Stock Formats

**NSE (National Stock Exchange):**
- `RELIANCE.NS`
- `TCS.NS`
- `INFY.NS`
- `HDFC.NS`
- `ICICIBANK.NS`
- `LT.NS`

**BSE (Bombay Stock Exchange):**
- `RELIANCE.BO`
- `TCS.BO`

---

## 💰 Supported Capital Amounts

- ₹500 (Micro)
- ₹5,000 (Small)
- ₹50,000 (Medium)
- ₹100,000 (Large)
- ₹1,000,000+ (XL)

*Position sizing automatically adjusts based on your capital.*

---

## 🎯 Trading Styles Supported

1. **Intraday Trading** - Same day trading
2. **Swing Trading** - 3-10 days holding
3. **Positional Trading** - 1-3 months
4. **Long-term Investing** - 1+ years

---

## 📈 Analysis Output

The system provides:

### Recommendation
- **BUY** - Strong buy signal (Confidence > 75%)
- **WAIT** - Hold/Monitor (60-75% confidence)
- **SELL** - Bearish signal (< 40% confidence)
- **AVOID** - Extreme risk (Risk level: EXTREME)

### Risk Levels
- 🟢 **Very Low** - Conservative play
- 🟢 **Low** - Safe entry
- 🟡 **Medium** - Moderate risk
- 🔴 **High** - Risky
- 🟣 **Extreme** - Avoid completely

### Trade Details
- Current Price
- Entry Price
- Stop Loss
- Target 1, Target 2, Target 3
- Position Size (₹)
- Risk/Reward Ratio
- Confidence Score

---

## 🔧 Configuration

Edit `config.py` to customize:

```python
RSI_PERIOD = 14          # RSI calculation period
MACD_FAST = 12          # MACD fast EMA
MACD_SLOW = 26          # MACD slow EMA
EMA_SHORT = 20          # Short-term EMA
EMA_LONG = 50           # Long-term EMA
MAX_RISK_PERCENTAGE = 2 # Risk per trade (% of capital)
MIN_CONFIDENCE = 70     # Minimum confidence to trade
```

---

## 📝 Example Analysis Flow

1. **Input:** Stock symbol, capital, trading style
2. **Fetch:** Real-time data from Yahoo Finance
3. **Calculate:** All technical indicators
4. **Analyze:** Fundamental metrics
5. **Assess:** Risk levels
6. **Generate:** Professional recommendation
7. **Output:** Color-coded report with actionable insights

---

## ⚠️ Disclaimer

⚡ **This is AI analysis, NOT financial advice.**

- Always consult a licensed financial advisor
- Past performance ≠ Future results
- Trading involves risk of loss
- Never risk more than you can afford to lose
- This system is for educational purposes

---

## 🛠️ Troubleshooting

### "No data found for symbol"
- ❌ Wrong symbol format
- ✅ Use NSE format: `RELIANCE.NS`
- ✅ Check if stock exists

### "Connection error"
- ❌ No internet connection
- ✅ Check your network
- ✅ Yahoo Finance might be temporarily down

### "ValueError in calculations"
- ✅ This is normal for newly listed stocks
- ✅ Try a different stock with more data

---

## 📚 Technical Stack

- **yfinance** - Stock data fetching
- **pandas** - Data processing
- **numpy** - Calculations
- **ta** - Technical analysis
- **colorama** - Terminal colors
- **tabulate** - Report formatting

---

## 🎓 Learning Resources

- RSI: Relative Strength Index (0-100 scale)
- MACD: Moving Average Convergence Divergence
- Bollinger Bands: Volatility indicator
- Support: Price level where buying pressure increases
- Resistance: Price level where selling pressure increases

---

## 💡 Pro Tips

1. **Never ignore risk warnings** - System flags extreme risk for a reason
2. **Confidence > 75%** - Only trade recommendations with high confidence
3. **Use stop loss** - Always set stops at suggested levels
4. **Position size matters** - Risk only 2% per trade
5. **Multiple timeframes** - Check analysis on different charts
6. **News matters** - Check company news before trading
7. **Patience pays** - Wait for high-confidence setups

---

## 📞 Support

If you encounter issues:

1. Ensure all dependencies are installed: `pip install -r requirements.txt`
2. Check stock symbol format (use NSE: `.NS`)
3. Verify internet connection
4. Try a different stock

---

## 📜 License

Educational use only. Not for commercial purposes without modification.

---

**Built with ⚡ by JARVIS Stock AI**

*"Logic, Data, and Probability over Emotions and Hype."*
