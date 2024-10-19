from sqlmodel import Session

from app.controllers.BaseController import BaseController
from app.models.categories import Category, CategoryCreate


class CategoriesController(BaseController):
    def __init__(self, session: Session):
        super().__init__(session, Category)

    async def get_categories(self):
        return await super().get_items_all()

    async def get_category_by_id(self,category_id):
        return await super().get_first_item_by_id(item_id=category_id)

    async def create_category(self, category : CategoryCreate):
        return await super().create_item(category)

    async def update_category(self, category : CategoryCreate, category_id : int):
        return await super().update_item(updated_item=category, item_id=category_id)

    async def delete_category(self, category_id : int):
        await super().delete_item(item_id=category_id)
