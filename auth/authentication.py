from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
from .schemas import UserInDB  # Ensure this is imported from your schema file

# Load environment variables
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "your-default-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Dummy database simulation (can be replaced with a real DB)
db = {
    "tim": {
        "username": "tim",
        "full_name": "tim ruscica",
        "email": "tim@gmail.com",
        "hashed_password": "$2b$12$FEx1pynReKqubcWcs0DWS.Wpq24bKOln40Izern3RkVae8nuClyIW",  # Example hashed password
        "disabled": False
    }
}

# Password hashing and verification
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# Function to retrieve user from the "database"
def get_user(username: str):
    if username in db:
        user_data = db[username]
        return UserInDB(**user_data)  # Convert the dictionary to a UserInDB object
    return None

# Function to authenticate user (check username and password)
def authenticate_user(username: str, password: str):
    user = get_user(username)
    if user is None:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

# JWT Token creation
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
