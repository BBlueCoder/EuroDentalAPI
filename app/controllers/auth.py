from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlmodel import Session, select
import jwt

from app.core.config import token_settings
from app.db.dependencies import get_session
from app.errors.login_credentials_invalid import LoginCredentialsInvalid
from app.models.users import User, UserLogin, Tokens
from app.utils.global_utils import verify_hashed_password, global_prefix
from app.utils.tokens_utils import create_tokens


class AuthController:
    def __init__(self,session : Session = Depends(get_session)):
        self.oauth_scheme = OAuth2PasswordBearer(tokenUrl=f'{global_prefix}/login')
        self.session = session

    def authenticate_user(self,credentials: UserLogin):
        user = self.session.exec(select(User).where(User.email == credentials.email)).first()
        if not user:
            return False
        if not verify_hashed_password(credentials.password, user.password_hash):
            return False
        return user


    async def authorize(self,token: str):
        try:
            data = jwt.decode(token, token_settings.secret_key, algorithms=[token_settings.algorithm])
            user_id : int = data.get("id")
            if not user_id:
                raise LoginCredentialsInvalid(message="Invalid Token")
            user = self.session.get(User,user_id)
            if not user:
                raise LoginCredentialsInvalid(message="Invalid Token")
            return user
        except InvalidTokenError:
            raise LoginCredentialsInvalid(message="Invalid Token")

    async def login(self, credentials : UserLogin):
        user = self.authenticate_user(credentials)
        if not user:
            raise LoginCredentialsInvalid()

        return create_tokens(user)


