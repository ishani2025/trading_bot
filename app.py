import streamlit as st
from orders import OS
from client import bc
from logger_setup import setup_logger
import json
setup_logger()
st.set_page_config(page_title="Trading Bot", layout="centered")
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #0b0e11;
    color: white;
}
[data-testid="stHeader"] {
    background: #0b0e11;
}
h1, h2, h3, h4, h5, h6, p, label {
    color: white !important;
}
.stTextInput input, .stNumberInput input {
    background-color: #1e2329 !important;
    color: white !important;
    border-radius: 8px;
}

.stSelectbox div[data-baseweb="select"] {
    background-color: #1e2329 !important;
    color: white !important;
    border-radius: 8px;
}

/* Buttons */
.stButton > button {
    background-color: #f0b90b !important;
    color: black !important;
    font-weight: bold;
    border-radius: 8px;
    padding: 10px;
}
.stAlert {
    background-color: #1e2329 !important;
    color: white !important;
}

</style>
""", unsafe_allow_html=True)
st.title("Trading BOT")
symbol=st.text_input("Symbol","BTCUSDT")
if not symbol.strip():
    st.error("Symbol cannot be empty")
    st.stop()
if "client" not in st.session_state:
    st.session_state.client = bc()
client = st.session_state.client
try:
    current_price = client.get_price(symbol)
    st.info(f"📊 Current Price: {current_price}")
except:
    st.warning("Unable to fetch market price")
side=st.selectbox("Side",["BUY","SELL"])
order_type=st.selectbox("Order Type",["MARKET","LIMIT"])
quantity=st.number_input("Quantity",min_value=0.001,value=0.001,format="%.3f")
default_price = current_price * 1.02 if 'current_price' in locals() else 30000.0
price = st.number_input("PRICE", min_value=0.0, value=float(default_price))
if order_type=="LIMIT":
    price=st.number_input("PRICE",min_value=0.0,value=30000.0)
if "last_order" not in st.session_state:
    st.session_state.last_order=None
col1, col2,col3 = st.columns(3)

with col1:
    place = st.button("Place Order")

with col2:
    repeat = st.button("Repeat Order")
with col3:
    reset=st.button("RESET")
if place:
    service=OS()
    try:
        response=service.place_order(
            symbol=symbol,
            side=side,
            quantity=quantity,
            price=price,
            order_type=order_type
        )

        st.session_state.last_order={
            "symbol":symbol,
            "side":side,
            "quantity":quantity,
            "price":price,
            "order_type":order_type
        }
        st.success(f"{side} {quantity} {symbol} order placed")
        st.code(json.dumps(response, indent=2), language="json")
    except Exception as e:
        st.error(str(e))
if repeat and st.session_state.last_order:
    last = st.session_state.last_order
    service = OS()

    try:
        if last["order_type"] == "MARKET":
            response = service.place_order(
                symbol=last["symbol"],
                side=last["side"],
                order_type=last["order_type"],
                quantity=last["quantity"]
            )
        else:
            response = service.place_order(**last)

        st.success("Repeated order placed")
        st.code(json.dumps(response, indent=2), language="json")

    except Exception as e:
        st.error(str(e))
if reset:
    st.session_state.clear()
    st.rerun()
