from sqlmodel import Session

from app.controllers.BaseController import BaseController
from app.models.task_products import TaskProduct, TaskProductCreate, TaskProductUpdate


class TaskProductController(BaseController):
    def __init__(self, session: Session):
        super().__init__(session, TaskProduct)

    async def get_task_products(self):
        return await super().get_items_all()

    async def get_task_product_by_id(self,task_product_id):
        return await super().get_first_item_by_id(item_id=task_product_id)

    async def get_all_task_products_for_a_task(self, task_id):
        return await super().get_items_with_condition(TaskProduct.task_id, task_id)

    async def create_task_product(self, task_product : TaskProductCreate):
        return await super().create_item(task_product)

    async def update_task_product(self, task_product : TaskProductUpdate, task_product_id : int):
        return await super().update_item(updated_item=task_product, item_id=task_product_id)

    async def delete_task_product(self, task_product_id : int):
        await super().delete_item(item_id=task_product_id)
