from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    goal: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str