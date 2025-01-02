from pydantic import BaseModel
from typing import Optional

# User model for displaying user info
class User(BaseModel):
    username: str
    full_name: Optional[str] = None
    email: Optional[str] = None

# UserCreate model for signup (including password)
class UserCreate(User):
    password: str

# UserInDB model that includes hashed password (used for database operations)
class UserInDB(UserCreate):
    hashed_password: str

# Token model for JWT response
class Token(BaseModel):
    access_token: str
    token_type: str

# TokenData model to store the token's decoded info
class TokenData(BaseModel):
    username: str


