from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from starlette.requests import Request

from app.db.dependencies import get_session
from app.errors.login_credentials_invalid import LoginCredentialsInvalid
from app.models.users import User, UserLogin, UserRead
from app.utils.global_utils import verify_hashed_password

router = APIRouter(prefix="", tags=["auth"])


@router.post("/login", response_model=UserRead)
async def login(
    *, session: Session = Depends(get_session), login: UserLogin, req: Request
):
    user = session.exec(select(User).where(User.email == login.email)).first()
    if not user:
        raise LoginCredentialsInvalid()
    if not verify_hashed_password(login.password, user.password_hash):
        raise LoginCredentialsInvalid()
    return user
