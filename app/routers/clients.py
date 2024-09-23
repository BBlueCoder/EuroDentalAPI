from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlmodel import Session, select

from app.db.dependencies import get_session
from app.models.clients import ClientRead, Client, ClientCreate

router = APIRouter(
    prefix="/clients",
    tags=["clients"]
)

@router.get("/",response_model=list[ClientRead])
async def get_all_clients(*, session : Session = Depends(get_session)):
    return session.exec(select(Client)).all()

@router.get("/{client_id}",response_model=ClientRead)
async def get_client_by_id(*, session : Session = Depends(get_session), client_id : int):
    client = session.get(Client,client_id)
    if not client:
        raise HTTPException(status_code=404,detail="Client Not Found")
    return client

@router.post("/",response_model=ClientRead)
async def create_client(*, session : Session = Depends(get_session),client : ClientCreate):
    db_client = Client.model_validate(client)
    session.add(db_client)
    session.commit()
    session.refresh(db_client)
    return db_client

@router.put("/{client_id}", response_model=ClientRead)
async def update_client(*, session : Session = Depends(get_session), client: ClientCreate, client_id : int):
    db_client = session.get(Client, client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client Not Found")
    client_data = client.model_dump(exclude_unset=True)
    db_client.sqlmodel_update(client_data)
    session.add(db_client)
    session.commit()
    session.refresh(db_client)
    return db_client

@router.delete("/{client_id}")
async def delete_client(*, session : Session = Depends(get_session), client_id : int):
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client Not Found")
    session.delete(client)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)