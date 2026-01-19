from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    goal: str


# class LoginRequest(BaseModel):
#    email: EmailStr
#    password: str


class AuthResponse(BaseModel):
    # access_token: str
    # token_type: str
    email: EmailStr
    # goal: str
    subscription_tier: str
    workspace_limit: int 
    current_workspace_id: str
