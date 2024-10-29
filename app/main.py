from datetime import timedelta
from typing import Annotated
from fastapi import Cookie, Depends, FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request
from starlette.responses import FileResponse

from app.core.config import TokenSettings
from app.db.dependencies import get_session
from app.models.users import Tokens, UserLogin

from .errors.item_not_found import ItemNotFound
from .errors.login_credentials_invalid import LoginCredentialsInvalid
from .errors.password_requires_change import PasswordRequiresChange
from .routers import (auth, brands, categories, images, products, rights,
                      profiles, sub_categories, task_products, tasks, users, clients)
from .utils.global_utils import global_prefix
from .utils.send_password_email import send_password_email

app = FastAPI(
    docs_url=f"/api/v1/docs",
    redoc_url=None
)

@app.post("/api/v1/web/login", response_model=Tokens)
async def login(
    *,
    session: Session = Depends(get_session),
    req: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    credentials = UserLogin(email=form_data.username, password=form_data.password)
    user = await auth.authenticate_user(session, credentials, req)
    if not user:
        raise LoginCredentialsInvalid()
    
    # Generate the access and refresh tokens
    tokens = auth.create_tokens(user)
    
    response = JSONResponse(content={
        "access_token": tokens.access_token,
        "id":tokens.id,
        "email":tokens.email,
        "first_name":tokens.first_name,
        "last_name":tokens.last_name,
        "profile":tokens.profile,
        "profile_id":tokens.profile_id,
        "image_path": tokens.image_path,
        "image_id":tokens.image_id
    })
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        max_age=int(timedelta(minutes=15).total_seconds()),  
        secure=True,  
        samesite="strict"
    )
    return response


@app.post("/api/v1/web/refresh_token")
async def refresh_token(
    *, 
    refresh_token: Annotated[str | None, Cookie()] = None  # Get the refresh token from the HTTP-only cookie
):
    # Check if the refresh token is valid
    if refresh_token is None:
        raise HTTPException(status_code=401, detail="Refresh token is missing")

    # Optionally validate the refresh token here
    # If validation passes, create new tokens
    token_data = {"id": 2, "profile_id": 2}
    access_token=auth.create_token(token_data, timedelta(seconds=10)),

    return JSONResponse(content={"access_token": access_token})


@app.exception_handler(IntegrityError)
async def integrity_error_handler(_, exc: IntegrityError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error_detail": jsonable_encoder(str(exc.__dict__["orig"]))},
    )

@app.exception_handler(ItemNotFound)
async def item_not_found_error_handler(_, exc: ItemNotFound):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error_detail": exc.message},
    )

@app.exception_handler(PasswordRequiresChange)
async def password_require_change_error_handler(_, exc: PasswordRequiresChange):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error_detail": exc.message},
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(req, exc: StarletteHTTPException):
    print(exc.detail)
    return JSONResponse(
        status_code=exc.status_code, content={"error_detail": exc.detail}
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(req, exc: RequestValidationError):
    print(exc.errors())
    return JSONResponse(
        status_code=422,
        content={
            "error_detail": "Request Body, Query or Path parameters are invalid. Please check the documentation."
        },
    )


@app.exception_handler(LoginCredentialsInvalid)
async def login_credentials_invalid_handler(req: Request, exc: LoginCredentialsInvalid):
    return JSONResponse(status_code=exc.status_code, content={"error_detail": exc.message})


<<<<<<< HEAD
origins = [
    "http://localhost:4200",
    "http://localhost"
    ]
=======
origins = ["http://localhost:4200"]
>>>>>>> master

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
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
app.include_router(rights.router)


@app.get("/")
async def root(req: Request):
    return {
        "message": f"Hello from server {req.url.scheme}://{req.url.hostname}:{req.url.port} !!!"
    }

@app.get("/logs")
async def logs():
    file_path = "logfile.log"
    return FileResponse(path=file_path, filename="logfile.log")

# @app.post("/email")
# async def send_mail():
#     send_password_email("opooo","aball.boy.99@gmail.com")
#     return {"message":"email sent successfully!"}

# class FormImage(BaseModel):
#     text: str
#     date: str
#
#
# def parse_form_date(text: str = Form(...), date: str = Form(...)):
#     return FormImage(text=text, date=date)
#
#
# @app.post("/upload")
# async def upload(*, form: FormImage = Depends(parse_form_date), image: UploadFile):
#     return {"image_details": form}
