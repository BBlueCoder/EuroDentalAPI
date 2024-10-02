from typing import Annotated

from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Depends
from sqlmodel import SQLModel
from pydantic import BaseModel
from .routers import categories, clients, sub_categories, brands, images

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


@app.get("/")
async def root():
    return {"message": "Hello from server!"}

class FormImage(BaseModel):
    text : str
    date : str

def parse_form_date(
        text : str = Form(...),
        date : str = Form(...)
):
    return FormImage(text=text,date=date)


@app.post("/upload")
async def upload(*,form : FormImage = Depends(parse_form_date),image : UploadFile):
    return {"image_details":form}
