from fastapi import APIRouter, Depends, UploadFile, HTTPException, Response, status, Form
from sqlmodel import Session, select
from pydantic import EmailStr
from app.db.dependencies import get_session
from app.models.products import Product, ProductRead, ProductCreate, parse_product_from_data_to_product_create, \
    ProductUpdate, parse_product_from_data_to_product_update
from app.utils.image_utils import save_image

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=list[ProductRead])
async def get_all_products(*, session: Session = Depends(get_session)):
    return session.exec(select(Product)).all()


@router.get("/{product_id}", response_model=ProductRead)
async def get_product_by_id(*, session: Session = Depends(get_session), product_id: int):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product Not Found")
    return product


@router.post("/", response_model=ProductRead)
async def create_product(
        *, session: Session = Depends(get_session),
        product: ProductCreate = Depends(parse_product_from_data_to_product_create),
        image: UploadFile | None = None
):
    if image:
        db_image = await save_image(image, session)
        if db_image:
            product.image_id = db_image.id

    db_product = Product.model_validate(product)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


@router.put("/{product_id}", response_model=ProductRead)
async def update_product(
        *, session: Session = Depends(get_session),
        product: ProductUpdate = Depends(parse_product_from_data_to_product_update),
        image: UploadFile | None = None,
        product_id: int
):
    if image:
        db_image = await save_image(image, session)
        if db_image:
            product.image_id = db_image.id

    db_product = session.get(Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product Not Found")
    product_data = product.model_dump(exclude_unset=True)
    db_product.sqlmodel_update(product_data)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


@router.delete("/{product_id}")
async def delete_product(*, session: Session = Depends(get_session), product_id: int):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product Not Found")
    session.delete(product)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
