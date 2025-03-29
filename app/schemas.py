from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    """
    Schema for user registration.
    """
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """
    Schema for returning user data.
    """
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True  # ORM compatibility

class Token(BaseModel):
    """
    Schema for access token response.
    """
    access_token: str
    refresh_token: str
    token_type: str

class UserLogin(BaseModel):
    """
    Schema for user login.
    """
    email: EmailStr
    password: str

