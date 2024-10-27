from datetime import timedelta, datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import InvalidTokenError
from sqlmodel import Session
import jwt

from app.controllers.users_controller import UsersController
from app.core.config import token_settings
from app.db.dependencies import get_session
from app.errors.item_not_found import ItemNotFound
from app.errors.login_credentials_invalid import LoginCredentialsInvalid
from app.models.users import User, UserLogin, Tokens, UserRead
from app.utils.global_utils import verify_hashed_password, global_prefix

router = APIRouter(prefix=f"{global_prefix}", tags=["auth"])
oauth_scheme = OAuth2PasswordBearer(tokenUrl=f'{global_prefix}/login')

async def authenticate_user(session : Session ,credentials: UserLogin, req: Request):
    user_controller = UsersController(session, req)
    try:
        user = await user_controller.get_user_by_email(credentials.email)
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
    return Tokens(
        access_token=create_token(token_data, timedelta(minutes=token_settings.access_token_expire_minutes)),
        access_token_expire_minutes= token_settings.access_token_expire_minutes,
        refresh_token=create_token(token_data, timedelta(minutes=token_settings.refresh_token_expire_minutes)),
        refresh_token_expire_minutes=token_settings.refresh_token_expire_minutes,
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

