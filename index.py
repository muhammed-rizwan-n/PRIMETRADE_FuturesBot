import logging
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException

from gui import BotGUI,tk

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.client = Client(api_key, api_secret)
        if testnet:
            self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def place_order(self, symbol, side, order_type, quantity, price=None):
        try:
            logging.info(f"Placing {order_type} order: {side} {quantity} {symbol} at {price if price else 'market price'}")
            if order_type == 'MARKET':
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=SIDE_BUY if side == 'BUY' else SIDE_SELL,
                    type=FUTURE_ORDER_TYPE_MARKET,
                    quantity=quantity
                )
            elif order_type == 'LIMIT':
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=SIDE_BUY if side == 'BUY' else SIDE_SELL,
                    type=FUTURE_ORDER_TYPE_LIMIT,
                    timeInForce=TIME_IN_FORCE_GTC,
                    quantity=quantity,
                    price=price
                )
            else:
                logging.error("Unsupported order.")
                return

            logging.info("Order placed successfully.")
            print("Order details:", order)
            return order

        except BinanceAPIException as e:
            logging.error(f"Binance API error: {e.message}")
            raise
        except BinanceOrderException as e:
            logging.error(f"Binance Order error: {e.message}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            raise
    
    def get_open_orders(self, symbol=None):
        try:
            return self.client.futures_get_open_orders(symbol=symbol) if symbol else self.client.futures_get_open_orders()
        except Exception as e:
            logging.error(str(e))
            raise

if __name__ == "__main__":
    API_KEY = open("./keys/testnet_api_key.txt").read()
    API_SECRET = open("./keys/testnet_api_secret.txt").read()

    bot = BasicBot(API_KEY, API_SECRET)
    root = tk.Tk()
    app = BotGUI(root, bot)
    root.mainloop()
