from typing import Annotated

from fastapi import (APIRouter, Depends, HTTPException, Query, Response,
                     UploadFile, status)
from sqlmodel import Session, select
from starlette.requests import Request

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
    user : User = Depends(authorize)):
    statement = select(User)
    if profile_name:
        profile = session.exec(
            select(Profile).where(Profile.profile_name == profile_name)
        ).first()
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Profile Not Found"
            )
        statement = statement.where(User.profile_id == profile.id)
    users = session.exec(statement).all()
    res = []
    for user in users:
        user_read = model_to_model_read(user, req)
        if profile_name:
            user_read = UserByProfile(
                id=user_read.id,
                image_path=user_read.image_path,
                full_name=f"{user_read.last_name} {user_read.first_name}",
            )
        res.append(user_read)

    return res


@router.get("/{user_id}", response_model=UserRead)
async def get_user_by_id(
    *, session: Session = Depends(get_session), user_id: int, req: Request
,user : User = Depends(authorize)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    return model_to_model_read(user, req)


@router.post("/", response_model=UserRead)
async def create_user(
    *,
    session: Session = Depends(get_session),
    user: UserCreate = Depends(parse_user_from_data_to_user_create),
    image: UploadFile | None = None,
    req: Request,
current_user : User = Depends(authorize)):
    if image:
        db_image = await save_image(image, session)
        if db_image:
            user.image_id = db_image.id

    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return model_to_model_read(db_user, req)


@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    *,
    session: Session = Depends(get_session),
    user: UserUpdate = Depends(parse_user_from_data_to_user_update),
    image: UploadFile | None = None,
    user_id: int,
    req: Request
,current_user : User = Depends(authorize)):
    if image:
        db_image = await save_image(image, session)
        if db_image:
            user.image_id = db_image.id

    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User Not Found")
    user_data = user.model_dump(exclude_unset=True)
    db_user.sqlmodel_update(user_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return model_to_model_read(db_user, req)


@router.delete("/{user_id}")
async def delete_user(*, session: Session = Depends(get_session), user_id: int,user : User = Depends(authorize)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    session.delete(user)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
