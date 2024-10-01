from sqlmodel import Field, SQLModel


class BrandBase(SQLModel):
    brand: str  = Field(
        ..., max_length=50, description="brand name, up to 50 characters"
    )


class Brand(BrandBase, table=True):
    __tablename__ = "brands"

    id: int | None = Field(None, primary_key=True)


class BrandCreate(BrandBase):
    pass


class BrandRead(BrandBase):
    id: int