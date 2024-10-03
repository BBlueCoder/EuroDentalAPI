from pydantic import EmailStr, computed_field
from sqlmodel import SQLModel, Field
from fastapi import Form
from datetime import datetime


class ProductBase(SQLModel):
    product_name: str | None = Field(
        None, max_length=100, description="Product name, up to 100 characters"
    )
    description: str | None = Field(
        None, description="Description or notes about the product"
    )
    id_category: int | None = Field(None, description="id of the product's category", foreign_key="categories.id")
    id_sub_category: int | None = Field(None, description="id of the product's sub category",
                                        foreign_key="sub_categories.id")
    id_brand: int | None = Field(None, description="id of the product's band", foreign_key="brands.id")
    price: float | None = Field(None, description="Price of the product")
    stock_quantity: int | None = Field(None, description="Quantity of the product in stock")
    has_warranty: bool | None = Field(None, description="Indicates if the product has a warranty")
    warranty_duration_months: int | None = Field(None, description="Warranty duration in months")
    reference: str | None = Field(None, description="Product reference")
    image_id: int | None = Field(None, description="id of the product's image", foreign_key="images.id")


class Product(ProductBase, table=True):
    __tablename__ = "products"

    id: int | None = Field(None, primary_key=True)
    purchase_date: datetime | None = Field(None, description="Date of purchase")


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int
    purchase_date: datetime | None = Field(None, description="Date of purchase")

    @computed_field()
    @property
    def image_path(self) -> str | None:
        if self.image_id:
            return f"/images/{self.image_id}"
        return None


def parse_product_from_data_to_product_create(
        product_name: str | None = Form(
            None, max_length=100, description="Product name, up to 100 characters"
        ),
        description: str | None = Form(
            None, description="Description or notes about the product"
        ),
        id_category: int | None = Form(None, description="id of the product's category"),
        id_sub_category: int | None = Form(None, description="id of the product's sub category",
                                            foreign_key="sub_categories.id"),
        id_brand: int | None = Form(None, description="id of the product's band"),
        price: float | None = Form(None, description="Price of the product"),
        stock_quantity: int | None = Form(None, description="Quantity of the product in stock"),
        has_warranty: bool | None = Form(None, description="Indicates if the product has a warranty"),
        warranty_duration_months: int | None = Form(None, description="Warranty duration in months"),
        reference: str | None = Form(None, description="Product reference"),
        image_id: int | None = Form(None, description="id of the product's image")
):
    return ProductCreate(
        product_name=product_name,
        description=description,
        id_category=id_category,
        id_sub_category=id_sub_category,
        id_brand=id_brand,
        price=price,
        stock_quantity=stock_quantity,
        has_warranty=has_warranty,
        warranty_duration_months=warranty_duration_months,
        reference=reference,
        image_id=image_id
    )

def parse_product_from_data_to_product_update(
        product_name: str | None = Form(
            None, max_length=100, description="Product name, up to 100 characters"
        ),
        description: str | None = Form(
            None, description="Description or notes about the product"
        ),
        id_category: int | None = Form(None, description="id of the product's category"),
        id_sub_category: int | None = Form(None, description="id of the product's sub category",
                                            foreign_key="sub_categories.id"),
        id_brand: int | None = Form(None, description="id of the product's band"),
        price: float | None = Form(None, description="Price of the product"),
        stock_quantity: int | None = Form(None, description="Quantity of the product in stock"),
        has_warranty: bool | None = Form(None, description="Indicates if the product has a warranty"),
        warranty_duration_months: int | None = Form(None, description="Warranty duration in months"),
        reference: str | None = Form(None, description="Product reference"),
        image_id: int | None = Form(None, description="id of the product's image")
):
    return ProductUpdate(
        product_name=product_name,
        description=description,
        id_category=id_category,
        id_sub_category=id_sub_category,
        id_brand=id_brand,
        price=price,
        stock_quantity=stock_quantity,
        has_warranty=has_warranty,
        warranty_duration_months=warranty_duration_months,
        reference=reference,
        image_id=image_id
    )