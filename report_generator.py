from tabulate import tabulate
from colorama import Fore, Back, Style, init

init(autoreset=True)

class ReportGenerator:
    """Generate professional analysis reports"""
    
    @staticmethod
    def generate_report(analysis_result):
        """
        Generate complete analysis report
        """
        if 'error' in analysis_result:
            print(f"\n{Fore.RED}❌ {analysis_result['error']}{Style.RESET_ALL}\n")
            return
        
        symbol = analysis_result['symbol']
        tech = analysis_result['technical']
        fund = analysis_result['fundamental']
        risk = analysis_result['risk']
        rec = analysis_result['recommendation']
        
        print("\n" + "="*70)
        print(f"{Back.CYAN}{Fore.BLACK} JARVIS STOCK AI - ANALYSIS REPORT {Style.RESET_ALL}")
        print("="*70 + "\n")
        
        # Summary
        print(f"{Fore.CYAN}📊 STOCK: {symbol}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Current Price: ₹{tech['current_price']}{Style.RESET_ALL}\n")
        
        # Recommendation Box
        color_map = {'BUY': Fore.GREEN, 'SELL': Fore.RED, 'WAIT': Fore.YELLOW, 'AVOID': Fore.MAGENTA}
        action_color = color_map.get(rec['action'], Fore.WHITE)
        print(f"{Back.BLACK}{action_color}{'='*35}{Style.RESET_ALL}")
        print(f"{Back.BLACK}{action_color}RECOMMENDATION: {rec['action']}{Style.RESET_ALL}")
        print(f"{Back.BLACK}{action_color}CONFIDENCE: {rec['confidence']}%{Style.RESET_ALL}")
        print(f"{Back.BLACK}{action_color}{'='*35}{Style.RESET_ALL}\n")
        
        # Technical Analysis
        print(f"{Fore.CYAN}{'─'*35}")
        print(f"📈 TECHNICAL ANALYSIS{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─'*35}{Style.RESET_ALL}\n")
        
        tech_data = [
            ['Trend', tech['trend']],
            ['RSI', f"{tech['rsi']} ({tech['rsi_signal']})"],
            ['MACD', f"{tech['macd_signal']}"],
            ['Support', f"₹{tech['support']}"],
            ['Resistance', f"₹{tech['resistance']}"],
            ['EMA 20', f"₹{tech['ema_20']}"],
            ['EMA 50', f"₹{tech['ema_50']}"],
            ['Volume', tech['volume_strength']],
            ['Candlestick', tech['candlestick']]
        ]
        
        print(tabulate(tech_data, headers=['Indicator', 'Value'], tablefmt='grid'))
        print()
        
        # Fundamental Analysis
        print(f"{Fore.CYAN}{'─'*35}")
        print(f"💼 FUNDAMENTAL ANALYSIS{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─'*35}{Style.RESET_ALL}\n")
        
        fund_data = [
            ['PE Ratio', fund.get('pe_ratio', 'N/A')],
            ['PB Ratio', fund.get('pb_ratio', 'N/A')],
            ['ROE', f"{fund.get('roe', 'N/A')}"],
            ['Profit Margin', f"{fund.get('profit_margin', 'N/A')}"],
            ['Valuation', fund.get('valuation', 'N/A')],
            ['Quality Score', f"{fund.get('quality_score', 'N/A')}/10"]
        ]
        
        print(tabulate(fund_data, headers=['Metric', 'Value'], tablefmt='grid'))
        print()
        
        # Risk Analysis
        print(f"{Fore.CYAN}{'─'*35}")
        print(f"⚠️  RISK ANALYSIS{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─'*35}{Style.RESET_ALL}\n")
        
        risk_color = {"LOW": Fore.GREEN, "MEDIUM": Fore.YELLOW, "HIGH": Fore.RED, "EXTREME": Fore.MAGENTA}
        color = risk_color.get(risk['risk_level'], Fore.WHITE)
        
        print(f"Risk Level: {color}{risk['risk_level']}{Style.RESET_ALL}")
        print(f"Risk Score: {risk['risk_score']}/10\n")
        
        print("Risk Factors:")
        for factor in risk['factors']:
            print(f"  {factor}")
        print()
        
        # Reasons to Trade
        print(f"{Fore.GREEN}{'─'*35}")
        print(f"✅ WHY {rec['action']}?{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'─'*35}{Style.RESET_ALL}\n")
        
        for i, reason in enumerate(rec['reasons'], 1):
            print(f"  {i}. {reason}")
        print()
        
        # Warnings
        if rec['risk_warning']:
            print(f"{Fore.RED}{'─'*35}")
            print(f"⚠️  WARNINGS{Style.RESET_ALL}")
            print(f"{Fore.RED}{'─'*35}{Style.RESET_ALL}\n")
            
            for warning in rec['risk_warning']:
                print(f"  {warning}")
            print()
        
        # Trade Details
        print(f"{Fore.CYAN}{'─'*35}")
        print(f"💹 TRADE DETAILS{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─'*35}{Style.RESET_ALL}\n")
        
        print(f"Suggested Position Size: ₹{rec['position_size']}")
        print(f"Entry Price: ₹{tech['current_price']}")
        print(f"Stop Loss: ₹{tech['support']}")
        print(f"Target 1: ₹{tech['resistance']}")
        print(f"Risk/Reward: 1:{round((tech['resistance'] - tech['current_price']) / (tech['current_price'] - tech['support']), 2) if tech['current_price'] != tech['support'] else 0}")
        print()
        
        print("="*70)
        print(f"{Fore.YELLOW}⚡ DISCLAIMER: This is AI analysis, not financial advice.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Always consult with a financial advisor before trading.{Style.RESET_ALL}")
        print("="*70 + "\n")
