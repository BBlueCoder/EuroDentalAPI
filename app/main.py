from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import categories, clients

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


@app.get("/")
async def root():
    return {"message": "Hello from server!"}
