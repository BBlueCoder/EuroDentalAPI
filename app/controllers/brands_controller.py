from sqlmodel import Session

from app.controllers.BaseController import BaseController
from app.models.brands import Brand, BrandCreate


class BrandsController(BaseController):
    def __init__(self, session: Session):
        super().__init__(session, Brand)

    async def get_brands(self):
        return await super().get_items_all()

    async def get_brand_by_id(self,brand_id):
        return await super().get_first_item_by_id(item_id=brand_id)

    async def create_brand(self, brand : BrandCreate):
        return await super().create_item(brand)

    async def update_brand(self, brand : BrandCreate, brand_id : int):
        return await super().update_item(updated_item=brand, item_id=brand_id)

    async def delete_brand(self, brand_id : int):
        await super().delete_item(item_id=brand_id)
