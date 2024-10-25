from sqlmodel import Session, select, and_, desc, asc, update

from app.controllers.BaseController import BaseController
from app.models.clients import Client
from app.models.task_products import TaskProduct
from app.models.tasks import Task, TaskCreate, TaskUpdate, TaskRead, TaskFilterParams, Status
from app.models.tasks_assignment import TasksAssignment
from app.models.users import User
from app.utils.global_utils import generate_the_address


class TasksController(BaseController):
    statement = (
        select(Task, Client, User, TaskProduct)
        .join(Client, isouter=True)
        .join(User, User.id == Task.technician_id, isouter=True)
        .join(TaskProduct, isouter=True)
        # .join(Product, TaskProduct.product_reference == Product.reference, isouter=True)
    )

    def __init__(self, session: Session, req = None, current_user : User = None):
        super().__init__(session, Task)
        self.req = req
        self.current_user = current_user

    def map_to_task_read(self, tasks):
        mapped_results: list[TaskRead] = []

        for task, client, user, task_product in tasks:
            task_read = TaskRead(**task.model_dump())
            if client:
                task_read.client = f"{client.last_name} {client.first_name}"
                if client.image_id:
                    task_read.client_image = generate_the_address(
                        self.req, f"/images/{client.image_id}"
                    )

            if user:
                task_read.technician = f"{user.last_name} {user.first_name}"
                if user.image_id:
                    task_read.technician_image = generate_the_address(
                        self.req, f"/images/{user.image_id}"
                    )

            # if product:
            #     if product.id_category:
            #         task_read.id_category = product.id_category
            #     if product.id_sub_category:
            #         task_read.id_sub_category = product.id_sub_category
            #     if product.id_brand:
            #         task_read.id_brand = product.id_brand

            mapped_results.append(task_read)

        return mapped_results


    async def get_tasks(self, filter_params : TaskFilterParams):
        _statement = self.statement
        if filter_params.exact_date:
            _statement = self.statement.where(Task.task_date == filter_params.exact_date)
        elif filter_params.date_range_start and filter_params.date_range_end:
            _statement = self.statement.where(
                and_(
                    Task.task_date >= filter_params.date_range_start,
                    Task.task_date <= filter_params.date_range_end,
                )
            )

        order_by = (
            Task.task_date
            if filter_params.order_by == "task_date"
            else (
                Task.task_name
                if filter_params.order_by == "task_name"
                else Task.task_type
            )
        )
        sort_by = desc(order_by) if filter_params.sort == "desc" else asc(order_by)

        _statement = _statement.order_by(sort_by)

        return await super().get_and_join_items(_statement,self.map_to_task_read)

    async def get_task_with_details_by_id(self, task_id):
        res = await super().get_and_join_items(self.statement.where(Task.id == task_id),self.map_to_task_read,is_first=True)
        return res[0]

    async def get_task_by_id(self,task_id):
        return await self.get_task_with_details_by_id(task_id)

    async def create_task(self, task : TaskCreate):
        if not task.create_by:
            task.create_by = self.current_user.id
        if task.technician_id:
            task.status = Status.in_progress.value
            
        db_task = await super().create_item(task)
        return await self.get_task_with_details_by_id(db_task.id)

    async def assign_tasks_to_technician(self, tasks : TasksAssignment):
        for task_id in tasks.task_ids:
            self.session.exec(
                update(Task)
                .where(Task.id == task_id)
                .values(technician_id=tasks.technician_id, status = Status.in_progress)
            )

        self.session.commit()

    async def update_task(self, task : TaskUpdate, task_id : int):
        db_task = await super().update_item(updated_item=task, item_id=task_id)
        return await self.get_task_with_details_by_id(db_task.id)

    async def delete_task(self, task_id : int):
        await super().delete_item(item_id=task_id)
