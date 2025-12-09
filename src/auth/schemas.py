from pydantic import BaseModel, EmailStr


class TokenResponse(BaseModel):
    """Token Response"""
    message: str = "Login successful"
    token: str
    # refresh_token: str
    token_type: str = "Bearer"


class Login(BaseModel):
    """Login user with email & password"""
    password: str
    email: EmailStr
