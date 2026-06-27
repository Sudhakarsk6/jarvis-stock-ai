import yfinance as yf
import pandas as pd
from config import YFINANCE_TIMEOUT, RETRY_ATTEMPTS
import time

class DataFetcher:
    """Fetch stock data from Yahoo Finance"""
    
    @staticmethod
    def get_stock_data(symbol, period='1y', interval='1d'):
        """
        Fetch stock historical data
        
        Args:
            symbol: Stock ticker (e.g., 'RELIANCE.NS' for NSE)
            period: '1y', '6mo', '3mo', '1mo', '1d'
            interval: '1d', '1h', '15m'
        
        Returns:
            DataFrame with OHLCV data
        """
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval=interval)
            
            if data.empty:
                print(f"❌ No data found for {symbol}")
                return None
            
            return data
        
        except Exception as e:
            print(f"❌ Error fetching data: {str(e)}")
            return None
    
    @staticmethod
    def get_stock_info(symbol):
        """
        Fetch fundamental stock information
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return {
                'name': info.get('longName', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'pe_ratio': info.get('trailingPE', 'N/A'),
                'pb_ratio': info.get('priceToBook', 'N/A'),
                'market_cap': info.get('marketCap', 'N/A'),
                'dividend_yield': info.get('dividendYield', 'N/A'),
                'profit_margin': info.get('profitMargins', 'N/A'),
                'roe': info.get('returnOnEquity', 'N/A'),
                '52w_high': info.get('fiftyTwoWeekHigh', 'N/A'),
                '52w_low': info.get('fiftyTwoWeekLow', 'N/A'),
                'current_price': info.get('currentPrice', 'N/A')
            }
        
        except Exception as e:
            print(f"❌ Error fetching info: {str(e)}")
            return None
