#!/usr/bin/env python3
"""
JARVIS STOCK AI - Real-Time Monitoring
Live market analysis with alerts
"""

from realtime_monitor import RealtimeMonitor
from broker_integration import BrokerAPI, AlertNotifier
from colorama import Fore, Back, Style, init
import sys
import os
from dotenv import load_dotenv

init(autoreset=True)
load_dotenv()

def display_realtime_menu():
    """
    Display real-time monitoring menu
    """
    print("\n" + "="*70)
    print(f"{Back.CYAN}{Fore.BLACK} JARVIS STOCK AI - REAL-TIME MONITOR {Style.RESET_ALL}")
    print(f"{Fore.CYAN}Live Market Analysis & Alerts{Style.RESET_ALL}")
    print("="*70 + "\n")
    
    print(f"{Fore.YELLOW}Enter Stock Symbol (NSE format):{Style.RESET_ALL}")
    print(f"  Example: RELIANCE.NS, TCS.NS, INFY.NS")
    symbol = input(f"{Fore.GREEN}> {Style.RESET_ALL}").strip().upper()
    
    if not symbol:
        print(f"{Fore.RED}❌ Symbol required!{Style.RESET_ALL}")
        return None, None, None
    
    # Capital
    print(f"\n{Fore.YELLOW}Enter Capital (in ₹):{Style.RESET_ALL}")
    try:
        capital = float(input(f"{Fore.GREEN}> ₹ {Style.RESET_ALL}"))
        if capital < 500:
            print(f"{Fore.RED}❌ Minimum capital: ₹500{Style.RESET_ALL}")
            return None, None, None
    except ValueError:
        print(f"{Fore.RED}❌ Invalid amount!{Style.RESET_ALL}")
        return None, None, None
    
    # Monitoring duration
    print(f"\n{Fore.YELLOW}Monitoring Duration (hours):")
    print(f"  Default: 8 (market hours)")
    print(f"  Min: 1, Max: 24{Style.RESET_ALL}")
    
    try:
        duration = input(f"{Fore.GREEN}> {Style.RESET_ALL}").strip()
        duration = float(duration) if duration else 8
        duration = max(1, min(24, duration))
    except ValueError:
        duration = 8
    
    return symbol, capital, duration

def display_broker_menu():
    """
    Display broker integration menu
    """
    print(f"\n{Fore.CYAN}{'-'*70}")
    print(f"BROKER INTEGRATION{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'-'*70}{Style.RESET_ALL}\n")
    
    print("Choose broker (optional):")
    print("  1. Manual Monitoring (No broker - recommended for learning)")
    print("  2. Zerodha Kite API")
    print("  3. Upstox API")
    print("  4. Skip for now")
    
    choice = input(f"{Fore.GREEN}> {Style.RESET_ALL}").strip()
    
    return choice

def setup_broker_kite():
    """
    Setup Zerodha Kite connection
    """
    print(f"\n{Fore.YELLOW}Zerodha Kite Setup:{Style.RESET_ALL}")
    print("Get API Key from: https://kite.zerodha.com/account/profile/api")
    print("pip install kiteconnect\n")
    
    api_key = input(f"{Fore.GREEN}API Key: {Style.RESET_ALL}").strip()
    access_token = input(f"{Fore.GREEN}Access Token: {Style.RESET_ALL}").strip()
    
    broker = BrokerAPI('kite')
    kite = broker.connect_kite(api_key, access_token)
    
    return broker if kite else None

def setup_broker_upstox():
    """
    Setup Upstox connection
    """
    print(f"\n{Fore.YELLOW}Upstox Setup:{Style.RESET_ALL}")
    print("Get API Key from: https://upstox.com/developer")
    print("pip install upstox\n")
    
    api_key = input(f"{Fore.GREEN}API Key: {Style.RESET_ALL}").strip()
    access_token = input(f"{Fore.GREEN}Access Token: {Style.RESET_ALL}").strip()
    
    broker = BrokerAPI('upstox')
    upstox = broker.connect_upstox(api_key, access_token)
    
    return broker if upstox else None

def display_alert_menu():
    """
    Display alert notification menu
    """
    print(f"\n{Fore.CYAN}{'-'*70}")
    print(f"ALERT NOTIFICATIONS{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'-'*70}{Style.RESET_ALL}\n")
    
    print("Enable notifications (optional):")
    print("  1. Console Only (default)")
    print("  2. Email Alerts")
    print("  3. Telegram Alerts")
    print("  4. SMS Alerts")
    print("  5. Skip")
    
    choice = input(f"{Fore.GREEN}> {Style.RESET_ALL}").strip()
    
    return choice

def setup_email_alerts():
    """
    Setup email alerts
    """
    print(f"\n{Fore.YELLOW}Email Setup (Gmail recommended):{Style.RESET_ALL}")
    print("1. Use Gmail 2FA App Password")
    print("2. Set environment: EMAIL_SENDER, EMAIL_PASSWORD\n")
    
    recipient = input(f"{Fore.GREEN}Recipient Email: {Style.RESET_ALL}").strip()
    
    return recipient if recipient else None

def setup_telegram_alerts():
    """
    Setup Telegram alerts
    """
    print(f"\n{Fore.YELLOW}Telegram Setup:{Style.RESET_ALL}")
    print("1. Message @BotFather on Telegram")
    print("2. Create new bot: /newbot")
    print("3. Get bot token")
    print("4. Get chat ID by messaging bot: /start\n")
    
    bot_token = input(f"{Fore.GREEN}Bot Token: {Style.RESET_ALL}").strip()
    chat_id = input(f"{Fore.GREEN}Chat ID: {Style.RESET_ALL}").strip()
    
    return bot_token, chat_id if bot_token and chat_id else (None, None)

def run_realtime_monitor(symbol, capital, duration):
    """
    Run real-time monitoring session
    """
    monitor = RealtimeMonitor(symbol, capital, check_interval=60)
    
    print(f"\n{Fore.CYAN}Starting real-time monitoring...{Style.RESET_ALL}\n")
    
    try:
        monitor.run_continuous(duration)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚡ Monitoring stopped{Style.RESET_ALL}\n")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Error: {str(e)}{Style.RESET_ALL}\n")

def main():
    """
    Main real-time monitoring function
    """
    try:
        while True:
            symbol, capital, duration = display_realtime_menu()
            
            if not symbol:
                continue
            
            # Broker setup
            broker_choice = display_broker_menu()
            broker = None
            
            if broker_choice == '2':
                broker = setup_broker_kite()
            elif broker_choice == '3':
                broker = setup_broker_upstox()
            
            # Alert setup
            alert_choice = display_alert_menu()
            notification_config = {}
            
            if alert_choice == '2':
                email = setup_email_alerts()
                if email:
                    notification_config['email'] = email
            elif alert_choice == '3':
                bot_token, chat_id = setup_telegram_alerts()
                if bot_token and chat_id:
                    notification_config['telegram'] = {'bot_token': bot_token, 'chat_id': chat_id}
            elif alert_choice == '4':
                print(f"{Fore.YELLOW}SMS requires Twilio setup (see code)")
            
            # Run monitoring
            run_realtime_monitor(symbol, capital, duration)
            
            # Ask to continue
            print(f"{Fore.YELLOW}Monitor another stock? (y/n): {Style.RESET_ALL}", end="")
            if input().strip().lower() != 'y':
                print(f"\n{Fore.CYAN}Thank you for using JARVIS Real-Time Monitor!{Style.RESET_ALL}\n")
                break
    
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Exiting JARVIS...{Style.RESET_ALL}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}❌ Error: {str(e)}{Style.RESET_ALL}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
