from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .authentication import  create_access_token , get_password_hash , verify_password , authenticate_user
from .schemas import TokenData, UserInDB, User, UserCreate , Token  # Adjust based on your actual class names in schema.py
from .utils import get_password_hash 

from . import db
import os
from datetime import timedelta
from .db import get_db
from sqlalchemy.orm import Session


router = APIRouter()

# OAuth2PasswordBearer allows token-based authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Signup endpoint
@router.post("/signup")
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the username already exists in the database
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # Hash the user's password
    hashed_password = get_password_hash(user.password)

    # Create a new User instance
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        disabled=False,
    )

    # Save the user to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"msg": "User created successfully", "id": new_user.id}

# Login endpoint
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}

