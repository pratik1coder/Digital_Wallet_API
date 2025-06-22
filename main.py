from fastapi import FastAPI, Depends
from . import wallet, auth, products, currency
from .db import Base, engine
from .models import *
from .auth import get_db
from .schemas import RegisterRequest
from sqlalchemy.orm import Session
import bcrypt

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(wallet.router)
app.include_router(products.router)
app.include_router(currency.router)

@app.post("/register")
def register_user(data: RegisterRequest, db: Session = Depends(get_db)):
    hashed = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt()).decode()
    user = User(username=data.username, hashed_password=hashed)
    db.add(user)
    db.commit()
    return {"message": "User created"}
