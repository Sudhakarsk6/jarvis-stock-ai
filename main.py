#!/usr/bin/env python3
"""
JARVIS STOCK AI - Main Entry Point
Indian Stock Market Analysis System
"""

from analyzer import StockAnalyzer
from report_generator import ReportGenerator
from config import TRADING_STYLES, CAPITAL_LEVELS
from colorama import Fore, Back, Style, init
import sys

init(autoreset=True)

def display_menu():
    """Display main menu"""
    print("\n" + "="*70)
    print(f"{Back.CYAN}{Fore.BLACK} JARVIS STOCK AI {Style.RESET_ALL}")
    print(f"{Fore.CYAN}Indian Stock Market Analysis System{Style.RESET_ALL}")
    print("="*70 + "\n")
    
    print(f"{Fore.YELLOW}Enter Stock Symbol (NSE format):{Style.RESET_ALL}")
    print(f"  Example: RELIANCE.NS, TCS.NS, INFY.NS, HDFC.NS")
    symbol = input(f"{Fore.GREEN}> {Style.RESET_ALL}").strip().upper()
    
    if not symbol:
        print(f"{Fore.RED}❌ Symbol required!{Style.RESET_ALL}")
        return None, None, None
    
    # Capital input
    print(f"\n{Fore.YELLOW}Enter Capital (in ₹) [{list(CAPITAL_LEVELS.values())[0]} to {list(CAPITAL_LEVELS.values())[-1]}]:{Style.RESET_ALL}")
    try:
        capital = float(input(f"{Fore.GREEN}> ₹ {Style.RESET_ALL}"))
        if capital < 500:
            print(f"{Fore.RED}❌ Minimum capital: ₹500{Style.RESET_ALL}")
            return None, None, None
    except ValueError:
        print(f"{Fore.RED}❌ Invalid amount!{Style.RESET_ALL}")
        return None, None, None
    
    # Trading style
    print(f"\n{Fore.YELLOW}Select Trading Style:{Style.RESET_ALL}")
    styles = list(TRADING_STYLES.items())
    for i, (key, value) in enumerate(styles, 1):
        print(f"  {i}. {value}")
    
    try:
        choice = int(input(f"{Fore.GREEN}> {Style.RESET_ALL}"))
        if 1 <= choice <= len(styles):
            trading_style = styles[choice-1][0]
        else:
            print(f"{Fore.RED}❌ Invalid choice!{Style.RESET_ALL}")
            return None, None, None
    except ValueError:
        print(f"{Fore.RED}❌ Invalid input!{Style.RESET_ALL}")
        return None, None, None
    
    return symbol, capital, trading_style

def run_analysis(symbol, capital, trading_style):
    """Run stock analysis"""
    analyzer = StockAnalyzer(symbol, capital, trading_style)
    result = analyzer.analyze()
    
    if 'error' not in result:
        ReportGenerator.generate_report(result)
        return True
    return False

def main():
    """Main function"""
    try:
        while True:
            symbol, capital, trading_style = display_menu()
            
            if symbol:
                print(f"\n{Fore.CYAN}🔄 Processing your analysis...{Style.RESET_ALL}\n")
                run_analysis(symbol, capital, trading_style)
            
            # Ask to continue
            print(f"{Fore.YELLOW}Analyze another stock? (y/n): {Style.RESET_ALL}", end="")
            if input().strip().lower() != 'y':
                print(f"\n{Fore.CYAN}Thank you for using JARVIS Stock AI!{Style.RESET_ALL}\n")
                break
    
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Exiting JARVIS Stock AI...{Style.RESET_ALL}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}❌ Error: {str(e)}{Style.RESET_ALL}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
