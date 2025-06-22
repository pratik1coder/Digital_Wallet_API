# 💳 Digital Wallet API (FastAPI + SQLite)

Backend service that simulates a digital wallet:
- Register users
- Fund wallet
- Pay other users
- Check balance (in INR or foreign currency)
- View transactions
- Buy products

## ✅ Tech Stack
- FastAPI
- SQLite
- SQLAlchemy
- bcrypt
- CurrencyAPI

## 🛠 Setup

1. Clone the repo
```bash
git clone https://github.com/your-username/digital-wallet-api.git
cd digital-wallet-api
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Create `.env` file
```
CURRENCY_API_KEY=your_currencyapi_key
```

4. Run the server
```bash
uvicorn app.main:app --reload
```
