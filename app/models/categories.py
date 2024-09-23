from sqlmodel import SQLModel, Field

class CategoryBase(SQLModel):
    category: str | None = Field(None, max_length=50, description="category name, up to 50 characters")


class Category(CategoryBase, table=True):
    __tablename__ = "categories"

    id: int | None = Field(None,primary_key=True)


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int
