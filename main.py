import argparse
from client import bc
from orders import OS
from logger_setup import setup_logger
setup_logger()
def parse_args():
    parser = argparse.ArgumentParser(description="Trading Bot CLI (Enhanced)")
    parser.add_argument("--symbol")
    parser.add_argument("--side", choices=["BUY", "SELL"])
    parser.add_argument("--type", choices=["MARKET", "LIMIT"])
    parser.add_argument("--quantity", type=float)
    parser.add_argument("--price", type=float)
    return parser.parse_args()
if __name__ == "__main__":
    args = parse_args()
    def get_input(prompt,default=None):
        val=input(f"{prompt} [{default}]: ")
        return val.strip() if val.strip() else default
    symbol = args.symbol or get_input("Enter symbol", "BTCUSDT")
    side = args.side or get_input("Enter side (BUY/SELL)", "BUY")
    order_type = args.type or get_input("Enter type (MARKET/LIMIT)", "MARKET")
    quantity = args.quantity or float(get_input("Enter quantity", "0.001"))
    price = args.price

    if order_type == "LIMIT":
        if price is None:
            price = float(get_input("Enter price", "30000"))
    print(f"{side} {quantity} {symbol} ({order_type})")
    if order_type == "LIMIT":
        print(f"Price: {price}")

    confirm = input("Proceed? (y/n): ")
    if confirm.lower() != "y":
        print("Cancelled.")
        exit()

    client = bc()
    print("\nServer:", client.get_server_time())

    service = OS()

    try:
        response = service.place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price
        )

        print("\nSUCCESS")
        print(f"Order ID: {response.get('orderId')}")
        print(f"Status: {response.get('status')}")
        print(f"Executed Qty: {response.get('executedQty')}")
        print(f"Avg Price: {response.get('avgPrice')}")

    except Exception as e:
        print("\nFAILED:", str(e))
