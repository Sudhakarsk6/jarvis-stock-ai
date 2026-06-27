import pandas as pd
import numpy as np
from technical_analysis import TechnicalAnalysis
from data_fetcher import DataFetcher
from config import RSI_PERIOD, MACD_FAST, MACD_SLOW, MACD_SIGNAL
from datetime import datetime
from colorama import Fore, Style

class IntradayAnalyzer:
    """
    Specialized analyzer for intraday trading (5-minute charts)
    Generates buy/sell signals for same-day trading
    """
    
    def __init__(self, symbol):
        self.symbol = symbol
        self.ta = TechnicalAnalysis()
    
    def get_intraday_data(self, period='1d', interval='5m'):
        """
        Fetch 5-minute intraday data
        """
        try:
            df = DataFetcher.get_stock_data(self.symbol, period=period, interval=interval)
            return df
        except Exception as e:
            print(f"{Fore.RED}✗ Error fetching intraday data: {str(e)}{Style.RESET_ALL}")
            return None
    
    def analyze_buy_signal(self, data=None):
        """
        Analyze intraday data for BUY signals
        Returns comprehensive buy suggestion
        """
        if data is None:
            data = self.get_intraday_data()
        
        if data is None or len(data) < 50:
            return None
        
        try:
            # Calculate all indicators
            rsi = self.ta.calculate_rsi(data, RSI_PERIOD)
            macd, signal, histogram = self.ta.calculate_macd(data, MACD_FAST, MACD_SLOW, MACD_SIGNAL)
            ema_20 = self.ta.calculate_ema(data, 20)
            ema_50 = self.ta.calculate_ema(data, 50)
            bollinger_up, bollinger_mid, bollinger_low = self.ta.calculate_bollinger_bands(data)
            atr = self.ta.calculate_atr(data)
            
            # Current values
            current_price = data['Close'].iloc[-1]
            current_rsi = rsi.iloc[-1]
            current_macd = macd.iloc[-1]
            current_histogram = histogram.iloc[-1]
            current_ema_20 = ema_20.iloc[-1]
            current_ema_50 = ema_50.iloc[-1]
            current_atr = atr.iloc[-1]
            
            # Previous values (for crossovers)
            prev_histogram = histogram.iloc[-2] if len(histogram) > 1 else 0
            prev_rsi = rsi.iloc[-2] if len(rsi) > 1 else 0
            
            # Support and Resistance
            support = data['Low'].tail(20).min()
            resistance = data['High'].tail(20).max()
            
            # Volume analysis
            avg_volume = data['Volume'].tail(20).mean()
            current_volume = data['Volume'].iloc[-1]
            volume_strength = 'STRONG' if current_volume > avg_volume * 1.5 else 'NORMAL'
            
            # Trend determination
            if current_ema_20 > current_ema_50:
                trend = 'UPTREND'
                trend_signal = 'BULLISH'
            elif current_ema_20 < current_ema_50 * 0.98:
                trend = 'DOWNTREND'
                trend_signal = 'BEARISH'
            else:
                trend = 'SIDEWAYS'
                trend_signal = 'NEUTRAL'
            
            # MACD signal
            if prev_histogram < 0 and current_histogram > 0:
                macd_signal = 'BULLISH_CROSSOVER'
            elif prev_histogram > 0 and current_histogram < 0:
                macd_signal = 'BEARISH_CROSSOVER'
            else:
                macd_signal = 'BULLISH' if current_histogram > 0 else 'BEARISH'
            
            # RSI signal
            if current_rsi < 30:
                rsi_signal = 'OVERSOLD_BUY'
            elif current_rsi > 70:
                rsi_signal = 'OVERBOUGHT_SELL'
            elif current_rsi < 50:
                rsi_signal = 'WEAK'
            else:
                rsi_signal = 'STRONG'
            
            # Calculate buy score (0-100)
            buy_score = self._calculate_buy_score(
                trend_signal, macd_signal, rsi_signal, 
                current_rsi, current_ema_20, current_ema_50, 
                volume_strength, current_atr
            )
            
            # Risk level
            risk_level = self._assess_risk_level(current_rsi, buy_score, trend_signal)
            
            # Generate entry and targets
            entry_price = self._calculate_entry_price(current_price, support, current_atr)
            target_1 = current_price + (current_atr * 1.5)
            target_2 = current_price + (current_atr * 3)
            target_3 = current_price + (current_atr * 5)
            stop_loss = support - (current_atr * 0.5)
            
            # Position sizing (for ₹50,000 capital)
            capital = 50000
            risk_amount = capital * 0.02  # 2% risk
            loss_per_share = current_price - stop_loss
            position_size = risk_amount / loss_per_share if loss_per_share > 0 else 0
            
            # Risk/Reward ratio
            potential_profit = target_2 - entry_price
            potential_loss = entry_price - stop_loss
            risk_reward = round(potential_profit / potential_loss, 2) if potential_loss > 0 else 0
            
            # Reasons to buy
            reasons = self._generate_reasons(trend_signal, macd_signal, rsi_signal, volume_strength)
            
            # Risk factors
            risks = self._generate_risks(current_rsi, buy_score, trend_signal)
            
            # Recommendation
            if buy_score >= 75:
                recommendation = 'BUY'
            elif buy_score >= 60:
                recommendation = 'WAIT'
            elif buy_score >= 40:
                recommendation = 'HOLD'
            else:
                recommendation = 'AVOID'
            
            return {
                'symbol': self.symbol,
                'timestamp': datetime.now().strftime('%H:%M:%S'),
                'current_price': round(current_price, 2),
                'action': recommendation,
                'confidence': buy_score,
                'risk_level': risk_level,
                'entry_price': round(entry_price, 2),
                'buy_zone_start': round(support, 2),
                'buy_zone_end': round(current_price + current_atr, 2),
                'target_1': round(target_1, 2),
                'target_1_profit': round(target_1 - entry_price, 2),
                'target_2': round(target_2, 2),
                'target_2_profit': round(target_2 - entry_price, 2),
                'target_3': round(target_3, 2),
                'target_3_profit': round(target_3 - entry_price, 2),
                'stop_loss': round(stop_loss, 2),
                'max_loss': round(entry_price - stop_loss, 2),
                'risk_reward': risk_reward,
                'trend': trend,
                'trend_signal': trend_signal,
                'rsi': round(current_rsi, 1),
                'rsi_signal': rsi_signal,
                'macd_signal': macd_signal,
                'volume_strength': volume_strength,
                'ema_status': f'EMA 20: {round(current_ema_20, 2)} | EMA 50: {round(current_ema_50, 2)}',
                'support': round(support, 2),
                'resistance': round(resistance, 2),
                'holding_time': '30-60 minutes',
                'exit_before': '3:15 PM IST',
                'position_size': round(position_size, 0),
                'reasons': reasons,
                'risks': risks,
                'atr': round(current_atr, 2)
            }
        
        except Exception as e:
            print(f"{Fore.RED}✗ Analysis error: {str(e)}{Style.RESET_ALL}")
            return None
    
    def _calculate_buy_score(self, trend, macd_signal, rsi_signal, rsi, ema_20, ema_50, volume, atr):
        """
        Calculate buy score (0-100)
        """
        score = 50  # Base score
        
        # Trend (20 points)
        if trend == 'BULLISH':
            score += 20
        elif trend == 'BEARISH':
            score -= 20
        
        # MACD (15 points)
        if macd_signal == 'BULLISH_CROSSOVER':
            score += 15
        elif macd_signal == 'BULLISH':
            score += 10
        elif macd_signal == 'BEARISH_CROSSOVER':
            score -= 15
        elif macd_signal == 'BEARISH':
            score -= 10
        
        # RSI (15 points)
        if rsi_signal == 'OVERSOLD_BUY':
            score += 15
        elif rsi_signal == 'STRONG':
            score += 10
        elif rsi_signal == 'WEAK':
            score -= 5
        elif rsi_signal == 'OVERBOUGHT_SELL':
            score -= 15
        
        # Volume (10 points)
        if volume == 'STRONG':
            score += 10
        
        # EMA crossover
        if ema_20 > ema_50 * 1.01:
            score += 10
        elif ema_20 < ema_50 * 0.99:
            score -= 10
        
        return max(0, min(100, score))
    
    def _assess_risk_level(self, rsi, score, trend):
        """
        Assess risk level
        """
        if score >= 80:
            if rsi > 75:
                return 'HIGH'
            return 'MEDIUM'
        elif score >= 60:
            return 'MEDIUM'
        elif score >= 40:
            return 'HIGH'
        else:
            return 'EXTREME'
    
    def _calculate_entry_price(self, current_price, support, atr):
        """
        Calculate ideal entry price
        """
        # Entry slightly above support or on pullback
        entry = max(support + (atr * 0.2), current_price - (atr * 0.5))
        return entry
    
    def _generate_reasons(self, trend, macd_signal, rsi_signal, volume):
        """
        Generate reasons to buy
        """
        reasons = []
        
        if trend == 'BULLISH':
            reasons.append('✅ Strong uptrend active (EMA 20 > EMA 50)')
        
        if macd_signal == 'BULLISH_CROSSOVER':
            reasons.append('✅ MACD bullish crossover signal')
        elif macd_signal == 'BULLISH':
            reasons.append('✅ MACD showing bullish momentum')
        
        if rsi_signal == 'OVERSOLD_BUY':
            reasons.append('✅ RSI oversold - reversal opportunity')
        elif rsi_signal == 'STRONG':
            reasons.append('✅ RSI in healthy buying zone (50-70)')
        
        if volume == 'STRONG':
            reasons.append('✅ Strong volume confirming move')
        
        return '\n'.join(reasons) if reasons else 'Limited buy signals'
    
    def _generate_risks(self, rsi, score, trend):
        """
        Generate risk factors
        """
        risks = []
        
        if rsi > 75:
            risks.append('⚠️  RSI overbought - possible pullback')
        
        if score < 50:
            risks.append('⚠️  Low confidence signal')
        
        if trend == 'BEARISH':
            risks.append('⚠️  Trading against downtrend')
        
        if rsi < 30:
            risks.append('⚠️  Extreme oversold - stop loss crucial')
        
        return '\n'.join(risks) if risks else 'No major risks identified'
    
    def check_for_buy_opportunity(self):
        """
        Quick check if there's a buy opportunity right now
        Returns True/False and suggestion data
        """
        suggestion = self.analyze_buy_signal()
        
        if suggestion is None:
            return False, None
        
        is_buy_signal = suggestion['confidence'] >= 70 and suggestion['action'] == 'BUY'
        
        return is_buy_signal, suggestion
