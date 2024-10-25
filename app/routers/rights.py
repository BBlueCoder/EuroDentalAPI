from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.controllers.rights_controller import RightController
from app.db.dependencies import get_session
from app.models.rights import RightRead
from app.models.users import User
from app.routers.auth import authorize
from app.utils.global_utils import global_prefix


router = APIRouter(prefix=f"{global_prefix}/rights", tags=["rights"])


@router.get("/", response_model=list[RightRead])
async def get_all_rights(*, session: Session = Depends(get_session), user : User = Depends(authorize)):
    controller = RightController(session)
    return await controller.get_rights()

@router.get("/{id_user}", response_model=RightRead)
async def get_right_by_user_id(
    *, 
    session: Session = Depends(get_session),
    user : User = Depends(authorize),
    id_user : int):
    controller = RightController(session)
    return await controller.get_right_by_user_id(id_user)

@router.put("/{right_id}", response_model=RightRead)
async def update_right(
        *,
        session : Session = Depends(get_session),
        right : RightRead,
        user : User = Depends(authorize)
):
    controller = RightController(session)
    return await controller.update_right(right, right.id)