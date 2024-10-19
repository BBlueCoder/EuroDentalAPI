from fastapi import APIRouter, Depends, Response, status
from sqlmodel import Session, select
from app.controllers.brands_controller import BrandsController
from app.db.dependencies import get_session
from app.models.brands import Brand, BrandCreate, BrandRead
from app.models.users import User
from app.routers.auth import authorize
from app.utils.global_utils import global_prefix

router = APIRouter(prefix=f"{global_prefix}/brands", tags=["brands"])

@router.get("/", response_model=list[BrandRead])
async def get_all_brands(*,session : Session = Depends(get_session), user : User = Depends(authorize)):
    controller = BrandsController(session)
    return await controller.get_brands()


@router.get("/{brand_id}", response_model=BrandRead)
async def get_brand_by_id(*, session: Session = Depends(get_session), brand_id: int,user : User = Depends(authorize)):
    controller = BrandsController(session)
    return await controller.get_brand_by_id(brand_id=brand_id)


@router.post("/", response_model=BrandRead)
async def create_brand(*, session: Session = Depends(get_session), brand: BrandCreate,user : User = Depends(authorize)):
    controller = BrandsController(session)
    return await controller.create_brand(brand=brand)


@router.put("/{brand_id}", response_model=BrandRead)
async def update_brand(
    *, session: Session = Depends(get_session), brand: BrandCreate, brand_id: int
,user : User = Depends(authorize)):
    controller = BrandsController(session)
    return await controller.update_item(brand,brand_id)


@router.delete("/{brand_id}")
async def delete_brand(*, session: Session = Depends(get_session), brand_id: int,user : User = Depends(authorize)):
    controller = BrandsController(session)
    await controller.delete_brand(brand_id=brand_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
