from fastapi import Form
from pydantic import EmailStr, computed_field
from sqlmodel import Field, SQLModel

from app.utils.global_utils import hash_password


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
    is_blocked: bool | None = Field(
        None, description="Indicates if the user is blocked"
    )
    image_id: int | None = Field(
        None, description="id of the client's image", foreign_key="images.id"
    )


class User(UserBase, table=True):
    __tablename__ = "users"

    id: int | None = Field(None, primary_key=True)
    email: EmailStr = Field(..., description="Email address, must be unique")
    profile_id: int = Field(..., foreign_key="profiles.id")
    password_hash: str = Field(
        ..., max_length=255, description="Password, up to 255 characters"
    )


class UserCreate(UserBase):
    email: EmailStr = Field(..., description="Email address, must be unique")
    password_hash: str = Field(
        ..., max_length=255, description="Password, up to 255 characters"
    )
    profile_id: int = Field(..., foreign_key="profiles.id")


class UserUpdate(UserBase):
    password_hash: str | None = Field(
        None, max_length=255, description="Password, up to 255 characters"
    )
    profile_id: int | None = Field(None, foreign_key="profiles.id")
    email: EmailStr | None = (Form(default=None),)


class UserRead(UserBase):
    id: int
    email: EmailStr = Field(..., description="Email address, must be unique")
    image_path: str | None = None
    profile_id: int = Field(..., foreign_key="profiles.id")


class UserByProfile(SQLModel):
    id: int
    image_path: str | None = None
    full_name: str | None = None


class UserLogin(SQLModel):
    email: EmailStr = Field(..., description="Email address, must be unique")
    password: str = Field(
        ..., max_length=255, description="Password, up to 255 characters"
    )


def parse_user_from_data_to_user_create(
    first_name: str | None = Form(
        None, max_length=100, description="First name, up to 100 characters"
    ),
    last_name: str | None = Form(
        None, max_length=100, description="Last name, up to 100 characters"
    ),
    password: str = Form(
        ..., max_length=255, description="Password, up to 255 characters"
    ),
    phone_number: str | None = Form(
        None, min_length=10, max_length=10, description="Phone number, 10 digits"
    ),
    is_blocked: bool | None = Form(
        None, description="Indicates if the user is blocked"
    ),
    profile_id: int = Form(..., foreign_key="profiles.id"),
    email: EmailStr = Form(..., description="Email address, must be unique"),
):
    return UserCreate(
        first_name=first_name,
        last_name=last_name,
        password_hash=hash_password(password),
        phone_number=phone_number,
        is_blocked=is_blocked,
        profile_id=profile_id,
        email=email,
    )


def parse_user_from_data_to_user_update(
    first_name: str | None = Form(
        None, max_length=100, description="First name, up to 100 characters"
    ),
    last_name: str | None = Form(
        None, max_length=100, description="Last name, up to 100 characters"
    ),
    password: str | None = Form(
        None, max_length=255, description="Password, up to 255 characters"
    ),
    phone_number: str | None = Form(
        None, min_length=10, max_length=10, description="Phone number, 10 digits"
    ),
    is_blocked: bool | None = Form(
        None, description="Indicates if the user is blocked"
    ),
    email: EmailStr | None = Form(default=None),
    profile_id: int | None = Form(None, foreign_key="profiles.id"),
):
    user_update = UserUpdate()
    if first_name:
        user_update.first_name = first_name
    if last_name:
        user_update.last_name = last_name
    if password:
        user_update.password_hash = hash_password(password)
    if phone_number:
        user_update.phone_number = phone_number
    if is_blocked:
        user_update.is_blocked = is_blocked
    if email:
        user_update.email = email
    if profile_id:
        user_update.profile_id = profile_id

    return user_update
