import os
import requests
from fastapi import APIRouter, Depends
from .auth import get_current_user

router = APIRouter()

@router.get("/bal")
def check_balance(currency: str = None, user=Depends(get_current_user)):
    if not currency:
        return {"balance": user.balance, "currency": "INR"}
    res = requests.get("https://api.currencyapi.com/v3/latest", params={
        "apikey": os.getenv("CURRENCY_API_KEY"),
        "base_currency": "INR",
        "currencies": currency
    })
    rate = res.json()["data"][currency]["value"]
    converted = user.balance * rate
    return {"balance": round(converted, 2), "currency": currency}
