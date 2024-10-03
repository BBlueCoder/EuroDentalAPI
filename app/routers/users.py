from fastapi import APIRouter, Depends, UploadFile, HTTPException, Response, status, Form
from sqlmodel import Session, select
from pydantic import EmailStr
from starlette.requests import Request

from app.db.dependencies import get_session
from app.models.users import UserRead, User, user_to_user_read, UserCreate, parse_user_from_data_to_user_create, \
    UserUpdate, parse_user_from_data_to_user_update
from app.utils.image_utils import save_image

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserRead])
async def get_all_users(*, session: Session = Depends(get_session), req : Request):
    users = session.exec(select(User)).all()
    res = []
    for user in users:
        res.append(user_to_user_read(user,req))

    return res


@router.get("/{user_id}", response_model=UserRead)
async def get_user_by_id(*, session: Session = Depends(get_session), user_id: int, req : Request):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    return user_to_user_read(user,req)


@router.post("/", response_model=UserRead)
async def create_user(
        *, session: Session = Depends(get_session),
        user: UserCreate = Depends(parse_user_from_data_to_user_create),
        image: UploadFile | None = None,
        req : Request
):
    if image:
        db_image = await save_image(image, session)
        if db_image:
            user.image_id = db_image.id

    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return user_to_user_read(db_user,req)


@router.put("/{user_id}", response_model=UserRead)
async def update_user(
        *, session: Session = Depends(get_session),
        user: UserUpdate = Depends(parse_user_from_data_to_user_update),
        email : EmailStr | None = Form(default=None),
        profile_id: int | None = Form(None, foreign_key="profiles.id"),
        image: UploadFile | None = None,
        user_id: int,
        req : Request
):
    if image:
        db_image = await save_image(image, session)
        if db_image:
            user.image_id = db_image.id

    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User Not Found")
    user_data = user.model_dump(exclude_unset=True)
    if email:
        user_data["email"] = email
    if profile_id:
        user_data["profile_id"] = profile_id
    db_user.sqlmodel_update(user_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return user_to_user_read(db_user,req)


@router.delete("/{user_id}")
async def delete_user(*, session: Session = Depends(get_session), user_id: int):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    session.delete(user)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
