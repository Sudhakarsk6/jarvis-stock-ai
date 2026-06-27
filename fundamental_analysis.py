class FundamentalAnalysis:
    """Fundamental analysis calculations"""
    
    @staticmethod
    def evaluate_valuation(pe_ratio, pb_ratio, roe, industry_avg_pe=25):
        """
        Evaluate if stock is overvalued or undervalued
        
        Args:
            pe_ratio: Price-to-Earnings ratio
            pb_ratio: Price-to-Book ratio
            roe: Return on Equity
            industry_avg_pe: Average PE for industry
        """
        valuation_score = 0
        reasons = []
        
        try:
            # PE Analysis
            if isinstance(pe_ratio, (int, float)) and pe_ratio > 0:
                if pe_ratio < industry_avg_pe * 0.8:
                    valuation_score += 3
                    reasons.append(f"✅ PE ({pe_ratio:.1f}) below industry avg ({industry_avg_pe})")
                elif pe_ratio > industry_avg_pe * 1.5:
                    valuation_score -= 2
                    reasons.append(f"⚠️ PE ({pe_ratio:.1f}) above industry avg ({industry_avg_pe})")
                else:
                    valuation_score += 1
                    reasons.append(f"✅ PE ({pe_ratio:.1f}) within reasonable range")
            
            # ROE Analysis
            if isinstance(roe, (int, float)) and roe > 0:
                if roe > 0.15:
                    valuation_score += 2
                    reasons.append(f"✅ Strong ROE ({roe*100:.1f}%)")
                elif roe > 0.10:
                    valuation_score += 1
                    reasons.append(f"✅ Decent ROE ({roe*100:.1f}%)")
                else:
                    valuation_score -= 1
                    reasons.append(f"⚠️ Weak ROE ({roe*100:.1f}%)")
        
        except:
            pass
        
        verdict = 'UNDERVALUED' if valuation_score >= 3 else 'OVERVALUED' if valuation_score <= -1 else 'FAIRLY_VALUED'
        
        return verdict, valuation_score, reasons
    
    @staticmethod
    def quality_score(profit_margin, roe, debt_equity):
        """
        Calculate business quality score (0-10)
        """
        score = 0
        factors = []
        
        try:
            if isinstance(profit_margin, (int, float)) and profit_margin > 0:
                if profit_margin > 0.20:
                    score += 3
                    factors.append(f"✅ Excellent margins ({profit_margin*100:.1f}%)")
                elif profit_margin > 0.10:
                    score += 2
                    factors.append(f"✅ Good margins ({profit_margin*100:.1f}%)")
                else:
                    score += 1
            
            if isinstance(roe, (int, float)) and roe > 0:
                if roe > 0.20:
                    score += 3
                    factors.append(f"✅ Excellent ROE ({roe*100:.1f}%)")
                elif roe > 0.15:
                    score += 2
                    factors.append(f"✅ Good ROE ({roe*100:.1f}%)")
                else:
                    score += 1
            
            if isinstance(debt_equity, (int, float)):
                if debt_equity < 0.5:
                    score += 2
                    factors.append(f"✅ Low debt ({debt_equity:.2f})")
                elif debt_equity < 1.0:
                    score += 1
                    factors.append(f"✅ Moderate debt ({debt_equity:.2f})")
                else:
                    factors.append(f"⚠️ High debt ({debt_equity:.2f})")
        
        except:
            pass
        
        return min(score, 10), factors
