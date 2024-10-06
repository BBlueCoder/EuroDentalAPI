from datetime import date, datetime
from sqlmodel import Field, SQLModel


class TaskProductBase(SQLModel):
    price: float | None = Field(None, description="Price of the product")
    purchase_date: date | None = Field(
        datetime.now().date(),
        description="Date the task product is scheduled or created.",
    )
    quantity: int | None = Field(1, description="Quantity of the product")


class TaskProduct(TaskProductBase, table=True):
    __tablename__ = "task_products"
    product_reference: str | None = Field(None, foreign_key="products.reference")
    id: int | None = Field(None, primary_key=True)
    task_id: int | None = Field(None, foreign_key="tasks.id")


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
