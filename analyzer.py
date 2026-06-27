from data_fetcher import DataFetcher
from technical_analysis import TechnicalAnalysis
from fundamental_analysis import FundamentalAnalysis
from config import MIN_CONFIDENCE, MAX_RISK_PERCENTAGE, CAPITAL_LEVELS
import pandas as pd
import numpy as np

class StockAnalyzer:
    """Main analyzer combining all analyses"""
    
    def __init__(self, symbol, capital=50000, trading_style='swing'):
        self.symbol = symbol
        self.capital = capital
        self.trading_style = trading_style
        self.data = None
        self.info = None
    
    def analyze(self):
        """Run complete analysis"""
        print(f"\n🔍 Analyzing {self.symbol}...\n")
        
        # Fetch data
        self.data = DataFetcher.get_stock_data(self.symbol, period='1y')
        self.info = DataFetcher.get_stock_info(self.symbol)
        
        if self.data is None or self.data.empty:
            return {'error': 'Unable to fetch data'}
        
        # Technical Analysis
        tech_analysis = self._technical_analysis()
        
        # Fundamental Analysis
        fund_analysis = self._fundamental_analysis()
        
        # Risk Analysis
        risk_analysis = self._risk_analysis(tech_analysis, fund_analysis)
        
        # Generate Recommendation
        recommendation = self._generate_recommendation(tech_analysis, fund_analysis, risk_analysis)
        
        return {
            'symbol': self.symbol,
            'technical': tech_analysis,
            'fundamental': fund_analysis,
            'risk': risk_analysis,
            'recommendation': recommendation
        }
    
    def _technical_analysis(self):
        """Perform technical analysis"""
        ta = TechnicalAnalysis()
        
        rsi = ta.calculate_rsi(self.data)
        macd, signal, histogram = ta.calculate_macd(self.data)
        ema_short = ta.calculate_ema(self.data, 20)
        ema_long = ta.calculate_ema(self.data, 50)
        upper_bb, middle_bb, lower_bb = ta.calculate_bollinger_bands(self.data)
        atr = ta.calculate_atr(self.data)
        
        support, resistance, current_price = ta.analyze_support_resistance(self.data)
        trend = ta.get_trend(ema_short, ema_long)
        pattern = ta.detect_candlestick_pattern(self.data)
        
        # Calculate signals
        rsi_signal = 'OVERBOUGHT' if rsi.iloc[-1] > 70 else 'OVERSOLD' if rsi.iloc[-1] < 30 else 'NEUTRAL'
        macd_signal = 'BULLISH' if histogram.iloc[-1] > 0 else 'BEARISH'
        
        volume = self.data['Volume'].iloc[-1]
        avg_volume = self.data['Volume'].rolling(20).mean().iloc[-1]
        volume_strength = 'STRONG' if volume > avg_volume * 1.2 else 'NORMAL'
        
        return {
            'current_price': round(current_price, 2),
            'trend': trend,
            'rsi': round(rsi.iloc[-1], 2),
            'rsi_signal': rsi_signal,
            'macd': round(macd.iloc[-1], 4),
            'macd_signal': macd_signal,
            'support': round(support, 2),
            'resistance': round(resistance, 2),
            'ema_20': round(ema_short.iloc[-1], 2),
            'ema_50': round(ema_long.iloc[-1], 2),
            'bb_upper': round(upper_bb.iloc[-1], 2),
            'bb_lower': round(lower_bb.iloc[-1], 2),
            'atr': round(atr.iloc[-1], 2),
            'candlestick': pattern,
            'volume_strength': volume_strength
        }
    
    def _fundamental_analysis(self):
        """Perform fundamental analysis"""
        if not self.info:
            return {'status': 'Data unavailable'}
        
        fa = FundamentalAnalysis()
        
        pe = self.info.get('pe_ratio', 0)
        pb = self.info.get('pb_ratio', 0)
        roe = self.info.get('roe', 0)
        profit_margin = self.info.get('profit_margin', 0)
        dividend_yield = self.info.get('dividend_yield', 0)
        
        valuation, val_score, val_reasons = fa.evaluate_valuation(pe, pb, roe)
        quality, quality_factors = fa.quality_score(profit_margin, roe, 0.5)
        
        return {
            'pe_ratio': pe,
            'pb_ratio': pb,
            'roe': roe,
            'profit_margin': profit_margin,
            'dividend_yield': dividend_yield,
            'valuation': valuation,
            'valuation_score': val_score,
            'quality_score': quality,
            'reasons': val_reasons + quality_factors
        }
    
    def _risk_analysis(self, tech, fund):
        """Analyze risk"""
        risk_score = 0
        risk_factors = []
        
        # Technical risks
        if tech['rsi_signal'] == 'OVERBOUGHT':
            risk_score += 2
            risk_factors.append(f"⚠️ RSI overbought ({tech['rsi']})")
        
        if tech['trend'] == 'DOWNTREND':
            risk_score += 2
            risk_factors.append("⚠️ In downtrend")
        
        if tech['volume_strength'] == 'NORMAL':
            risk_score += 1
            risk_factors.append("⚠️ Low volume")
        
        # Fundamental risks
        if fund.get('valuation') == 'OVERVALUED':
            risk_score += 2
            risk_factors.append("⚠️ Overvalued")
        
        if fund.get('quality_score', 0) < 4:
            risk_score += 2
            risk_factors.append("⚠️ Poor quality")
        
        # Determine risk level
        if risk_score <= 2:
            risk_level = 'LOW'
        elif risk_score <= 4:
            risk_level = 'MEDIUM'
        elif risk_score <= 6:
            risk_level = 'HIGH'
        else:
            risk_level = 'EXTREME'
        
        return {
            'risk_level': risk_level,
            'risk_score': risk_score,
            'factors': risk_factors if risk_factors else ['✅ No major risks identified']
        }
    
    def _generate_recommendation(self, tech, fund, risk):
        """Generate BUY/SELL/WAIT recommendation"""
        score = 0
        reasons = []
        
        # Technical signals
        if tech['trend'] == 'UPTREND':
            score += 2
            reasons.append("📈 Uptrend detected")
        elif tech['trend'] == 'DOWNTREND':
            score -= 2
            reasons.append("📉 Downtrend detected")
        
        if tech['macd_signal'] == 'BULLISH':
            score += 1.5
            reasons.append("📊 MACD bullish crossover")
        elif tech['macd_signal'] == 'BEARISH':
            score -= 1.5
            reasons.append("📊 MACD bearish crossover")
        
        if tech['rsi_signal'] == 'OVERSOLD':
            score += 1
            reasons.append("🔻 RSI oversold - Buy signal")
        elif tech['rsi_signal'] == 'OVERBOUGHT':
            score -= 1
            reasons.append("🔺 RSI overbought - Sell signal")
        
        # Fundamental signals
        if fund.get('valuation') == 'UNDERVALUED':
            score += 1.5
            reasons.append("💰 Undervalued")
        elif fund.get('valuation') == 'OVERVALUED':
            score -= 1.5
            reasons.append("💸 Overvalued")
        
        if fund.get('quality_score', 0) >= 7:
            score += 1
            reasons.append("⭐ High quality business")
        
        # Risk adjustment
        if risk['risk_level'] == 'EXTREME':
            score -= 3
            reasons.append("❌ Extreme risk - AVOID")
        elif risk['risk_level'] == 'HIGH':
            score -= 1
        
        # Position sizing
        position_size = (self.capital * MAX_RISK_PERCENTAGE) / 100
        
        # Calculate confidence
        base_confidence = 50 + (score * 5)  # Convert score to confidence
        confidence = max(0, min(100, base_confidence))
        
        # Generate recommendation
        if confidence >= 75 and risk['risk_level'] not in ['HIGH', 'EXTREME']:
            recommendation = 'BUY'
        elif confidence >= 60 and confidence < 75:
            recommendation = 'WAIT'
        elif confidence < 40:
            recommendation = 'SELL'
        else:
            recommendation = 'WAIT'
        
        if risk['risk_level'] == 'EXTREME':
            recommendation = 'AVOID'
        
        return {
            'action': recommendation,
            'confidence': round(confidence, 1),
            'score': round(score, 2),
            'reasons': reasons[:3],
            'position_size': round(position_size, 2),
            'risk_warning': risk['factors'][:2]
        }
