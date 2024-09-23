from fastapi import FastAPI
from .routers import clients


app = FastAPI()

app.include_router(clients.router)

@app.get("/")
async def root():
    return {"message": "Hello from server!"}


