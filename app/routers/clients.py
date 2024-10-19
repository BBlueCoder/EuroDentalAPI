from fastapi import (APIRouter, Depends, status,
                     UploadFile)
from sqlmodel import Session
from starlette.requests import Request
from starlette.responses import Response

from app.controllers.clients_controller import ClientsController
from app.db.dependencies import get_session
from app.models.clients import (ClientCreate, ClientRead, ClientUpdate,
                                parse_client_from_date_to_client_create,
                                parse_client_from_date_to_client_update)
from app.models.users import User
from app.routers.auth import authorize
from app.utils.global_utils import global_prefix

router = APIRouter(prefix=f"{global_prefix}/clients", tags=["clients"])


@router.get("/", response_model=list[ClientRead])
async def get_all_clients(*, session: Session = Depends(get_session), req: Request,user : User = Depends(authorize)):
    controller = ClientsController(session,req)
    return await controller.get_clients()


@router.get("/{client_id}", response_model=ClientRead)
async def get_client_by_id(
    *, session: Session = Depends(get_session), client_id: int, req: Request
,user : User = Depends(authorize)):
    controller = ClientsController(session, req)
    return await controller.get_client_by_id(client_id)


@router.post("/", response_model=ClientRead)
async def create_client(
    *,
    session: Session = Depends(get_session),
    client: ClientCreate = Depends(parse_client_from_date_to_client_create),
    image: UploadFile | None = None,
    req: Request
,user : User = Depends(authorize)):
    controller = ClientsController(session, req)
    return await controller.create_client(client, image)


@router.put("/{client_id}", response_model=ClientRead)
async def update_client(
    *,
    session: Session = Depends(get_session),
    client: ClientUpdate = Depends(parse_client_from_date_to_client_update),
    image: UploadFile | None = None,
    client_id: int,
    req: Request
,user : User = Depends(authorize)):
    controller = ClientsController(session, req)
    return await controller.update_client(client,client_id,image)


@router.delete("/{client_id}")
async def delete_client(*, session: Session = Depends(get_session), client_id: int,user : User = Depends(authorize)):
    controller = ClientsController(session)
    await controller.delete_client(client_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
