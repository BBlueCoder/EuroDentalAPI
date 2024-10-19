from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlmodel import Session, select

from app.controllers.categories_controller import CategoriesController
from app.db.dependencies import get_session
from app.models.categories import Category, CategoryCreate, CategoryRead
from app.models.users import User
from app.routers.auth import authorize
from app.utils.global_utils import global_prefix

router = APIRouter(prefix=f"{global_prefix}/categories", tags=["categories"])


@router.get("/", response_model=list[CategoryRead])
async def get_all_categories(*, session: Session = Depends(get_session),user : User = Depends(authorize)):
    controller = CategoriesController(session)
    return await controller.get_categories()


@router.get("/{category_id}", response_model=CategoryRead)
async def get_category_by_id(
    *, session: Session = Depends(get_session), category_id: int
,user : User = Depends(authorize)):
    controller = CategoriesController(session)
    return await controller.get_category_by_id(category_id)


@router.post("/", response_model=CategoryRead)
async def create_category(
    *, session: Session = Depends(get_session), category: CategoryCreate
,user : User = Depends(authorize)):
    controller = CategoriesController(session)
    return await controller.create_category(category)


@router.put("/{category_id}", response_model=CategoryRead)
async def update_category(
    *,
    session: Session = Depends(get_session),
    category: CategoryCreate,
    category_id: int
,user : User = Depends(authorize)):
    controller = CategoriesController(session)
    return await controller.update_category(category,category_id)


@router.delete("/{category_id}")
async def delete_category(*, session: Session = Depends(get_session), category_id: int,user : User = Depends(authorize)):
    controller = CategoriesController(session)
    await controller.delete_category(category_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
