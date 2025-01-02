import sys
import os
from fastapi import FastAPI
from dotenv import load_dotenv
from .db import engine, Base, check_tables
from auth.routes import router as auth_router  # Import auth router here
from stock.routes import router as stock_router  # Import stock router here

 # Import password reset router

app = FastAPI()

# Load environment variables
load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

# Include your authentication routes
app.include_router(auth_router, prefix="/auth", tags=["auth"])

# Include your stock routes
app.include_router(stock_router, prefix="/stock", tags=["stock"])

# Include password reset routes if applicable
app.include_router(auth_router, prefix="/password-reset", tags=["password-reset"])

check_tables()

@app.get("/")
async def root():
    return {"message": "Welcome to the API!"}

