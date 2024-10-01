from sqlmodel import SQLModel, Field


class ImageBase(SQLModel):
    image_name : str

class Image(ImageBase, table=True):
    __tablename__ = "images"
    id : int | None = Field(None, primary_key=True)

class ImageCreate(ImageBase):
    pass