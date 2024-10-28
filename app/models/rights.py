from sqlmodel import SQLModel, Field


class RightBase(SQLModel):
    invoices_read: bool | None = Field(
        False, description="Indicates if the profile has the right to read invoices"
    )
    invoices_write: bool | None = Field(
        False, description="Indicates if the profile has the right to update invoices"
    )
    clients_read: bool | None = Field(
        False, description="Indicates if the profile has the right to read clients"
    )
    clients_write: bool | None = Field(
        False, description="Indicates if the profile has the right to update clients"
    )
    products_read: bool | None = Field(
        False, description="Indicates if the profile has the right to read products"
    )
    products_write: bool | None = Field(
        False, description="Indicates if the profile has the right to update products"
    )
    tasks_read: bool | None = Field(
        False, description="Indicates if the profile has the right to read tasks"
    )
    tasks_write: bool | None = Field(
        False, description="Indicates if the profile has the right to update tasks"
    )
    users_read: bool | None = Field(
        False, description="Indicates if the profile has the right to read users"
    )
    users_write: bool | None = Field(
        False, description="Indicates if the profile has the right to update users"
    )
    mobile_tasks_read: bool | None = Field(
        False, description="Indicates if the profile has the right to read tasks in the mobile app"
    )
    mobile_tasks_write: bool | None = Field(
        False, description="Indicates if the profile has the right to update tasks in the mobile app"
    )
    mobile_stock_read: bool | None = Field(
        False, description="Indicates if the profile has the right to read stock in the mobile app"
    )
    mobile_stock_write: bool | None = Field(
        False, description="Indicates if the profile has the right to update stock in the mobile app"
    )
    

class RightBaseWithIDs(RightBase):
    id_profile: int | None = Field(
        None, description="id of the profile", foreign_key="profiles.id"
    )


class Right(RightBaseWithIDs, table=True):
    __tablename__ = "rights"

    id: int | None = Field(None, primary_key=True)

class RightRead(RightBaseWithIDs):
    id: int

    profile_name: str | None = None

class RightCreate(RightBaseWithIDs):
    pass


