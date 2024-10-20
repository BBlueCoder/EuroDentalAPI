from typing import Annotated

from fastapi import (APIRouter, Depends, HTTPException, Query, Response,
                     UploadFile, status)
from sqlmodel import Session, select
from starlette.requests import Request

from app.controllers.users_controller import UsersController
from app.db.dependencies import get_session
from app.models.profiles import Profile
from app.models.users import (User, UserByProfile, UserCreate, UserRead,
                              UserUpdate, parse_user_from_data_to_user_create,
                              parse_user_from_data_to_user_update)
from app.routers.auth import authorize
from app.utils.global_utils import global_prefix
from app.utils.image_utils import save_image
from app.utils.map_model_to_model_read import model_to_model_read

router = APIRouter(prefix=f"{global_prefix}/users", tags=["users"])


@router.get("/")
async def get_all_users(
    *,
    session: Session = Depends(get_session),
    req: Request,
    profile_name: Annotated[str | None, Query(max_length=25)] = None,
    current_user : User = Depends(authorize)):
    controller = UsersController(session,req)
    return await controller.get_users(profile_name)


@router.get("/{user_id}", response_model=UserRead)
async def get_user_by_id(
    *, session: Session = Depends(get_session), user_id: int, req: Request
,current_user : User = Depends(authorize)):
    controller = UsersController(session,req)
    return await controller.get_user_by_id(user_id)


@router.post("/", response_model=UserRead)
async def create_user(
    *,
    session: Session = Depends(get_session),
    user: UserCreate = Depends(parse_user_from_data_to_user_create),
    image: UploadFile | None = None,
    req: Request,
current_user : User = Depends(authorize)):
    controller = UsersController(session,req)
    return await controller.create_user(user,image)


@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    *,
    session: Session = Depends(get_session),
    user: UserUpdate = Depends(parse_user_from_data_to_user_update),
    image: UploadFile | None = None,
    user_id: int,
    req: Request
,current_user : User = Depends(authorize)):
    controller = UsersController(session, req)
    return await controller.update_user(user,user_id,image)


@router.delete("/{user_id}")
async def delete_user(*, session: Session = Depends(get_session), user_id: int,current_user : User = Depends(authorize)):
    controller = UsersController(session)
    await controller.delete_user(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
