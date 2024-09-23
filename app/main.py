from fastapi import FastAPI
from .routers import clients,categories


app = FastAPI()

app.include_router(clients.router)
app.include_router(categories.router)

@app.get("/")
async def root():
    return {"message": "Hello from server!"}


