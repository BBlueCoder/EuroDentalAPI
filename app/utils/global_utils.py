import bcrypt
from starlette.requests import Request


def generate_the_address(req: Request, extra_path: str):
    if req.url.port:
        return f"{req.url.scheme}://{req.url.hostname}:{req.url.port}{extra_path}"
    return f"{req.url.scheme}://{req.url.hostname}{extra_path}"


def hash_password(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes,salt=salt)
    return hashed_password.decode('utf-8')


def verify_hashed_password(password: str, hashed_password: str):
    pwd_bytes = password.encode('utf-8')
    return bcrypt.checkpw(password=pwd_bytes,hashed_password=hashed_password.encode('utf-8'))
