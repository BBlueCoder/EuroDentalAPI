from datetime import timedelta, datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, Request, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import InvalidTokenError
from sqlmodel import Session
import jwt

from app.controllers.users_controller import UsersController
from app.core.config import token_settings
from app.db.dependencies import get_session
from app.errors.item_not_found import ItemNotFound
from app.errors.login_credentials_invalid import LoginCredentialsInvalid
from app.errors.password_requires_change import PasswordRequiresChange
from app.models.users import User, UserLogin, Tokens, UserRead, ChangeUserPassword, ResetPassword
from app.utils.global_utils import verify_hashed_password, global_prefix

router = APIRouter(prefix=f"{global_prefix}", tags=["auth"])
oauth_scheme = OAuth2PasswordBearer(tokenUrl=f'{global_prefix}/login')

async def authenticate_user(session : Session ,credentials: UserLogin, req: Request):
    user_controller = UsersController(session, req)
    try:
        user = await user_controller.get_user_by_email(credentials.email)
        if user.requires_password_change:
            raise PasswordRequiresChange()
        if user.is_blocked:
            return False
    except ItemNotFound:
        return False
    if not verify_hashed_password(credentials.password, user.password_hash):
        return False
    return await user_controller.get_user_by_id(user.id)

def create_token(data : dict, expires_delta: timedelta):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.now(timezone.utc) + expires_delta})
    return jwt.encode(to_encode, token_settings.secret_key, algorithm=token_settings.algorithm)

def create_tokens(user : UserRead):
    token_data = {"id": user.id, "profile_id": user.profile_id}
    print(user)
    return Tokens(
        access_token=create_token(token_data, timedelta(seconds=10)),
        refresh_token=create_token(token_data, timedelta(minutes=token_settings.refresh_token_expire_minutes)),
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        profile=user.profile,
        profile_id=user.profile_id,
        image_path= user.image_path,
        image_id=user.image_id
    )

async def authorize(token: str = Depends(oauth_scheme), session : Session = Depends(get_session)):
    try:
        data = jwt.decode(token, token_settings.secret_key, algorithms=[token_settings.algorithm])
        user_id : int = data.get("id")
        if not user_id:
            raise LoginCredentialsInvalid(message="Invalid Token")
        user_controller = UsersController(session)
        user = await user_controller.get_user_by_id(user_id)
        if not user or user.is_blocked:
            raise LoginCredentialsInvalid(message="Invalid Token")
        return user
    except InvalidTokenError:
        raise LoginCredentialsInvalid(message="Invalid Token")

@router.post("/login", response_model=Tokens)
async def login(
    *,session: Session = Depends(get_session), form_data: Annotated[OAuth2PasswordRequestForm, Depends()], req : Request
):
    credentials = UserLogin(email=form_data.username,password=form_data.password)
    user = await authenticate_user(session,credentials,req)
    if not user:
        raise LoginCredentialsInvalid()

    return create_tokens(user)

@router.post("/refresh_token", response_model=Tokens)
async def refresh_token(*, user : User = Depends(authorize)):
    return create_token(user)

@router.post("/change_password")
async def change_password(*, session: Session = Depends(get_session), user_data: ChangeUserPassword,
                          user: User = Depends(authorize)):
    user_controller = UsersController(session)
    await user_controller.change_password(user_data.id,user_data.old_password,user_data.new_password)
    return {"message":"Password changed successfully"}

@router.post("/reset_password")
async def reset_password(*, session: Session = Depends(get_session), email: ResetPassword,
                          user: User = Depends(authorize)):
    user_controller = UsersController(session)
    await user_controller.reset_password(email.email)
    return {"message": "New Password sent to the user email"}


from fastapi.responses import JSONResponse
from datetime import timedelta

@router.post("/web/login", response_model=Tokens)
async def login(
    *,
    session: Session = Depends(get_session),
    req: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    credentials = UserLogin(email=form_data.username, password=form_data.password)
    user = await authenticate_user(session, credentials, req)
    if not user:
        raise LoginCredentialsInvalid()

    # Generate the access and refresh tokens
    tokens = create_tokens(user)

    response = JSONResponse(content={
        "access_token": tokens.access_token,
        "id":tokens.id,
        "email":tokens.email,
        "first_name":tokens.first_name,
        "last_name":tokens.last_name,
        "profile":tokens.profile,
        "profile_id":tokens.profile_id,
        "image_path": tokens.image_path,
        "image_id":tokens.image_id
    })
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        max_age=int(timedelta(minutes=token_settings.refresh_token_expire_minutes).total_seconds()),
        secure=True,
        samesite="strict"
    )
    return response


@router.post("/web/refresh_token")
async def refresh_token(
    *,
    refresh_token: Annotated[str | None, Cookie()] = None  # Get the refresh token from the HTTP-only cookie
):
    # Check if the refresh token is valid
    if refresh_token is None:
        raise HTTPException(status_code=401, detail="Refresh token is missing")

    # Optionally validate the refresh token here
    # If validation passes, create new tokens
    token_data = {"id": 2, "profile_id": 2}
    access_token=create_token(token_data, timedelta(minutes=token_settings.access_token_expire_minutes)),

    return JSONResponse(content={"access_token": access_token})


