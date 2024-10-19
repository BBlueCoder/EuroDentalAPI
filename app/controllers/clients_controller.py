from fastapi import UploadFile
from sqlmodel import Session
from starlette.requests import Request

from app.controllers.BaseController import BaseController
from app.models.clients import Client, ClientCreate, ClientUpdate
from app.utils.image_utils import save_image, add_image_to_entity
from app.utils.map_model_to_model_read import model_to_model_read


class ClientsController(BaseController):
    def __init__(self, session: Session, req : Request | None = None):
        super().__init__(session, Client)
        self.req = req

    def map_to_client_read(self, client):
        return model_to_model_read(client,self.req)

    async def get_clients(self):
        clients = await super().get_items_all()
        res = []
        for client in clients:
            res.append(self.map_to_client_read(client))

        return res

    async def get_client_by_id(self,client_id):
        client = await super().get_first_item_by_id(item_id=client_id)
        return self.map_to_client_read(client)

    async def create_client(self, client : ClientCreate, image : UploadFile | None = None):
        client = await add_image_to_entity(client,self.session,image)
        db_client = await super().create_item(client)
        return self.map_to_client_read(db_client)

    async def update_client(self, client : ClientUpdate, client_id : int, image : UploadFile | None = None):
        client = await add_image_to_entity(client,self.session,image)
        db_client = await super().update_item(updated_item=client, item_id=client_id)
        return self.map_to_client_read(db_client)

    async def delete_client(self, client_id : int):
        await super().delete_item(item_id=client_id)
