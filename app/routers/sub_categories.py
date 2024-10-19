from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlmodel import Session, select

from app.controllers.sub_categories_controller import SubCategoriesController
from app.db.dependencies import get_session
from app.models.sub_categories import (SubCategoryCreate,
                                       SubCategoryRead, SubCategoryUpdate)
from app.models.users import User
from app.routers.auth import authorize
from app.utils.global_utils import global_prefix

router = APIRouter(prefix=f"{global_prefix}/sub_categories", tags=["sub_categories"])


@router.get("/", response_model=list[SubCategoryRead])
async def get_all_sub_categories(
    *, session: Session = Depends(get_session), category_id: int | None = None
,user : User = Depends(authorize)):
    controller = SubCategoriesController(session)
    return await controller.get_sub_categories(category_id)


@router.get("/{sub_category_id}", response_model=SubCategoryRead)
async def get_sub_category_by_id(
    *, session: Session = Depends(get_session), sub_category_id: int
,user : User = Depends(authorize)):
    controller = SubCategoriesController(session)
    return await controller.get_sub_category_by_id(sub_category_id)


@router.post("/", response_model=SubCategoryRead)
async def create_sub_category(
    *, session: Session = Depends(get_session), sub_category: SubCategoryCreate
,user : User = Depends(authorize)):
    controller = SubCategoriesController(session)
    return await controller.create_sub_category(sub_category)


@router.put("/{sub_category_id}", response_model=SubCategoryRead)
async def update_sub_category(
    *,
    session: Session = Depends(get_session),
    sub_category: SubCategoryUpdate,
    sub_category_id: int
,user : User = Depends(authorize)):
    controller = SubCategoriesController(session)
    return await controller.update_sub_category(sub_category,sub_category_id)


@router.delete("/{sub_category_id}")
async def update_sub_category(
    *, session: Session = Depends(get_session), sub_category_id: int
,user : User = Depends(authorize)):
    controller = SubCategoriesController(session)
    await controller.delete_sub_category(sub_category_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
