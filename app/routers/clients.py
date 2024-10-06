from fastapi import APIRouter, Depends, UploadFile, HTTPException, Response, status, Form
from sqlmodel import Session, select
from pydantic import EmailStr
from starlette.requests import Request

from app.db.dependencies import get_session
from app.models.clients import Client, ClientCreate, ClientRead, ClientUpdate, parse_client_from_date_to_client_create, \
    parse_client_from_date_to_client_update
from app.utils.image_utils import save_image
from app.utils.map_model_to_model_read import model_to_model_read

router = APIRouter(prefix="/clients", tags=["clients"])


@router.get("/", response_model=list[ClientRead])
async def get_all_clients(*, session: Session = Depends(get_session), req : Request):
    clients= session.exec(select(Client)).all()
    res = []
    for client in clients:
        res.append(model_to_model_read(client,req))

    return res


@router.get("/{client_id}", response_model=ClientRead)
async def get_client_by_id(*, session: Session = Depends(get_session), client_id: int, req : Request):
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client Not Found")
    return model_to_model_read(client,req)


@router.post("/", response_model=ClientRead)
async def create_client(
        *, session: Session = Depends(get_session),
        client: ClientCreate = Depends(parse_client_from_date_to_client_create),
        image: UploadFile | None = None,
        req : Request
):
    if image:
        db_image = await save_image(image, session)
        if db_image:
            client.image_id = db_image.id

    db_client = Client.model_validate(client)
    session.add(db_client)
    session.commit()
    session.refresh(db_client)
    return model_to_model_read(db_client,req)


@router.put("/{client_id}", response_model=ClientRead)
async def update_client(
        *, session: Session = Depends(get_session),
        client: ClientUpdate = Depends(parse_client_from_date_to_client_update),
        email : EmailStr | None = Form(default=None),
        image: UploadFile | None = None,
        client_id: int,
        req : Request
):
    if image:
        db_image = await save_image(image, session)
        if db_image:
            client.image_id = db_image.id

    db_client = session.get(Client, client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client Not Found")
    client_data = client.model_dump(exclude_unset=True)
    if email:
        client_data["email"] = email
    db_client.sqlmodel_update(client_data)
    session.add(db_client)
    session.commit()
    session.refresh(db_client)
    return model_to_model_read(db_client,req)


@router.delete("/{client_id}")
async def delete_client(*, session: Session = Depends(get_session), client_id: int):
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client Not Found")
    session.delete(client)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
