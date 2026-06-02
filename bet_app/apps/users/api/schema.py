from django.urls import reverse
from ninja import ModelSchema, Schema
from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional

from bet_app.apps.users.models import User


class RegisterSchema(Schema):
    username: str = Field(..., min_length=3, max_length=150)
    email: EmailStr
    password: str = Field(..., min_length=8)


class LoginSchema(Schema):
    email: str
    password: str


class PasswordChangeSchema(Schema):
    old_password: str
    new_password: str = Field(..., min_length=8)
    confirm_new_password: str

    @model_validator(mode="after")
    def verify_password_match(self):
        if self.new_password != self.confirm_new_password:
            raise ValueError("The two new passwords do not match.")
        return self


class UserOutSchema(Schema):
    id: int
    username: str
    email: EmailStr

    user_type: str
    is_platform_admin: bool


class UpdateUserSchema(ModelSchema):
    class Meta:
        model = User
        fields = ["username", "email"]


class UserSchema(ModelSchema):
    url: str

    class Meta:
        model = User
        fields = ["username", "email"]

    @staticmethod
    def resolve_url(obj: User):
        return reverse("api:retrieve_user", kwargs={"username": obj.username})
