# ⚡ Trading Bot (Binance Futures Testnet)

A lightweight trading execution system built in Python that integrates with the Binance Futures Testnet API to place MARKET and LIMIT orders via CLI and a Streamlit UI.

---

## 🚀 Overview

This project implements a structured trading workflow:

* Secure API authentication using HMAC SHA256
* Order execution (MARKET & LIMIT)
* Real-time price fetching
* Input validation (price + notional checks)
* Logging for request/response tracking
* Streamlit-based UI for interaction

---

## 🧱 Architecture

```
Streamlit UI (app.py)
        ↓
Order Service (orders.py)
        ↓
API Client (client.py)
        ↓
Binance Futures Testnet API
```

---

## ✨ Features

* 🔐 Secure signed API requests (HMAC SHA256)
* 📈 MARKET and LIMIT order placement
* 📊 Live market price retrieval
* ⚠️ Validation:

  * LIMIT price must not be too far below market
  * Minimum order notional ≥ 50 USDT
* 🔁 Repeat last order (UI)
* 🧾 JSON response display
* 📝 Logging of API requests and responses

---

## 🛠 Tech Stack

* Python
* Streamlit
* Requests
* Binance Futures Testnet API

---

## ⚙️ Setup

```bash
git clone https://github.com/ishani2025/trading_bot.git
cd trading_bot
pip install -r req.txt
```

---

## 🔑 Configuration

Create a `config.py` file:

```python
API_KEY = "your_api_key"
SECRET_KEY = "your_secret_key"
BASE_URL = "https://testnet.binancefuture.com"
```

---

## ▶️ Run Application

### UI (Streamlit)

```bash
streamlit run app.py
```

---

### CLI

```bash
python main.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

---

## 📂 Project Structure

```
├── app.py              # Streamlit UI
├── client.py           # API client (signing, requests)
├── orders.py           # Order execution logic
├── validators.py       # Validation utilities
├── logger_setup.py     # Logging configuration
├── main.py             # CLI entry point
├── req.txt             # Dependencies
├── .gitignore
├── LICENSE
├── logs/               # Runtime logs
```

---

## 🔍 Core Logic

### API Client

Handles:

* Request signing using SECRET_KEY
* Timestamp injection
* HTTP request execution
* Logging of requests and responses

Reference: 

---

### Order Service

Handles:

* Parameter construction
* Price validation vs market
* Minimum notional check (≥ 50 USDT)
* LIMIT order constraints

Reference: 

---

## 📌 Validation Rules

* LIMIT orders require price
* Price must not be too far below market
* Order value must be ≥ 50 USDT

---

## 🧠 Design Focus

* Separation of concerns (UI / service / client)
* Secure API handling
* Real-world validation logic
* Clean request-response flow

---

## 🚧 Future Improvements

* Order history tracking
* Real-time price streaming
* Strategy/automation layer
* Persistent storage

---

## 👤 Author

Ishani
