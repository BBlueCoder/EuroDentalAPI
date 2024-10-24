from sqlmodel import Session

from app.controllers.BaseController import BaseController
from app.errors.item_not_found import ItemNotFound
from app.models.profiles import Profile, ProfileCreate, ProfileRead, ProfileUpdate


class ProfileController(BaseController):
    def __init__(self, session: Session):
        super().__init__(session, Profile, ItemNotFound("Profile Not Found"))

    async def get_profiles(self):
        return await super().get_items_all()

    async def get_profile_by_name(self, profile_name):
        return await super().get_first_item_with_condition(Profile.profile_name,profile_name)

    async def get_profile_by_id(self,profile_id):
        return await super().get_first_item_by_id(item_id=profile_id)

    async def create_profile(self, profile : ProfileCreate):
        return await super().create_item(profile)

    async def update_profile(self, profile : ProfileCreate, profile_id : int):
        return await super().update_item(updated_item=profile, item_id=profile_id)

    async def delete_profile(self, profile_id : int):
        await super().delete_item(item_id=profile_id)
