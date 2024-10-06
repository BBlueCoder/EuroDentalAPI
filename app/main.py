from typing import Annotated

from fastapi import FastAPI, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Depends
from httpx import request
from pydantic import BaseModel
from sqlmodel import SQLModel
from starlette.requests import Request

from .routers import (
    brands,
    categories,
    clients,
    images,
    products,
    profiles,
    sub_categories,
    task_products,
    tasks,
    users,
)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clients.router)
app.include_router(categories.router)
app.include_router(sub_categories.router)
app.include_router(brands.router)
app.include_router(images.router)
app.include_router(products.router)
app.include_router(profiles.router)
app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(task_products.router)


@app.get("/")
async def root(req: Request):
    return {
        "message": f"Hello from server {req.url.scheme}://{req.url.hostname}:{req.url.port} !!!"
    }


class FormImage(BaseModel):
    text: str
    date: str


def parse_form_date(text: str = Form(...), date: str = Form(...)):
    return FormImage(text=text, date=date)


@app.post("/upload")
async def upload(*, form: FormImage = Depends(parse_form_date), image: UploadFile):
    return {"image_details": form}
