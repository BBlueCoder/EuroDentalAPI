from sqlmodel import Session, select
from starlette.requests import Request

from app.controllers.BaseController import BaseController
from app.models.brands import Brand
from app.models.categories import Category
from app.models.products import Product, ProductCreate, ProductUpdate
from app.models.sub_categories import SubCategory
from app.utils.image_utils import add_image_to_entity
from app.utils.map_model_to_model_read import model_to_model_read


class ProductsController(BaseController):
    statement = (
        select(Product, Category, SubCategory, Brand)
        .join(Category, isouter=True)
        .join(SubCategory, isouter=True)
        .join(Brand, isouter=True)
    )

    def __init__(self, session: Session, req : Request | None = None):
        super().__init__(session, Product)
        self.req = req

    def map_to_product_read(self, products):
        mapped_products = []
        for product, category, sub_category, brand in products:
            product_read = model_to_model_read(product, self.req)
            if category:
                product_read.category_name = category.category

            if sub_category:
                product_read.sub_category_name = sub_category.sub_category

            if brand:
                product_read.brand_name = brand.brand

            mapped_products.append(product_read)

        return mapped_products

    async def get_products(self):
        return await super().get_and_join_items(self.statement,self.map_to_product_read)

    async def get_product_with_details_by_id(self, product_id):
        res = await super().get_and_join_items(self.statement.where(Product.id == product_id),self.map_to_product_read,is_first=True)
        return res[0]

    async def get_product_by_id(self,product_id):
        return await self.get_product_with_details_by_id(product_id)

    async def create_product(self, product : ProductCreate, image):
        product = await add_image_to_entity(product,self.session, image)
        db_product = await super().create_item(product)
        return await self.get_product_with_details_by_id(db_product.id)

    async def update_product(self, product : ProductUpdate, product_id : int, image):
        product = await add_image_to_entity(product, self.session, image)
        db_product = await super().update_item(updated_item=product, item_id=product_id)
        return await self.get_product_with_details_by_id(db_product.id)


    async def delete_product(self, product_id : int):
        await super().delete_item(item_id=product_id)