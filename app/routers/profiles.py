from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlmodel import Session, select

from app.db.dependencies import get_session
from app.models.profiles import Profile, ProfileCreate, ProfileRead
from app.models.users import User
from app.routers.auth import authorize
from app.utils.global_utils import global_prefix

router = APIRouter(prefix=f"{global_prefix}/profiles", tags=["profiles"])


@router.get("/", response_model=list[ProfileRead])
async def get_all_profiles(*, session: Session = Depends(get_session),user : User = Depends(authorize)):
    return session.exec(select(Profile)).all()


@router.get("/{profile_id}", response_model=ProfileRead)
async def get_profile_by_id(
    *, session: Session = Depends(get_session), profile_id: int
,user : User = Depends(authorize)):
    profile = session.get(Profile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile Not Found")
    return profile


@router.post("/", response_model=ProfileRead)
async def create_profile(
    *, session: Session = Depends(get_session), profile: ProfileCreate
,user : User = Depends(authorize)):
    db_profile = Profile.model_validate(profile)
    session.add(db_profile)
    session.commit()
    session.refresh(db_profile)
    return db_profile


@router.put("/{profile_id}", response_model=ProfileRead)
async def update_profile(
    *, session: Session = Depends(get_session), profile: ProfileCreate, profile_id: int
,user : User = Depends(authorize)):
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
async def delete_profile(*, session: Session = Depends(get_session), profile_id: int,user : User = Depends(authorize)):
    profile = session.get(Profile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile Not Found")
    session.delete(profile)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
