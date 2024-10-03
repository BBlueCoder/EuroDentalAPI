from pydantic import EmailStr, computed_field
from sqlmodel import SQLModel, Field
from fastapi import Form
from datetime import datetime

from starlette.requests import Request

from app.utils.global_utils import generate_the_address, hash_password


class UserBase(SQLModel):
    first_name: str | None = Field(
        None, max_length=100, description="First name, up to 100 characters"
    )
    last_name: str | None = Field(
        None, max_length=100, description="Last name, up to 100 characters"
    )
    phone_number: str | None = Field(
        None, min_length=10, max_length=10, description="Phone number, 10 digits"
    )
    is_blocked: bool | None = Field(None, description="Indicates if the user is blocked")
    image_id: int | None = Field(None, description="id of the client's image", foreign_key="images.id")


class User(UserBase, table=True):
    __tablename__ = "users"

    id: int | None = Field(None, primary_key=True)
    email: EmailStr = Field(..., description="Email address, must be unique")
    profile_id: int = Field(..., foreign_key="profiles.id")
    password_hash: str = Field(
        ..., max_length=255, description="Last name, up to 255 characters"
    )


class UserCreate(UserBase):
    email: EmailStr = Field(..., description="Email address, must be unique")
    password_hash: str = Field(
        ..., max_length=255, description="Last name, up to 255 characters"
    )
    profile_id: int = Field(..., foreign_key="profiles.id")


class UserUpdate(UserBase):
    password_hash: str | None = Field(
        None, max_length=255, description="Last name, up to 255 characters"
    )
    profile_id: int | None = Field(None, foreign_key="profiles.id")


class UserRead(UserBase):
    id: int
    email: EmailStr = Field(..., description="Email address, must be unique")
    image_path: str | None = None
    profile_id: int = Field(..., foreign_key="profiles.id")


def parse_user_from_data_to_user_create(
        first_name: str | None = Form(
            None, max_length=100, description="First name, up to 100 characters"
        ),
        last_name: str | None = Form(
            None, max_length=100, description="Last name, up to 100 characters"
        ),
        password: str = Form(
            ..., max_length=255, description="Last name, up to 255 characters"
        ),
        phone_number: str | None = Form(
            None, min_length=10, max_length=10, description="Phone number, 10 digits"
        ),
        is_blocked: bool | None = Form(None, description="Indicates if the user is blocked"),
        profile_id: int = Form(..., foreign_key="profiles.id"),
        email: EmailStr = Form(..., description="Email address, must be unique")

):
    return UserCreate(
        first_name=first_name,
        last_name=last_name,
        password_hash=hash_password(password),
        phone_number=phone_number,
        is_blocked=is_blocked,
        profile_id=profile_id,
        email=email
    )


def parse_user_from_data_to_user_update(
        first_name: str | None = Form(
            None, max_length=100, description="First name, up to 100 characters"
        ),
        last_name: str | None = Form(
            None, max_length=100, description="Last name, up to 100 characters"
        ),
        password: str | None = Form(
            None, max_length=255, description="Last name, up to 255 characters"
        ),
        phone_number: str | None = Form(
            None, min_length=10, max_length=10, description="Phone number, 10 digits"
        ),
        is_blocked: bool | None = Form(None, description="Indicates if the user is blocked"),
):
    if password:
        return UserUpdate(
            first_name=first_name,
            last_name=last_name,
            password_hash=hash_password(password),
            phone_number=phone_number,
            is_blocked=is_blocked
        )
    return UserUpdate(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            is_blocked=is_blocked
        )

def user_to_user_read(user: User, req: Request):
    user_dic = user.model_dump()
    if user_dic["image_id"]:
        user_dic["image_path"] = generate_the_address(req, f"/images/{user_dic["image_id"]}")
    return UserRead(**user_dic)
