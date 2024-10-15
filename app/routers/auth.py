from datetime import timedelta, datetime, timezone
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlmodel import Session, select
import jwt

from app.core.config import token_settings
from app.db.dependencies import get_session
from app.errors.login_credentials_invalid import LoginCredentialsInvalid
from app.models.users import User, UserLogin, UserRead, Tokens
from app.utils.global_utils import verify_hashed_password

router = APIRouter(prefix="", tags=["auth"])
oauth_scheme = OAuth2PasswordBearer(tokenUrl='/token')

def authenticate_user(session : Session ,credentials: UserLogin):
    user = session.exec(select(User).where(User.email == credentials.email)).first()
    if not user:
        return False
    if not verify_hashed_password(credentials.password, user.password_hash):
        return False
    return user

def create_token(data : dict, expires_delta: timedelta):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.now(timezone.utc) + expires_delta})
    return jwt.encode(to_encode, token_settings.secret_key, algorithm=token_settings.algorithm)

def create_tokens(user : User):
    token_data = {"id": user.id, "profile_id": user.profile_id}
    return Tokens(
        access_token=create_token(token_data, timedelta(minutes=token_settings.access_token_expire_minutes)),
        refresh_token=create_token(token_data, timedelta(minutes=token_settings.refresh_token_expire_minutes))
    )

async def authorize(token: str = Depends(oauth_scheme), session : Session = Depends(get_session)):
    try:
        data = jwt.decode(token, token_settings.secret_key, algorithms=[token_settings.algorithm])
        user_id : int = data.get("id")
        if not user_id:
            raise LoginCredentialsInvalid(message="Invalid Token")
        user = session.get(User,user_id)
        if not user:
            raise LoginCredentialsInvalid(message="Invalid Token")
        return create_tokens(user)
    except InvalidTokenError:
        raise LoginCredentialsInvalid(message="Invalid Token")

@router.post("/login", response_model=Tokens)
async def login(
    *, session: Session = Depends(get_session), credentials: UserLogin
):
    user = authenticate_user(session,credentials)
    if not user:
        raise LoginCredentialsInvalid()

    return create_tokens(user)

@router.post("/refresh_token", response_model=Tokens)
async def refresh_token(*, tokens : Tokens = Depends(authorize)):
    return tokens


