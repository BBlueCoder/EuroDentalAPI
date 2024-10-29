from datetime import date, datetime

from sqlmodel import Field, SQLModel

from app.models.products import ProductRead, Product


class TaskProductBase(SQLModel):
    price: float | None = Field(None, description="Price of the product")
    quantity: int | None = Field(1, description="Quantity of the product")


class TaskProduct(TaskProductBase, table=True):
    __tablename__ = "task_products"
    product_reference: str | None = Field(None, foreign_key="products.reference")
    id: int | None = Field(None, primary_key=True)
    task_id: int | None = Field(None, foreign_key="tasks.id")
    purchase_date: datetime = Field(
        datetime.now(),
        description="Date the task product is scheduled or created.",
    )


class TaskProductCreate(TaskProductBase):
    product_reference: str = Field(..., unique=True, foreign_key="products.reference")
    task_id: int = Field(..., foreign_key="tasks.id")


class TaskProductUpdate(TaskProductBase):
    product_reference: str | None = Field(None, foreign_key="products.reference")
    task_id: int | None = Field(None, foreign_key="tasks.id")


class TaskProductRead(TaskProductBase):
    product_reference: str
    id: int
    task_id: int
    purchase_date: datetime

class TaskProductUpdateQuantity(SQLModel):
    new_quantity : float

class TaskProductsDetails(TaskProductRead):
    product_details : ProductRead | None = None
