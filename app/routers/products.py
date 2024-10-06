from fastapi import APIRouter, Depends, UploadFile, HTTPException, Response, status
from sqlmodel import Session, select
from starlette.requests import Request

from app.db.dependencies import get_session
from app.models.brands import Brand
from app.models.categories import Category
from app.models.products import Product, ProductRead, ProductCreate, parse_product_from_data_to_product_create, \
    ProductUpdate, parse_product_from_data_to_product_update
from app.models.sub_categories import SubCategory
from app.utils.image_utils import save_image
from app.utils.map_model_to_model_read import model_to_model_read

router = APIRouter(prefix="/products", tags=["products"])

async def get_products(*,product_id : int | None = None,session : Session, req : Request):
    statement = select(Product, Category, SubCategory, Brand).join(Category, isouter=True).join(SubCategory, isouter=True).join(
            Brand, isouter=True)
    if product_id:
        statement = statement.where(Product.id == product_id)

    products_with_details = session.exec(statement).all()

    mapped_results = []
    for product, category, sub_category, brand in products_with_details:
        product_read = model_to_model_read(product, req)
        if category:
            product_read.category_name = category.category

        if sub_category:
            product_read.sub_category_name = sub_category.sub_category

        if brand:
            product_read.brand_name = brand.brand

        mapped_results.append(product_read)

    return mapped_results


@router.get("/", response_model=list[ProductRead])
async def get_all_products(*, session: Session = Depends(get_session), req: Request):
    return await get_products(session=session,req=req)


@router.get("/{product_id}", response_model=ProductRead)
async def get_product_by_id(*, session: Session = Depends(get_session), product_id: int, req: Request):
    product = await get_products(product_id=product_id,session=session,req=req)
    if not product:
        raise HTTPException(status_code=404, detail="Product Not Found")
    return product[0]


@router.post("/", response_model=ProductRead)
async def create_product(
        *, session: Session = Depends(get_session),
        product: ProductCreate = Depends(parse_product_from_data_to_product_create),
        image: UploadFile | None = None,
        req : Request
):
    if image:
        db_image = await save_image(image, session)
        if db_image:
            product.image_id = db_image.id

    db_product = Product.model_validate(product)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return (await get_products(product_id=db_product.id,session=session,req=req))[0]


@router.put("/{product_id}", response_model=ProductRead)
async def update_product(
        *, session: Session = Depends(get_session),
        product: ProductUpdate = Depends(parse_product_from_data_to_product_update),
        image: UploadFile | None = None,
        product_id: int,
        req : Request
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
    return (await get_products(product_id=db_product.id,session=session,req=req))[0]


@router.delete("/{product_id}")
async def delete_product(*, session: Session = Depends(get_session), product_id: int):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product Not Found")
    session.delete(product)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
