from typing import TypeVar, Type

from fastapi import HTTPException
from sqlmodel import Session, asc, select

from app.errors.item_not_found import ItemNotFound
from app.models.brands import Brand
from app.models.categories import Category
from app.models.clients import Client
from app.models.products import Product
from app.models.profiles import Profile
from app.models.rights import Right
from app.models.sub_categories import SubCategory
from app.models.task_products import TaskProduct
from app.models.tasks import Task
from app.models.users import User

Entity = TypeVar(
    "Entity",
    bound=Type[Brand] | Type[Category] | Type[Client] | Type[Product] | Type[Profile] | Type[SubCategory] | Type[
        TaskProduct] | Type[Task] | Type[User] | Type[Right]
)


class BaseController:
    def __init__(self, session: Session, entity: Entity, not_found_exc = ItemNotFound()):
        self.session = session
        self.entity = entity
        self.not_found_exc = not_found_exc

    async def get_items_all(self):
        return self.session.exec(select(self.entity)).all()

    async def get_first_item_by_id(self, item_id: int):
        return await self.get_first_item_with_condition(self.entity.id,item_id)

    async def get_first_item_with_condition(self, condition, condition_val):
        item = self.session.exec(select(self.entity).where(condition == condition_val)).first()
        if not item:
            raise self.not_found_exc
        return item

    async def get_items_with_condition(self,condition, condition_val):
        return self.session.exec(select(self.entity).where(condition == condition_val).order_by(asc(self.entity.id))).all()

    async def get_and_join_items(self, join_statement, map_fun,is_first : bool = False):
        res = self.session.exec(join_statement).all()
        if is_first and len(res) == 0:
            raise self.not_found_exc

        if map_fun:
            return map_fun(res)

        return res


    async def create_item(self, item):
        db_item = self.entity.model_validate(item)
        self.session.add(db_item)
        self.session.commit()
        self.session.refresh(db_item)
        return db_item

    async def update_item(self, updated_item, item_id):
        db_item = await self.get_first_item_by_id(item_id)
        item_data = updated_item.model_dump(exclude_unset=True)
        db_item.sqlmodel_update(item_data)
        self.session.add(db_item)
        self.session.commit()
        self.session.refresh(db_item)
        return db_item

    async def delete_item(self, item_id):
        item = await self.get_first_item_by_id(item_id)
        self.session.delete(item)
        self.session.commit()
