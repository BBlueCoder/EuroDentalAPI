from fastapi import Form
from sqlmodel import Field, SQLModel

class ProductAddQuantity(SQLModel):
    reference: str = Field(..., description="Product reference", unique=True)
    stock_quantity: int = Field(
        ..., description="Quantity of the product to increase"
    )

class ProductBase(SQLModel):
    product_name: str | None = Field(
        None, max_length=100, description="Product name, up to 100 characters"
    )
    description: str | None = Field(
        None, description="Description or notes about the product"
    )

    price: float | None = Field(None, description="Price of the product")
    stock_quantity: int | None = Field(
        0, description="Quantity of the product in stock"
    )
    has_warranty: bool | None = Field(
        None, description="Indicates if the product has a warranty"
    )
    warranty_duration_months: int | None = Field(
        None, description="Warranty duration in months"
    )
    image_id: int | None = Field(
        None, description="id of the product's image", foreign_key="images.id"
    )


class ProductBaseWithIDs(ProductBase):
    id_category: int | None = Field(
        None, description="id of the product's category", foreign_key="categories.id"
    )
    id_sub_category: int | None = Field(
        None,
        description="id of the product's sub category",
        foreign_key="sub_categories.id",
    )
    id_brand: int | None = Field(
        None, description="id of the product's band", foreign_key="brands.id"
    )


class Product(ProductBaseWithIDs, table=True):
    __tablename__ = "products"

    id: int | None = Field(None, primary_key=True)
    reference: str = Field(..., description="Product reference", unique=True)


class ProductCreate(ProductBaseWithIDs):
    reference: str = Field(..., description="Product reference", unique=True),


class ProductUpdate(ProductBaseWithIDs):
    reference: str | None = Field(None, description="Product reference", unique=True)


class ProductRead(ProductBaseWithIDs):
    id: int
    reference: str = Field(..., description="Product reference", unique=True)

    image_path: str | None = None
    category_name: str | None = None
    sub_category_name: str | None = None
    brand_name: str | None = None


def parse_product_from_data_to_product_create(
    product_name: str | None = Form(
        None, max_length=100, description="Product name, up to 100 characters"
    ),
    description: str | None = Form(
        None, description="Description or notes about the product"
    ),
    id_category: int | None = Form(None, description="id of the product's category"),
    id_sub_category: int | None = Form(
        None,
        description="id of the product's sub category",
        foreign_key="sub_categories.id",
    ),
    id_brand: int | None = Form(None, description="id of the product's band"),
    price: float | None = Form(None, description="Price of the product"),
    stock_quantity: int | None = Form(
        None, description="Quantity of the product in stock"
    ),
    has_warranty: bool | None = Form(
        None, description="Indicates if the product has a warranty"
    ),
    warranty_duration_months: int = Form(
        0, description="Warranty duration in months"
    ),
    reference: str = Form(..., description="Product reference"),
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
    )


def parse_product_from_data_to_product_update(
    product_name: str | None = Form(
        None, max_length=100, description="Product name, up to 100 characters"
    ),
    description: str | None = Form(
        None, description="Description or notes about the product"
    ),
    id_category: int | None = Form(None, description="id of the product's category"),
    id_sub_category: int | None = Form(
        None,
        description="id of the product's sub category",
        foreign_key="sub_categories.id",
    ),
    id_brand: int | None = Form(None, description="id of the product's band"),
    price: float | None = Form(None, description="Price of the product"),
    stock_quantity: int | None = Form(
        None, description="Quantity of the product in stock"
    ),
    has_warranty: bool | None = Form(
        None, description="Indicates if the product has a warranty"
    ),
    warranty_duration_months: int | None = Form(
        None, description="Warranty duration in months"
    ),
    reference: str | None = Form(None, description="Product reference"),
):
    product_update = ProductUpdate()
    if product_name:
        product_update.product_name = product_name
    if description:
        product_update.description = description
    if id_category:
        product_update.id_category = id_category
    if id_sub_category:
        product_update.id_sub_category = id_sub_category
    if id_brand:
        product_update.id_brand = id_brand
    if price:
        product_update.price = price
    if stock_quantity:
        product_update.stock_quantity = stock_quantity
    if has_warranty:
        product_update.has_warranty = has_warranty
    if warranty_duration_months:
        product_update.warranty_duration_months = warranty_duration_months
    if reference:
        product_update.reference = reference

    return product_update
