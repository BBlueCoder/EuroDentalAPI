import bcrypt
from starlette.requests import Request

global_prefix = "/api/v1"


def generate_the_address(req: Request, extra_path: str):
    if req.url.port:
        return f"{req.url.scheme}://{req.url.hostname}:{req.url.port}{global_prefix}{extra_path}"
    return f"{req.url.scheme}://{req.url.hostname}{extra_path}"


def hash_password(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes,salt=salt)
    return hashed_password.decode('utf-8')


def verify_hashed_password(password: str, hashed_password: str):
    pwd_bytes = password.encode('utf-8')
    return bcrypt.checkpw(password=pwd_bytes,hashed_password=hashed_password.encode('utf-8'))
