from sqlmodel import Session

from app.controllers.BaseController import BaseController
from app.models.sub_categories import SubCategory, SubCategoryCreate, SubCategoryUpdate


class SubCategoriesController(BaseController):
    def __init__(self, session: Session):
        super().__init__(session, SubCategory)

    async def get_sub_categories(self, category_id : int | None = None):
        if category_id:
            return await super().get_items_with_condition(SubCategory.category_id,category_id)

        return await super().get_items_all()

    async def get_sub_category_by_id(self,sub_category_id):
        return await super().get_first_item_by_id(item_id=sub_category_id)

    async def create_sub_category(self, sub_category : SubCategoryCreate):
        return await super().create_item(sub_category)

    async def update_sub_category(self, sub_category : SubCategoryUpdate, sub_category_id : int):
        return await super().update_item(updated_item=sub_category, item_id=sub_category_id)

    async def delete_sub_category(self, sub_category_id : int):
        await super().delete_item(item_id=sub_category_id)
