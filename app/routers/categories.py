from sys import prefix

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlmodel import Session, select
from app.db.dependencies import get_session
from app.models.categories import CategoryRead, Category, CategoryCreate
from app.routers.clients import router

router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)


@router.get("/",response_model=list[CategoryRead])
async def get_all_categories(*, session : Session = Depends(get_session)):
    return session.exec(select(Category)).all()

@router.get("/{category_id}",response_model=CategoryRead)
async def get_category_by_id(*, session : Session = Depends(get_session), category_id : int):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404,detail="Category Not Found")
    return category

@router.post("/",response_model=CategoryRead)
async def create_category(*, session : Session = Depends(get_session), category : CategoryCreate):
    db_category = Category.model_validate(category)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category

@router.put("/{category_id}", response_model=CategoryRead)
async def update_category(*, session : Session = Depends(get_session), category: CategoryCreate, category_id : int):
    db_category = session.get(Category, category_id)
    if not db_category:
        raise HTTPException(status_code=404,detail="Category Not Found")
    category_data = category.model_dump(exclude_unset=True)
    db_category.sqlmodel_update(category_data)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category

@router.delete("/{category_id}")
async def delete_category(*, session : Session = Depends(get_session), category_id : int):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404,detail="Category Not Found")
    session.delete(category)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

