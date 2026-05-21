from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional


class RegisterInSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=150)
    email: EmailStr
    password: str = Field(..., min_length=8)
    password_confirm: str = Field(..., min_length=8)

    @model_validator(mode='after')
    def check_passwords_match(self):
        if self.password != self.password_confirm:
            raise ValueError("Passwords do not match")
        return self


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class PasswordChangeInSchema(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=8)
    confirm_new_password: str

    @model_validator(mode="after")
    def verify_password_match(self):
        if self.new_password != self.confirm_new_password:
            raise ValueError("The two new passwords do not match.")
        return self


class UserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_admin: bool
    is_active: bool


class UserOutSchema(BaseModel):
    id: int
    username: str
    email: EmailStr

    user_type: str
    is_platform_admin: bool
