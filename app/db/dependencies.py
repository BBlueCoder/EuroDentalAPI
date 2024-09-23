from sqlmodel import Session
from .db_connection import engine


async def get_session():
    with Session(engine) as session:
        yield session