from pydantic import EmailStr
from sqlmodel import Field, SQLModel


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


class Client(ClientBase, table=True):
    __tablename__ = "clients"

    email: EmailStr = Field(..., description="Email address, must be unique")
    id: int | None = Field(None, primary_key=True)
    image_path: str | None = Field(None, description="Path to the client's image")


class ClientCreate(ClientBase):
    email: EmailStr = Field(..., description="Email address, must be unique")


class ClientUpdate(ClientBase):
    email: str | None = None


class ClientRead(ClientBase):
    id: int
    image_path: str | None = Field(None, description="Path to the client's image")
    email: EmailStr = Field(..., description="Email address, must be unique")
