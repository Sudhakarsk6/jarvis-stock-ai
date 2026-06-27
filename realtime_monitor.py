import yfinance as yf
import pandas as pd
import time
from datetime import datetime, timedelta
from analyzer import StockAnalyzer
from technical_analysis import TechnicalAnalysis
from data_fetcher import DataFetcher
from config import RSI_PERIOD, MACD_FAST, MACD_SLOW, MACD_SIGNAL
from colorama import Fore, Back, Style, init
import threading
import json
import os

init(autoreset=True)

class RealtimeMonitor:
    """
    Real-time market monitoring system
    Tracks stocks and generates alerts
    """
    
    def __init__(self, symbol, capital=50000, check_interval=60):
        """
        Initialize real-time monitor
        
        Args:
            symbol: Stock ticker (e.g., 'RELIANCE.NS')
            capital: Trading capital
            check_interval: Seconds between checks (min: 60)
        """
        self.symbol = symbol
        self.capital = capital
        self.check_interval = max(60, check_interval)  # Min 60 seconds
        self.is_running = False
        self.previous_rsi = None
        self.previous_price = None
        self.previous_macd = None
        self.alert_history = []
        self.price_history = []
        self.tick_count = 0
        
    def fetch_live_price(self):
        """
        Fetch current live price
        """
        try:
            ticker = yf.Ticker(self.symbol)
            data = ticker.history(period='1d', interval='1m')
            
            if data.empty:
                return None
            
            current_price = data['Close'].iloc[-1]
            volume = data['Volume'].iloc[-1]
            high = data['High'].iloc[-1]
            low = data['Low'].iloc[-1]
            
            return {
                'price': current_price,
                'volume': volume,
                'high': high,
                'low': low,
                'timestamp': datetime.now()
            }
        
        except Exception as e:
            print(f"{Fore.RED}❌ Error fetching live price: {str(e)}{Style.RESET_ALL}")
            return None
    
    def analyze_quick(self):
        """
        Quick analysis of current market state
        """
        try:
            # Fetch intraday data (last 4 hours)
            data = yf.Ticker(self.symbol).history(period='1d', interval='5m')
            
            if data.empty or len(data) < 20:
                return None
            
            ta = TechnicalAnalysis()
            
            # Calculate indicators
            rsi = ta.calculate_rsi(data, RSI_PERIOD)
            macd, signal, histogram = ta.calculate_macd(data, MACD_FAST, MACD_SLOW, MACD_SIGNAL)
            ema_20 = ta.calculate_ema(data, 20)
            ema_50 = ta.calculate_ema(data, 50)
            
            current_price = data['Close'].iloc[-1]
            
            return {
                'current_price': current_price,
                'rsi': rsi.iloc[-1],
                'macd': macd.iloc[-1],
                'macd_signal': signal.iloc[-1],
                'histogram': histogram.iloc[-1],
                'ema_20': ema_20.iloc[-1],
                'ema_50': ema_50.iloc[-1],
                'trend': 'UP' if ema_20.iloc[-1] > ema_50.iloc[-1] else 'DOWN'
            }
        
        except Exception as e:
            print(f"{Fore.RED}❌ Analysis error: {str(e)}{Style.RESET_ALL}")
            return None
    
    def generate_alerts(self, analysis):
        """
        Generate trading alerts based on analysis
        """
        alerts = []
        
        if analysis is None:
            return alerts
        
        current_rsi = analysis['rsi']
        current_price = analysis['current_price']
        macd_histogram = analysis['histogram']
        trend = analysis['trend']
        
        # RSI Alerts
        if current_rsi > 80:
            alerts.append({
                'type': 'OVERBOUGHT',
                'severity': 'HIGH',
                'message': f"🔺 OVERBOUGHT: RSI {current_rsi:.1f} > 80",
                'action': 'SELL SIGNAL'
            })
        
        elif current_rsi < 20:
            alerts.append({
                'type': 'OVERSOLD',
                'severity': 'HIGH',
                'message': f"🔻 OVERSOLD: RSI {current_rsi:.1f} < 20",
                'action': 'BUY SIGNAL'
            })
        
        elif 70 < current_rsi <= 80:
            alerts.append({
                'type': 'NEAR_OVERBOUGHT',
                'severity': 'MEDIUM',
                'message': f"⚠️ RSI approaching overbought: {current_rsi:.1f}",
                'action': 'WATCH'
            })
        
        elif 20 <= current_rsi < 30:
            alerts.append({
                'type': 'NEAR_OVERSOLD',
                'severity': 'MEDIUM',
                'message': f"⚠️ RSI approaching oversold: {current_rsi:.1f}",
                'action': 'WATCH'
            })
        
        # MACD Alerts
        if self.previous_macd is not None:
            if self.previous_macd < 0 and macd_histogram > 0:
                alerts.append({
                    'type': 'MACD_BULLISH',
                    'severity': 'HIGH',
                    'message': f"📈 MACD Bullish Crossover",
                    'action': 'BUY SIGNAL'
                })
            
            elif self.previous_macd > 0 and macd_histogram < 0:
                alerts.append({
                    'type': 'MACD_BEARISH',
                    'severity': 'HIGH',
                    'message': f"📉 MACD Bearish Crossover",
                    'action': 'SELL SIGNAL'
                })
        
        # Price Movement Alerts
        if self.previous_price is not None:
            price_change = ((current_price - self.previous_price) / self.previous_price) * 100
            
            if price_change > 2:
                alerts.append({
                    'type': 'PRICE_UP',
                    'severity': 'MEDIUM',
                    'message': f"📈 Price up {price_change:.2f}%",
                    'action': 'MONITOR'
                })
            
            elif price_change < -2:
                alerts.append({
                    'type': 'PRICE_DOWN',
                    'severity': 'MEDIUM',
                    'message': f"📉 Price down {price_change:.2f}%",
                    'action': 'MONITOR'
                })
        
        # Trend Alerts
        if trend == 'UP':
            alerts.append({
                'type': 'UPTREND',
                'severity': 'LOW',
                'message': f"📈 Uptrend Active",
                'action': 'BULLISH'
            })
        elif trend == 'DOWN':
            alerts.append({
                'type': 'DOWNTREND',
                'severity': 'LOW',
                'message': f"📉 Downtrend Active",
                'action': 'BEARISH'
            })
        
        self.previous_rsi = current_rsi
        self.previous_price = current_price
        self.previous_macd = macd_histogram
        
        return alerts
    
    def display_alert(self, alert):
        """
        Display alert with color coding
        """
        severity_color = {
            'HIGH': Fore.RED,
            'MEDIUM': Fore.YELLOW,
            'LOW': Fore.GREEN
        }
        
        color = severity_color.get(alert['severity'], Fore.WHITE)
        
        print(f"{color}[{datetime.now().strftime('%H:%M:%S')}] {alert['message']} | Action: {alert['action']}{Style.RESET_ALL}")
    
    def save_to_log(self, data):
        """
        Save monitoring data to log file
        """
        log_file = f"monitor_{self.symbol.replace('.', '_')}.json"
        
        try:
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            else:
                logs = []
            
            logs.append(data)
            
            # Keep only last 1000 entries
            if len(logs) > 1000:
                logs = logs[-1000:]
            
            with open(log_file, 'w') as f:
                json.dump(logs, f)
        
        except Exception as e:
            pass  # Silently fail on logging errors
    
    def run_once(self):
        """
        Run single monitoring cycle
        """
        print(f"{Fore.CYAN}[{datetime.now().strftime('%H:%M:%S')}] Checking {self.symbol}...{Style.RESET_ALL}")
        
        # Get live price
        live_data = self.fetch_live_price()
        if live_data:
            print(f"{Fore.YELLOW}Current Price: ₹{live_data['price']:.2f}{Style.RESET_ALL}")
        
        # Quick analysis
        analysis = self.analyze_quick()
        if analysis:
            print(f"{Fore.CYAN}RSI: {analysis['rsi']:.1f} | Trend: {analysis['trend']}{Style.RESET_ALL}")
            
            # Generate alerts
            alerts = self.generate_alerts(analysis)
            
            if alerts:
                print(f"{Fore.GREEN}\n{len(alerts)} Alert(s):{Style.RESET_ALL}")
                for alert in alerts:
                    self.display_alert(alert)
                    self.alert_history.append({
                        'timestamp': datetime.now(),
                        'alert': alert
                    })
                print()
            else:
                print(f"{Fore.YELLOW}No alerts{Style.RESET_ALL}\n")
            
            # Save to log
            self.save_to_log({
                'timestamp': datetime.now().isoformat(),
                'symbol': self.symbol,
                'price': analysis['current_price'],
                'rsi': analysis['rsi'],
                'alerts': len(alerts)
            })
    
    def run_continuous(self, duration_hours=8):
        """
        Run continuous monitoring for specified hours
        
        Args:
            duration_hours: How long to monitor (market hours = ~7.5)
        """
        self.is_running = True
        start_time = time.time()
        duration_seconds = duration_hours * 3600
        
        print(f"{Back.CYAN}{Fore.BLACK} JARVIS REAL-TIME MONITOR {Style.RESET_ALL}")
        print(f"{Fore.CYAN}Symbol: {self.symbol}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Duration: {duration_hours} hours{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Check Interval: {self.check_interval} seconds{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Starting at: {datetime.now().strftime('%H:%M:%S')}{Style.RESET_ALL}\n")
        
        try:
            while self.is_running and (time.time() - start_time) < duration_seconds:
                self.tick_count += 1
                print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}TICK #{self.tick_count} | {datetime.now().strftime('%H:%M:%S')}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
                
                self.run_once()
                
                elapsed = time.time() - start_time
                remaining = duration_seconds - elapsed
                
                if remaining > 0:
                    wait_time = min(self.check_interval, remaining)
                    print(f"{Fore.YELLOW}Next check in {wait_time:.0f} seconds...{Style.RESET_ALL}\n")
                    time.sleep(wait_time)
            
            self.print_session_summary()
        
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}⚡ Monitoring stopped by user{Style.RESET_ALL}\n")
            self.print_session_summary()
        
        finally:
            self.is_running = False
    
    def print_session_summary(self):
        """
        Print monitoring session summary
        """
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"SESSION SUMMARY{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        
        print(f"📄 Symbol: {self.symbol}")
        print(f"⏳ Total Ticks: {self.tick_count}")
        print(f"🚨 Total Alerts: {len(self.alert_history)}")
        
        if self.alert_history:
            print(f"\n{Fore.GREEN}Alert Breakdown:{Style.RESET_ALL}")
            alert_types = {}
            for entry in self.alert_history:
                alert_type = entry['alert']['type']
                alert_types[alert_type] = alert_types.get(alert_type, 0) + 1
            
            for alert_type, count in alert_types.items():
                print(f"  {alert_type}: {count}")
        
        print(f"\n{Fore.YELLOW}End Time: {datetime.now().strftime('%H:%M:%S')}{Style.RESET_ALL}\n")
