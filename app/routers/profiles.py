from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlmodel import Session, select

from app.controllers.profiles_controllers import ProfileController
from app.db.dependencies import get_session
from app.models.profiles import Profile, ProfileCreate, ProfileRead
from app.models.users import User
from app.routers.auth import authorize
from app.utils.global_utils import global_prefix

router = APIRouter(prefix=f"{global_prefix}/profiles", tags=["profiles"])


@router.get("/", response_model=list[ProfileRead])
async def get_all_profiles(*, session: Session = Depends(get_session),user : User = Depends(authorize)):
    controller = ProfileController(session)
    return await controller.get_profiles()


@router.get("/{profile_id}", response_model=ProfileRead)
async def get_profile_by_id(
    *, session: Session = Depends(get_session), profile_id: int
,user : User = Depends(authorize)):
    controller = ProfileController(session)
    return await controller.get_profile_by_id(profile_id)


@router.post("/", response_model=ProfileRead)
async def create_profile(
    *, session: Session = Depends(get_session), profile: ProfileCreate
,user : User = Depends(authorize)):
    controller = ProfileController(session)
    return await controller.create_profile(profile)


@router.put("/{profile_id}", response_model=ProfileRead)
async def update_profile(
    *, session: Session = Depends(get_session), profile: ProfileCreate, profile_id: int
,user : User = Depends(authorize)):
    controller = ProfileController(session)
    return await controller.update_profile(profile,profile_id)


@router.delete("/{profile_id}")
async def delete_profile(*, session: Session = Depends(get_session), profile_id: int,user : User = Depends(authorize)):
    controller = ProfileController(session)
    await controller.delete_profile(profile_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
