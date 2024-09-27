from sqlmodel import Field, SQLModel

class SubCategoryBase(SQLModel):
    sub_category: str | None = Field(
        None, max_length=50, description="sub category name, up to 50 characters"
    )

class SubCategory(SubCategoryBase, table=True):
    __tablename__ = "sub_categories"
    id: int | None = Field(None, primary_key=True)
    category_id: int


class SubCategoryCreate(SubCategoryBase):
    category_id: int


class SubCategoryRead(SubCategoryBase):
    id: int
    category_id: int


class SubCategoryUpdate(SubCategoryBase):
    category_id: int | None = None


