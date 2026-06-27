import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
YFINANCE_TIMEOUT = 10
RETRY_ATTEMPTS = 3

# Analysis Configuration
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
EMA_SHORT = 20
EMA_LONG = 50
BB_PERIOD = 20
BB_STD_DEV = 2

# Risk Management
MAX_RISK_PERCENTAGE = 2.0  # 2% of capital
MIN_CONFIDENCE = 70  # Don't trade below 70% confidence

# Capital Amounts (in INR)
CAPITAL_LEVELS = {
    'micro': 500,
    'small': 5000,
    'medium': 50000,
    'large': 100000,
    'xlarge': 1000000
}

# Trading Styles
TRADING_STYLES = {
    'intraday': 'Intraday Trading (same day)',
    'swing': 'Swing Trading (3-10 days)',
    'positional': 'Positional Trading (1-3 months)',
    'longterm': 'Long-term Investing (1+ years)'
}

# Risk Levels
RISK_LEVELS = {
    'very_low': 'Very Low (Conservative)',
    'low': 'Low',
    'medium': 'Medium',
    'high': 'High',
    'extreme': 'Extreme (Avoid)'
}
