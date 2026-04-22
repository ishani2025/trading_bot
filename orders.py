from client import bc
class OS:
    def __init__(self):
        self.client=bc()
    def place_order(self,symbol: str,side: str,order_type: str,quantity: float,price: float | None= None):
        params={
            "symbol":symbol.upper(),
            "side":side.upper(),
            "type":order_type.upper(),
            "quantity":quantity

        }
        current_price = self.client.get_price(symbol)
        print(f"Current Market Price: {current_price}")
        if order_type.upper() == "LIMIT":
            if price is None:
                raise ValueError("price required for LIMIT orders")
            if price<current_price*0.8:
                raise ValueError("Limit price too low compared to market price")
            notional=price*quantity
            if notional<50:
                raise ValueError("Order must be atleast 50 USDT")
            params["price"]=price
            params["timeInForce"]="GTC"
        return self.client.signed_request("POST","/fapi/v1/order",params)

    
