import os
import argparse
import json
from dotenv import load_dotenv
from bot.logging_config import setup_logging
from bot.validators import validate_inputs
from bot.client import BinanceFuturesClient
from bot.orders import OrderManager

def print_summary_box(args):
    print("\n" + "="*40)
    print("      ORDER REQUEST SUMMARY")
    print("="*40)
    print(f" Symbol:    {args.symbol.upper()}")
    print(f" Side:      {args.side.upper()}")
    print(f" Type:      {args.type.upper()}")
    print(f" Quantity:  {args.quantity}")
    if args.price: print(f" Price:     {args.price}")
    if args.stop_price: print(f" Stop Price:{args.stop_price}")
    print("="*40 + "\n")

def main():
    load_dotenv()
    logger = setup_logging()

    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot CLI")
    parser.add_argument("--symbol", required=True, help="Trading pair (e.g., BTCUSDT)")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL"], help="BUY or SELL")
    parser.add_argument("--type", required=True, choices=["MARKET", "LIMIT", "STOP"], help="MARKET, LIMIT, or STOP")
    parser.add_argument("--quantity", required=True, type=float, help="Quantity to trade")
    parser.add_argument("--price", type=float, help="Price for LIMIT and STOP orders")
    parser.add_argument("--stop-price", type=float, help="Trigger price for STOP orders")

    args = parser.parse_args()

    # 1. Validate Inputs
    validate_inputs(args)

    # 2. Show Summary Box
    print_summary_box(args)

    # 3. Check Credentials
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        logger.error("API Keys missing in .env file.")
        print("❌ Error: BINANCE_API_KEY or BINANCE_API_SECRET not found in .env")
        return

    # 4. Initialize Client and Manager
    client = BinanceFuturesClient(api_key, api_secret)
    manager = OrderManager(client)

    # 5. Place Order
    success, response = manager.place_order(
        symbol=args.symbol,
        side=args.side,
        order_type=args.type,
        quantity=args.quantity,
        price=args.price,
        stop_price=args.stop_price
    )

    # 6. Display Result
    if success:
        print("[SUCCESS] ORDER PLACED SUCCESSFULLY")
        print(f"Order ID:      {response.get('orderId')}")
        print(f"Status:        {response.get('status')}")
        print(f"Executed Qty:  {response.get('executedQty')}")
        print(f"Avg Price:     {response.get('avgPrice', '0.00')}")
        if 'stopPrice' in response:
            print(f"Stop Price:    {response.get('stopPrice')}")
        
        print("\nFull JSON Response:")
        print(json.dumps(response, indent=2))
    else:
        print(f"[FAILURE] ORDER FAILED")
        print(f"Reason: {response.get('msg', 'Unknown Error')}")
        if 'code' in response:
            print(f"Error Code: {response.get('code')}")

if __name__ == "__main__":
    main()
