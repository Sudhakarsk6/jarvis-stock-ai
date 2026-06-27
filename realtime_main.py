#!/usr/bin/env python3
"""
JARVIS STOCK AI - Real-Time Monitoring with Intraday Signals
Live market analysis with intraday buy suggestions and Telegram alerts
"""

from realtime_monitor import RealtimeMonitor
from intraday_analyzer import IntradayAnalyzer
from broker_integration import BrokerAPI, AlertNotifier
from colorama import Fore, Back, Style, init
import sys
import os
from dotenv import load_dotenv
import time

init(autoreset=True)
load_dotenv()

def display_realtime_menu():
    """
    Display real-time monitoring menu
    """
    print("\n" + "="*70)
    print(f"{Back.CYAN}{Fore.BLACK} JARVIS STOCK AI - REAL-TIME MONITOR {Style.RESET_ALL}")
    print(f"{Fore.CYAN}Live Market Analysis with Intraday Buy Signals{Style.RESET_ALL}")
    print("="*70 + "\n")
    
    print(f"{Fore.YELLOW}Enter Stock Symbol (NSE format):{Style.RESET_ALL}")
    print(f"  Example: RELIANCE.NS, TCS.NS, INFY.NS")
    symbol = input(f"{Fore.GREEN}> {Style.RESET_ALL}").strip().upper()
    
    if not symbol:
        print(f"{Fore.RED}✗ Symbol required!{Style.RESET_ALL}")
        return None, None, None
    
    # Capital
    print(f"\n{Fore.YELLOW}Enter Capital (in ₹):{Style.RESET_ALL}")
    try:
        capital = float(input(f"{Fore.GREEN}> ₹ {Style.RESET_ALL}"))
        if capital < 500:
            print(f"{Fore.RED}✗ Minimum capital: ₹500{Style.RESET_ALL}")
            return None, None, None
    except ValueError:
        print(f"{Fore.RED}✗ Invalid amount!{Style.RESET_ALL}")
        return None, None, None
    
    # Monitoring duration
    print(f"\n{Fore.YELLOW}Monitoring Duration (hours):{Style.RESET_ALL}")
    print(f"  Default: 7 (market hours 9:15 AM - 3:30 PM)")
    print(f"  Min: 1, Max: 24")
    
    try:
        duration = input(f"{Fore.GREEN}> {Style.RESET_ALL}").strip()
        duration = float(duration) if duration else 7
        duration = max(1, min(24, duration))
    except ValueError:
        duration = 7
    
    return symbol, capital, duration

def display_telegram_setup():
    """
    Display Telegram setup menu
    """
    print(f"\n{Fore.CYAN}{'-'*70}")
    print(f"🤖 TELEGRAM SETUP (For Alerts & Intraday Signals){Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'-'*70}{Style.RESET_ALL}\n")
    
    print("Choose notification option:")
    print("  1. Console Only (No notifications)")
    print("  2. Enable Telegram Alerts")
    
    choice = input(f"{Fore.GREEN}> {Style.RESET_ALL}").strip()
    
    if choice == '2':
        print(f"\n{Fore.YELLOW}Telegram Setup:{Style.RESET_ALL}")
        print("1. Message @BotFather on Telegram")
        print("2. Create bot: /newbot")
        print("3. Copy Bot Token")
        print("4. Add bot to group or get personal chat ID\n")
        
        bot_token = input(f"{Fore.GREEN}Bot Token: {Style.RESET_ALL}").strip()
        
        if not bot_token:
            print(f"{Fore.YELLOW}⚠️  Telegram disabled{Style.RESET_ALL}")
            return None, None
        
        print(f"\n{Fore.YELLOW}Chat ID Types:{Style.RESET_ALL}")
        print("  Group: Starts with -")
        print("  Channel: Starts with -100")
        print("  Personal: Just numbers")
        print()
        
        chat_id = input(f"{Fore.GREEN}Chat ID: {Style.RESET_ALL}").strip()
        
        if not chat_id:
            print(f"{Fore.YELLOW}⚠️  Telegram disabled{Style.RESET_ALL}")
            return None, None
        
        print(f"{Fore.GREEN}✅ Telegram enabled!{Style.RESET_ALL}")
        return bot_token, chat_id
    
    return None, None

def display_intraday_menu():
    """
    Display intraday trading options
    """
    print(f"\n{Fore.CYAN}{'-'*70}")
    print(f"📈 INTRADAY BUY SIGNALS{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'-'*70}{Style.RESET_ALL}\n")
    
    print("Enable intraday buy suggestions:")
    print("  1. Off (Only real-time alerts)")
    print("  2. On (Get intraday buy signals)")
    
    choice = input(f"{Fore.GREEN}> {Style.RESET_ALL}").strip()
    
    return choice == '2'

def run_realtime_with_intraday(symbol, capital, duration, bot_token=None, chat_id=None, enable_intraday=False):
    """
    Run real-time monitoring with intraday analysis
    """
    monitor = RealtimeMonitor(symbol, capital, check_interval=60)
    intraday = IntradayAnalyzer(symbol) if enable_intraday else None
    
    print(f"\n{Fore.CYAN}Starting real-time monitoring...{Style.RESET_ALL}\n")
    
    try:
        # Run continuous monitoring
        monitor.run_continuous_with_intraday(
            duration=duration,
            intraday_analyzer=intraday,
            telegram_config={'bot_token': bot_token, 'chat_id': chat_id} if bot_token and chat_id else None
        )
    
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚡ Monitoring stopped{Style.RESET_ALL}\n")
    except Exception as e:
        print(f"\n{Fore.RED}✗ Error: {str(e)}{Style.RESET_ALL}\n")

def main():
    """
    Main real-time monitoring function
    """
    try:
        while True:
            symbol, capital, duration = display_realtime_menu()
            
            if not symbol:
                continue
            
            # Telegram setup
            bot_token, chat_id = display_telegram_setup()
            
            # Intraday signals
            enable_intraday = display_intraday_menu()
            
            # Run monitoring
            run_realtime_with_intraday(symbol, capital, duration, bot_token, chat_id, enable_intraday)
            
            # Ask to continue
            print(f"{Fore.YELLOW}Monitor another stock? (y/n): {Style.RESET_ALL}", end="")
            if input().strip().lower() != 'y':
                print(f"\n{Fore.CYAN}Thank you for using JARVIS Real-Time Monitor!{Style.RESET_ALL}\n")
                break
    
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}⚡ Exiting JARVIS...{Style.RESET_ALL}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}✗ Error: {str(e)}{Style.RESET_ALL}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
