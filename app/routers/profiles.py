from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlmodel import Session, select

from app.db.dependencies import get_session
from app.models.profiles import Profile, ProfileCreate, ProfileRead

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("/", response_model=list[ProfileRead])
async def get_all_profiles(*, session: Session = Depends(get_session)):
    return session.exec(select(Profile)).all()


@router.get("/{profile_id}", response_model=ProfileRead)
async def get_profile_by_id(
    *, session: Session = Depends(get_session), profile_id: int
):
    profile = session.get(Profile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile Not Found")
    return profile


@router.post("/", response_model=ProfileRead)
async def create_profile(
    *, session: Session = Depends(get_session), profile: ProfileCreate
):
    db_profile = Profile.model_validate(profile)
    session.add(db_profile)
    session.commit()
    session.refresh(db_profile)
    return db_profile


@router.put("/{profile_id}", response_model=ProfileRead)
async def update_profile(
    *, session: Session = Depends(get_session), profile: ProfileCreate, profile_id: int
):
    db_profile = session.get(Profile, profile_id)
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile Not Found")
    profile_data = profile.model_dump(exclude_unset=True)
    db_profile.sqlmodel_update(profile_data)
    session.add(db_profile)
    session.commit()
    session.refresh(db_profile)
    return db_profile


@router.delete("/{profile_id}")
async def delete_profile(*, session: Session = Depends(get_session), profile_id: int):
    profile = session.get(Profile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile Not Found")
    session.delete(profile)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
