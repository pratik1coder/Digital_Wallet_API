from fastapi import APIRouter, Depends, HTTPException
from .auth import get_current_user, get_db
from .models import Product, User, Transaction
from .schemas import ProductCreate, BuyRequest

router = APIRouter()

@router.post("/product")
def add_product(data: ProductCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    product = Product(**data.dict())
    db.add(product)
    db.commit()
    return {"id": product.id, "message": "Product added"}

@router.get("/product")
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@router.post("/buy")
def buy_product(data: BuyRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    product = db.query(Product).filter_by(id=data.product_id).first()
    if not product or user.balance < product.price:
        raise HTTPException(status_code=400, detail="Insufficient balance or invalid product")
    user.balance -= product.price
    db.add(Transaction(user_id=user.id, kind="debit", amt=product.price, updated_bal=user.balance))
    db.commit()
    return {"message": "Product purchased", "balance": user.balance}
