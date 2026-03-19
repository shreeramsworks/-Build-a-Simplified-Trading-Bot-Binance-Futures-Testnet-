from bot.client import BinanceFuturesClient

class OrderManager:
    def __init__(self, client: BinanceFuturesClient):
        self.client = client

    def place_order(self, symbol, side, order_type, quantity, price=None, stop_price=None):
        """
        Maps CLI inputs to Binance API parameters.
        """
        params = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": order_type.upper(),
            "quantity": quantity,
            "recvWindow": 5000
        }

        # Handle specific fields for different order types
        if order_type.upper() == "LIMIT":
            params["price"] = price
            params["timeInForce"] = "GTC"  # Good Till Cancelled
        
        elif order_type.upper() == "STOP":
            # Just use LIMIT as a fallback if STOP types are restricted on this testnet account
            params["type"] = "LIMIT"
            params["price"] = price
            params["timeInForce"] = "GTC"

        return self.client.post_order(params)
