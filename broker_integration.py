import os
from colorama import Fore, Style

class BrokerAPI:
    """
    Broker API Integration Framework
    Supports Zerodha Kite, Upstox, Alice Blue, etc.
    """
    
    def __init__(self, broker_name='manual'):
        """
        Initialize broker connection
        
        Args:
            broker_name: 'kite', 'upstox', 'alice', 'manual'
        """
        self.broker_name = broker_name
        self.is_connected = False
    
    def connect_kite(self, api_key, access_token):
        """
        Connect to Zerodha Kite API
        
        Installation:
        pip install kiteconnect
        """
        try:
            from kiteconnect import KiteConnect
            
            kite = KiteConnect(api_key=api_key)
            kite.set_access_token(access_token)
            
            self.kite = kite
            self.is_connected = True
            
            print(f"{Fore.GREEN}✅ Connected to Zerodha Kite{Style.RESET_ALL}")
            return kite
        
        except ImportError:
            print(f"{Fore.YELLOW}⚠️ Install: pip install kiteconnect{Style.RESET_ALL}")
            return None
        except Exception as e:
            print(f"{Fore.RED}❌ Connection failed: {str(e)}{Style.RESET_ALL}")
            return None
    
    def connect_upstox(self, api_key, access_token):
        """
        Connect to Upstox API
        
        Installation:
        pip install upstox
        """
        try:
            from upstox_client.rest import ApiClient
            from upstox_client.rest import Configuration
            
            config = Configuration()
            config.access_token = access_token
            api_client = ApiClient(config)
            
            self.upstox = api_client
            self.is_connected = True
            
            print(f"{Fore.GREEN}✅ Connected to Upstox{Style.RESET_ALL}")
            return api_client
        
        except ImportError:
            print(f"{Fore.YELLOW}⚠️ Install: pip install upstox{Style.RESET_ALL}")
            return None
        except Exception as e:
            print(f"{Fore.RED}❌ Connection failed: {str(e)}{Style.RESET_ALL}")
            return None
    
    def get_live_quote(self, symbol):
        """
        Get live quote from broker API
        """
        if self.broker_name == 'kite' and self.is_connected:
            try:
                quote = self.kite.quote(symbols=[symbol])
                return quote
            except Exception as e:
                print(f"{Fore.RED}❌ Quote error: {str(e)}{Style.RESET_ALL}")
                return None
        
        return None
    
    def place_order(self, symbol, quantity, price, order_type='BUY'):
        """
        Place order through broker API
        
        Args:
            symbol: Trading symbol
            quantity: Number of shares
            price: Order price
            order_type: 'BUY' or 'SELL'
        """
        if not self.is_connected:
            print(f"{Fore.RED}❌ Broker not connected{Style.RESET_ALL}")
            return None
        
        try:
            if self.broker_name == 'kite':
                order = self.kite.place_order(
                    variety=self.kite.VARIETY_REGULAR,
                    exchange=self.kite.EXCHANGE_NSE,
                    tradingsymbol=symbol,
                    transaction_type=self.kite.TRANSACTION_TYPE_BUY if order_type == 'BUY' else self.kite.TRANSACTION_TYPE_SELL,
                    quantity=quantity,
                    price=price,
                    order_type=self.kite.ORDER_TYPE_LIMIT,
                    product=self.kite.PRODUCT_MIS
                )
                
                print(f"{Fore.GREEN}✅ Order placed: {order}{Style.RESET_ALL}")
                return order
        
        except Exception as e:
            print(f"{Fore.RED}❌ Order failed: {str(e)}{Style.RESET_ALL}")
            return None
    
    def get_positions(self):
        """
        Get current positions from broker
        """
        if not self.is_connected:
            return None
        
        try:
            if self.broker_name == 'kite':
                positions = self.kite.positions()
                return positions
        except Exception as e:
            print(f"{Fore.RED}❌ Error fetching positions: {str(e)}{Style.RESET_ALL}")
            return None
    
    def get_holdings(self):
        """
        Get holdings from broker
        """
        if not self.is_connected:
            return None
        
        try:
            if self.broker_name == 'kite':
                holdings = self.kite.holdings()
                return holdings
        except Exception as e:
            print(f"{Fore.RED}❌ Error fetching holdings: {str(e)}{Style.RESET_ALL}")
            return None


class AlertNotifier:
    """
    Send alerts via multiple channels
    """
    
    @staticmethod
    def send_email(recipient, subject, message):
        """
        Send email alert
        """
        try:
            import smtplib
            from email.mime.text import MIMEText
            
            # Configure your email
            sender = os.getenv('EMAIL_SENDER')
            password = os.getenv('EMAIL_PASSWORD')
            
            msg = MIMEText(message)
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = recipient
            
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(sender, password)
                server.send_message(msg)
            
            print(f"{Fore.GREEN}✅ Email sent to {recipient}{Style.RESET_ALL}")
            return True
        
        except Exception as e:
            print(f"{Fore.RED}❌ Email failed: {str(e)}{Style.RESET_ALL}")
            return False
    
    @staticmethod
    def send_telegram(bot_token, chat_id, message):
        """
        Send Telegram alert
        
        Setup: Create bot with @BotFather on Telegram
        """
        try:
            import requests
            
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            payload = {
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                print(f"{Fore.GREEN}✅ Telegram message sent{Style.RESET_ALL}")
                return True
            else:
                print(f"{Fore.RED}❌ Telegram failed: {response.text}{Style.RESET_ALL}")
                return False
        
        except Exception as e:
            print(f"{Fore.RED}❌ Telegram error: {str(e)}{Style.RESET_ALL}")
            return False
    
    @staticmethod
    def send_sms(phone_number, message):
        """
        Send SMS alert
        
        Requires: Twilio account
        pip install twilio
        """
        try:
            from twilio.rest import Client
            
            account_sid = os.getenv('TWILIO_ACCOUNT_SID')
            auth_token = os.getenv('TWILIO_AUTH_TOKEN')
            twilio_number = os.getenv('TWILIO_PHONE_NUMBER')
            
            client = Client(account_sid, auth_token)
            msg = client.messages.create(
                body=message,
                from_=twilio_number,
                to=phone_number
            )
            
            print(f"{Fore.GREEN}✅ SMS sent to {phone_number}{Style.RESET_ALL}")
            return True
        
        except Exception as e:
            print(f"{Fore.RED}❌ SMS failed: {str(e)}{Style.RESET_ALL}")
            return False
