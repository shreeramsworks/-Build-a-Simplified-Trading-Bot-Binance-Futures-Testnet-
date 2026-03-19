# Binance Futures Testnet Trading Bot

**[NOTICE]: This project was built 100% using AI **

A robust Python CLI application to place orders on the Binance Futures Testnet (USDT-M) using direct REST API calls and HMAC-SHA256 signing.

## Features
- **Direct REST Implementation**: No external Binance libraries used.
- **Secure Signing**: Manual HMAC-SHA256 signature generation.
- **Order Types**: Supports `MARKET`, `LIMIT`, and `STOP` (Stop-Limit).
- **Beautiful Logging**: Structured logs in `logs/trading_bot.log`.
- **Validation**: Strict input validation with clear CLI feedback.

## Setup Instructions

1. **Clone the project** and navigate to the directory:
   ```bash
   cd trading_bot
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   - Copy `.env.example` to `.env`.
   - Add your Binance Futures Testnet API Key and Secret.
   ```bash
   cp .env.example .env
   ```

## Usage Examples

### 1. Market Buy Order
Places a market order to buy 0.001 BTC.
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### 2. Limit Sell Order
Places a limit order to sell 0.001 BTC at $70,000.
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 70000
```

### 3. Stop-Limit Buy Order
Places a stop-limit order to buy 0.001 BTC when price hits $65,000, with a limit price of $65,100.
```bash
python cli.py --symbol BTCUSDT --side BUY --type STOP --quantity 0.001 --stop-price 65000 --price 65100
```

## Assumptions & Logic
- **Base URL**: Uses `https://demo-fapi.binance.com` (Futures Demo API).
- **Time in Force**: `LIMIT` and `STOP` orders default to `GTC` (Good Till Cancelled).
- **STOP Type**: Implemented as a Stop-Limit order as per bonus requirements.
- **RecvWindow**: Set to 5000ms to prevent timestamp synchronization issues.

## Documentation References
- [Spot Demo API Documentation](https://developers.binance.com/docs/binance-spot-api-docs/demo-mode/general-info)
- [Futures Demo API Base Endpoint](https://demo-fapi.binance.com)
- [Futures API Documentation](https://developers.binance.com/docs/derivatives/)
