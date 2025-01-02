from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from datetime import datetime, timedelta, timezone
import random
from .db import get_db
from .utils import get_password_hash

router = APIRouter()

# Temporary storage for verification codes
verification_codes = {}

@router.post("/password-reset/request")
async def request_password_reset(email: str, background_tasks: BackgroundTasks):
    # Fetch the user from the database
    user = next((user for user in get_db.values() if user["email"] == email), None)
    
    # If user is not found, raise HTTPException
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found",
        )

    # Generate a 6-digit verification code
    verification_code = str(random.randint(100000, 999999))
    
    # Set expiration time for the code (10 minutes from now)
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=10)
    
    # Store the code and expiration time in temporary storage
    verification_codes[email] = {
        "code": verification_code,
        "expires_at": expiration_time,
    }

    # Log the verification code (you can replace this with an actual email service)
    background_tasks.add_task(
        print, f"Verification code for {email}: {verification_code}"
    )
    
    return {"message": "Verification code sent. Please check your email."}

@router.post("/password-reset/verify")
async def verify_reset_code(email: str, verification_code: str):
    # Check if there is a reset request for the email
    if email not in verification_codes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No reset request found for this email.",
        )

    # Retrieve the stored code and expiration time
    stored_code_data = verification_codes[email]
    
    # Check if the provided code matches the stored code
    if stored_code_data["code"] != verification_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification code.",
        )

    # Check if the verification code has expired
    if datetime.now(timezone.utc) > stored_code_data["expires_at"]:
        # Remove the expired code from temporary storage
        verification_codes.pop(email, None)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification code has expired.",
        )

    return {"message": "Verification successful. You may now reset your password."}

@router.post("/password-reset/confirm")
async def reset_password(email: str, new_password: str):
    # Check if there was a valid reset request
    if email not in verification_codes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No verified reset request found for this email.",
        )

    # Fetch the user from the database
    user = next((user for user in get_db.values() if user["email"] == email), None)
    
    # If the user is not found, raise HTTPException
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    # Hash the new password
    hashed_password = get_password_hash(new_password)
    
    # Update the user's password in the database
    get_db[user["username"]]["hashed_password"] = hashed_password
    
    # Remove the verification code after the password reset
    verification_codes.pop(email, None)
    
    return {"message": "Password has been successfully reset."}

