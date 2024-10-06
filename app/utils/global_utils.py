import typing

from passlib.handlers.pbkdf2 import pbkdf2_sha256
from starlette.requests import Request

def generate_the_address(req : Request, extra_path : str):
    if req.url.port:
        return f"{req.url.scheme}://{req.url.hostname}:{req.url.port}{extra_path}"
    return f"{req.url.scheme}://{req.url.hostname}{extra_path}"

def hash_password(password : str) -> str:
    return pbkdf2_sha256.hash(password)

def verify_hashed_password(password : str, hashed_password : str):
    return pbkdf2_sha256.verify(password,hashed_password)

