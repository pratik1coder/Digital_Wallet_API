import base64, bcrypt
from fastapi import HTTPException, Request, Depends
from sqlalchemy.orm import Session
from .db import SessionLocal
from .models import User

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(request: Request, db: Session = Depends(get_db)):
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Basic "):
        raise HTTPException(status_code=401, detail="Invalid Authorization")
    decoded = base64.b64decode(auth[6:]).decode()
    username, password = decoded.split(":")
    user = db.query(User).filter_by(username=username).first()
    if not user or not bcrypt.checkpw(password.encode(), user.hashed_password.encode()):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user
