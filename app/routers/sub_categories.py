from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlmodel import Session, select

from app.db.dependencies import get_session
from app.models.sub_categories import (SubCategory, SubCategoryCreate,
                                       SubCategoryRead, SubCategoryUpdate)

router = APIRouter(prefix="/sub_categories", tags=["sub_categories"])


@router.get("/", response_model=list[SubCategoryRead])
async def get_all_sub_categories(
    *, session: Session = Depends(get_session), category_id: int | None = None
):
    if not category_id:
        return session.exec(select(SubCategory)).all()

    return session.exec(
        select(SubCategory).where(SubCategory.category_id == category_id)
    ).all()


@router.get("/{sub_category_id}", response_model=SubCategoryRead)
async def get_sub_category_by_id(
    *, session: Session = Depends(get_session), sub_category_id: int
):
    sub_category = session.get(SubCategory, sub_category_id)
    if not sub_category:
        raise HTTPException(status_code=404, detail="Sub Category Not Found")
    return sub_category


@router.post("/", response_model=SubCategoryRead)
async def create_sub_category(
    *, session: Session = Depends(get_session), sub_category: SubCategoryCreate
):
    db_sub_category = SubCategory.model_validate(sub_category)
    session.add(db_sub_category)
    session.commit()
    session.refresh(db_sub_category)
    return db_sub_category


@router.put("/{sub_category_id}", response_model=SubCategoryRead)
async def update_sub_category(
    *,
    session: Session = Depends(get_session),
    sub_category: SubCategoryUpdate,
    sub_category_id: int
):
    db_sub_category = session.get(SubCategory, sub_category_id)
    if not db_sub_category:
        raise HTTPException(status_code=404, detail="Sub Category Not Found")
    sub_category_data = sub_category.model_dump(exclude_unset=True)
    db_sub_category.sqlmodel_update(sub_category_data)
    session.add(db_sub_category)
    session.commit()
    session.refresh(db_sub_category)
    return db_sub_category


@router.delete("/{sub_category_id}")
async def update_sub_category(
    *, session: Session = Depends(get_session), sub_category_id: int
):
    sub_category = session.get(SubCategory, sub_category_id)
    if not sub_category:
        raise HTTPException(status_code=404, detail="Sub Category Not Found")
    session.delete(sub_category)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
