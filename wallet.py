from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .auth import get_db, get_current_user
from .models import User, Transaction
from .schemas import FundRequest, PayRequest, TransactionOut

router = APIRouter()

@router.post("/fund")
def fund_wallet(data: FundRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user.balance += data.amt
    db.add(Transaction(user_id=user.id, kind="credit", amt=data.amt, updated_bal=user.balance))
    db.commit()
    return {"balance": user.balance}

@router.post("/pay")
def pay_user(data: PayRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if user.balance < data.amt:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    recipient = db.query(User).filter_by(username=data.to).first()
    if not recipient:
        raise HTTPException(status_code=400, detail="Recipient not found")
    user.balance -= data.amt
    recipient.balance += data.amt
    db.add(Transaction(user_id=user.id, kind="debit", amt=data.amt, updated_bal=user.balance))
    db.add(Transaction(user_id=recipient.id, kind="credit", amt=data.amt, updated_bal=recipient.balance))
    db.commit()
    return {"balance": user.balance}

@router.get("/stmt", response_model=list[TransactionOut])
def get_statement(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    txns = db.query(Transaction).filter_by(user_id=user.id).order_by(Transaction.timestamp.desc()).all()
    return txns
