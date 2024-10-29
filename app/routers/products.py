from fastapi import (APIRouter, Depends, HTTPException, Response, UploadFile,
                     status)
from sqlmodel import Session, select
from starlette.requests import Request

from app.controllers.products_controller import ProductsController
from app.db.dependencies import get_session
from app.models.brands import Brand
from app.models.categories import Category
from app.models.products import (Product, ProductCreate, ProductRead,
                                 ProductUpdate,
                                 parse_product_from_data_to_product_create,
                                 parse_product_from_data_to_product_update, ProductAddQuantity)
from app.models.sub_categories import SubCategory
from app.models.users import User
from app.routers.auth import authorize
from app.utils.global_utils import global_prefix
from app.utils.image_utils import save_image
from app.utils.map_model_to_model_read import model_to_model_read

router = APIRouter(prefix=f"{global_prefix}/products", tags=["products"])


@router.get("/", response_model=list[ProductRead])
async def get_all_products(*, session: Session = Depends(get_session), req: Request,user : User = Depends(authorize),ref : str | None = None):
    controller = ProductsController(session,req)
    return await controller.get_products(ref)


@router.get("/{product_id}", response_model=ProductRead)
async def get_product_by_id(
    *, session: Session = Depends(get_session), product_id: int, req: Request
,user : User = Depends(authorize)):
    controller = ProductsController(session, req)
    return await controller.get_product_by_id(product_id)


@router.post("/", response_model=ProductRead)
async def create_product(
    *,
    session: Session = Depends(get_session),
    product: ProductCreate = Depends(parse_product_from_data_to_product_create),
    image: UploadFile | None = None,
    req: Request
    ,user : User = Depends(authorize)):
    controller = ProductsController(session,req)
    return await controller.create_product(product,image)


@router.put("/quantity")
async def update_products_quantity(
        *,
        session : Session = Depends(get_session),
        products : list[ProductAddQuantity],
        user : User = Depends(authorize)
):
    controller = ProductsController(session)
    await controller.update_products_quantity(products)
    return {"message": "Stock quantities updated successfully"}

@router.put("/{product_id}", response_model=ProductRead)
async def update_product(
    *,
    session: Session = Depends(get_session),
    product: ProductUpdate = Depends(parse_product_from_data_to_product_update),
    image: UploadFile | None = None,
    product_id: int,
    req: Request
,user : User = Depends(authorize)):
    controller = ProductsController(session,req)
    return await controller.update_product(product,product_id,image)

@router.delete("/{product_id}")
async def delete_product(*, session: Session = Depends(get_session), product_id: int,user : User = Depends(authorize)):
    controller = ProductsController(session)
    await controller.delete_product(product_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
