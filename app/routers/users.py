from typing import Annotated, Callable

from fastapi import (APIRouter, Depends, Query, Response,
                     UploadFile, status)
from sqlmodel import Session
from starlette.requests import Request

from app.controllers.users_controller import UsersController
from app.db.dependencies import get_session
from app.models.users import (User, UserCreate, UserRead,
                              UserUpdate, parse_user_from_data_to_user_create,
                              parse_user_from_data_to_user_update, BlockedIDs)
from app.routers.auth import authorize
from app.utils.global_utils import global_prefix
from app.utils.send_password_email import send_password_email

router = APIRouter(prefix=f"{global_prefix}/users", tags=["users"])


@router.get("/")
async def get_all_users(
    *,
    session: Session = Depends(get_session),
    req: Request,
    profile_name: Annotated[str | None, Query(max_length=25)] = None,
    current_user : User = Depends(authorize)):
    controller = UsersController(session,req)
    return await controller.get_users(profile_name, current_user.id)


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
    current_user : User = Depends(authorize),
    send_password_email_sender : Callable = Depends(send_password_email)
):
    controller = UsersController(session,req)
    return await controller.create_user(user,image,send_password_email_sender)

@router.post("/block_users")
async def block_users(
    *,
    session : Session = Depends(get_session),
    blocked_ids : BlockedIDs,
    user : User = Depends(authorize)
):
    controller = UsersController(session)
    await controller.block_users(blocked_ids)
    return {"message":"Blocked users successfully"}


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
