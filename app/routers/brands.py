from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlmodel import Session, select

from app.db.dependencies import get_session
from app.models.brands import Brand, BrandCreate, BrandRead
from app.models.users import User
from app.routers.auth import authorize
from app.utils.global_utils import global_prefix

router = APIRouter(prefix=f"{global_prefix}/brands", tags=["brands"])


@router.get("/", response_model=list[BrandRead])
async def get_all_brands(*, session: Session = Depends(get_session),user : User = Depends(authorize)):
    return session.exec(select(Brand)).all()


@router.get("/{brand_id}", response_model=BrandRead)
async def get_brand_by_id(*, session: Session = Depends(get_session), brand_id: int,user : User = Depends(authorize)):
    brand = session.get(Brand, brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand Not Found")
    return brand


@router.post("/", response_model=BrandRead)
async def create_brand(*, session: Session = Depends(get_session), brand: BrandCreate,user : User = Depends(authorize)):
    db_brand = Brand.model_validate(brand)
    session.add(db_brand)
    session.commit()
    session.refresh(db_brand)
    return db_brand


@router.put("/{brand_id}", response_model=BrandRead)
async def update_brand(
    *, session: Session = Depends(get_session), brand: BrandCreate, brand_id: int
,user : User = Depends(authorize)):
    db_brand = session.get(Brand, brand_id)
    if not db_brand:
        raise HTTPException(status_code=404, detail="Brand Not Found")
    brand_data = brand.model_dump(exclude_unset=True)
    db_brand.sqlmodel_update(brand_data)
    session.add(db_brand)
    session.commit()
    session.refresh(db_brand)
    return db_brand


@router.delete("/{brand_id}")
async def delete_brand(*, session: Session = Depends(get_session), brand_id: int,user : User = Depends(authorize)):
    brand = session.get(Brand, brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand Not Found")
    session.delete(brand)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
