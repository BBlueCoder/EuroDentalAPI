from sqlmodel import Session, select, update

from app.controllers.BaseController import BaseController
from app.controllers.products_controller import ProductsController
from app.errors.insufficient_stock import InsufficientStock
from app.errors.item_not_found import ItemNotFound
from app.models.products import Product
from app.models.task_products import TaskProduct, TaskProductCreate, TaskProductUpdate, TaskProductsDetails


class TaskProductController(BaseController):
    def __init__(self, session: Session):
        super().__init__(session, TaskProduct)

    async def get_task_products(self):
        return await super().get_items_all()

    async def get_task_product_by_id(self,task_product_id):
        return await super().get_first_item_by_id(item_id=task_product_id)

    async def get_all_task_products_for_a_task(self, task_id, req):
        product_controller = ProductsController(self.session,req)

        task_products : list[TaskProduct] = await super().get_items_with_condition(TaskProduct.task_id, task_id)
        mapped_result : list[TaskProductsDetails] = []
        for product in task_products:
            task_product_details = TaskProductsDetails(**product.model_dump())
            try:
                product_details = await product_controller.get_product_by_reference(product.product_reference)
                if not product.price:
                    task_product_details.price = product_details.price
                task_product_details.product_details = product_details
            except ItemNotFound:
                pass
            mapped_result.append(task_product_details)

        return mapped_result

    async def create_task_product(self, task_product : TaskProductCreate):

        #check if the product already exists in the task
        task_products : list[TaskProduct] = await super().get_items_with_condition(TaskProduct.task_id, task_product.task_id)
        for product in task_products:
            if product.product_reference == task_product.product_reference:
                raise InsufficientStock(message="product already exists in this task")
            
        #check if there enough stock quantity of this product
        product_controller = ProductsController(self.session)
        product  : Product = await product_controller.get_product_by_reference_without_details(task_product.product_reference)
        if product.stock_quantity - task_product.quantity < 0:
            raise InsufficientStock()

        #update the stock quantity
        await product_controller.update_stock(task_product.product_reference, -task_product.quantity)

        return await super().create_item(task_product)
    

    async def update_task_product(self, task_product : TaskProductUpdate, task_product_id : int):

        db_task_product = await self.get_task_product_by_id(task_product_id)
        current_quantity = db_task_product.quantity
        diff = current_quantity - task_product.quantity 



        product_controller = ProductsController(self.session)
        #if the new quantity is greater then the old
        if diff > 0:
            #update the stock quantity
            await product_controller.update_stock(task_product.product_reference, diff)
        #if the old quantity is greater then the new check if the is enough quantity in the stock
        else :
            product  : Product = await product_controller.get_product_by_reference_without_details(task_product.product_reference)
            if product.stock_quantity + diff < 0:
                raise InsufficientStock()
            else:
                #update the stock quantity
                await product_controller.update_stock(task_product.product_reference, diff)


        #update the task product
        self.session.exec(
            update(TaskProduct)
            .where(TaskProduct.id == task_product_id)
            .values(quantity = task_product.quantity)
            .values(price = task_product.price)
        )
        self.session.commit()


    async def update_product_quantity(self, task_product_id, new_quantity):
        task_product = await self.get_task_product_by_id(task_product_id)
        product_controller = ProductsController(self.session)
        product  : Product = await product_controller.get_product_by_reference_without_details(task_product.product_reference)
        previous_quantity = task_product.quantity
        diff = previous_quantity - new_quantity
        if product.stock_quantity + diff <= 0:
            raise InsufficientStock()
        await product_controller.update_product_quantity(product.id,product.stock_quantity + diff)
        self.session.exec(
            update(TaskProduct)
            .where(TaskProduct.id == task_product_id)
            .values(quantity=new_quantity)
        )
        self.session.commit()
        return await self.get_task_product_by_id(task_product_id)

    async def delete_task_product(self, task_product_id : int):
        await super().delete_item(item_id=task_product_id)
