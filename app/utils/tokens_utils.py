from datetime import timedelta, datetime, timezone

import jwt

from app.core.config import token_settings
from app.models.users import User, Tokens

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