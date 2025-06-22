from pydantic import BaseModel
from datetime import datetime

class RegisterRequest(BaseModel):
    username: str
    password: str

class FundRequest(BaseModel):
    amt: float

class PayRequest(BaseModel):
    to: str
    amt: float

class ProductCreate(BaseModel):
    name: str
    price: float
    description: str

class BuyRequest(BaseModel):
    product_id: int

class TransactionOut(BaseModel):
    kind: str
    amt: float
    updated_bal: float
    timestamp: datetime
