import typing

from starlette.requests import Request

from app.models.clients import Client, ClientRead
from app.models.products import Product, ProductRead
from app.models.users import User, UserRead
from app.utils.global_utils import generate_the_address

Model = typing.TypeVar("Model", bound=Product | Client | User)
ModelRead = typing.TypeVar("ModelRead", bound=ProductRead | ClientRead | UserRead)


def model_to_model_read(model: Model, req: Request) -> ModelRead:
    model_dic = model.model_dump()
    if model_dic["image_id"]:
        model_dic["image_path"] = generate_the_address(
            req, f"/images/{model_dic["image_id"]}"
        )

    if type(model) is Product:
        return ProductRead(**model_dic)

    if type(model) is Client:
        return ClientRead(**model_dic)

    if type(model) is User:
        return UserRead(**model_dic)
