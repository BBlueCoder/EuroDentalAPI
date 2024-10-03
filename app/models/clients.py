from typing import Any

from pydantic import EmailStr, computed_field
from sqlmodel import Field, SQLModel
from fastapi import Form
from starlette.requests import Request

from app.utils.global_utils import generate_the_address


class ClientBase(SQLModel):
    first_name: str | None = Field(
        None, max_length=100, description="First name, up to 100 characters"
    )
    last_name: str | None = Field(
        None, max_length=100, description="Last name, up to 100 characters"
    )
    phone_number: str | None = Field(
        None, min_length=10, max_length=10, description="Phone number, 10 digits"
    )
    address: str | None = Field(None, description="Address of the client")
    city: str | None = Field(None, description="City where the client resides")
    fixed_phone_number: str | None = Field(None, description="Fixed phone number")
    description: str | None = Field(
        None, description="Description or notes about the client"
    )
    image_id: int | None = Field(None, description="id of the client's image",foreign_key="images.id")



class Client(ClientBase, table=True):
    __tablename__ = "clients"

    email: EmailStr = Field(..., description="Email address, must be unique")
    id: int | None = Field(None, primary_key=True)


class ClientCreate(ClientBase):
    email: EmailStr = Field(..., description="Email address, must be unique")


class ClientUpdate(ClientBase):
    pass


class ClientRead(ClientBase):
    id: int
    email: EmailStr = Field(..., description="Email address, must be unique")
    image_path : str | None = None


def parse_client_from_date_to_client_create(
        first_name: str | None = Form(
            None, max_length=100, description="First name, up to 100 characters"
        ),
        last_name: str | None = Form(
            None, max_length=100, description="Last name, up to 100 characters"
        ),
        phone_number: str | None = Form(
            None, min_length=10, max_length=10, description="Phone number, 10 digits"
        ),
        address: str | None = Form(None, description="Address of the client"),
        city: str | None = Form(None, description="City where the client resides"),
        fixed_phone_number: str | None = Form(None, description="Fixed phone number"),
        description: str | None = Form(
            None, description="Description or notes about the client"
        ),
        email: EmailStr = Form(..., description="Email address, must be unique")
):
    return ClientCreate(
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
        address=address,
        city=city,
        fixed_phone_number=fixed_phone_number,
        description=description,
        email=email
    )

def parse_client_from_date_to_client_update(
        first_name: str | None = Form(
            None, max_length=100, description="First name, up to 100 characters"
        ),
        last_name: str | None = Form(
            None, max_length=100, description="Last name, up to 100 characters"
        ),
        phone_number: str | None = Form(
            None, min_length=10, max_length=10, description="Phone number, 10 digits"
        ),
        address: str | None = Form(None, description="Address of the client"),
        city: str | None = Form(None, description="City where the client resides"),
        fixed_phone_number: str | None = Form(None, description="Fixed phone number"),
        description: str | None = Form(
            None, description="Description or notes about the client"
        ),
        image_id : int | None = None
):
    return ClientUpdate(
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
        address=address,
        city=city,
        fixed_phone_number=fixed_phone_number,
        description=description,
        image_id=image_id
    )

def client_to_client_read(client : Client, req : Request):
    client_dic = client.model_dump()
    if client_dic["image_id"]:
        client_dic["image_path"] = generate_the_address(req, f"/images/{client_dic["image_id"]}")
    return ClientRead(**client_dic)

