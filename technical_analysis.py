import pandas as pd
import numpy as np
from config import RSI_PERIOD, MACD_FAST, MACD_SLOW, MACD_SIGNAL, EMA_SHORT, EMA_LONG, BB_PERIOD, BB_STD_DEV

class TechnicalAnalysis:
    """Technical analysis calculations"""
    
    @staticmethod
    def calculate_rsi(data, period=RSI_PERIOD):
        """Calculate Relative Strength Index"""
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    @staticmethod
    def calculate_macd(data, fast=MACD_FAST, slow=MACD_SLOW, signal=MACD_SIGNAL):
        """Calculate MACD"""
        ema_fast = data['Close'].ewm(span=fast).mean()
        ema_slow = data['Close'].ewm(span=slow).mean()
        macd = ema_fast - ema_slow
        signal_line = macd.ewm(span=signal).mean()
        histogram = macd - signal_line
        return macd, signal_line, histogram
    
    @staticmethod
    def calculate_bollinger_bands(data, period=BB_PERIOD, std_dev=BB_STD_DEV):
        """Calculate Bollinger Bands"""
        sma = data['Close'].rolling(window=period).mean()
        std = data['Close'].rolling(window=period).std()
        upper_band = sma + (std * std_dev)
        lower_band = sma - (std * std_dev)
        return upper_band, sma, lower_band
    
    @staticmethod
    def calculate_ema(data, period):
        """Calculate Exponential Moving Average"""
        return data['Close'].ewm(span=period).mean()
    
    @staticmethod
    def calculate_sma(data, period):
        """Calculate Simple Moving Average"""
        return data['Close'].rolling(window=period).mean()
    
    @staticmethod
    def calculate_atr(data, period=14):
        """Calculate Average True Range"""
        data['H-L'] = data['High'] - data['Low']
        data['H-PC'] = abs(data['High'] - data['Close'].shift())
        data['L-PC'] = abs(data['Low'] - data['Close'].shift())
        tr = data[['H-L', 'H-PC', 'L-PC']].max(axis=1)
        atr = tr.rolling(period).mean()
        return atr
    
    @staticmethod
    def get_trend(ema_short, ema_long):
        """Determine trend: UPTREND, DOWNTREND, SIDEWAYS"""
        last_short = ema_short.iloc[-1]
        last_long = ema_long.iloc[-1]
        
        if last_short > last_long * 1.02:
            return 'UPTREND'
        elif last_short < last_long * 0.98:
            return 'DOWNTREND'
        else:
            return 'SIDEWAYS'
    
    @staticmethod
    def analyze_support_resistance(data, lookback=20):
        """Find support and resistance levels"""
        recent_data = data.tail(lookback)
        
        support = recent_data['Low'].min()
        resistance = recent_data['High'].max()
        current_price = data['Close'].iloc[-1]
        
        return support, resistance, current_price
    
    @staticmethod
    def detect_candlestick_pattern(data):
        """Simple candlestick pattern detection"""
        recent = data.tail(3)
        
        last = recent.iloc[-1]
        prev = recent.iloc[-2]
        
        body = abs(last['Close'] - last['Open'])
        wick = last['High'] - last['Low']
        
        pattern = 'NEUTRAL'
        
        # Bullish patterns
        if last['Close'] > last['Open'] and last['Close'] > prev['Close']:
            if body > wick * 0.5:
                pattern = 'BULLISH_CANDLE'
        
        # Bearish patterns
        elif last['Close'] < last['Open'] and last['Close'] < prev['Close']:
            if body > wick * 0.5:
                pattern = 'BEARISH_CANDLE'
        
        return pattern
