from sqlmodel import Session, select, update

from app.controllers.BaseController import BaseController
from app.controllers.profiles_controllers import ProfileController
from app.models.profiles import Profile
from app.models.users import User, UserCreate, UserByProfile, UserUpdate, BlockedIDs
from app.utils.image_utils import add_image_to_entity
from app.utils.map_model_to_model_read import model_to_model_read


class UsersController(BaseController):
    statement = select(User, Profile).join(Profile, isouter=True)

    def __init__(self, session: Session, req = None):
        super().__init__(session, User)
        self.req = req

    def map_to_user_read(self, users, profile_name = None):
        res = []
        for user, profile in users:
            user_read = model_to_model_read(user, self.req)
            if profile_name:
                user_read = UserByProfile(
                    id=user_read.id,
                    image_path=user_read.image_path,
                    full_name=f"{user_read.last_name} {user_read.first_name}",
                )
            elif profile:
                user_read.profile = profile.profile_name
            res.append(user_read)

        return res

    async def get_users(self, profile_name):
        _statement = self.statement
        if profile_name:
            profile_controller = ProfileController(self.session)
            profile = await profile_controller.get_profile_by_name(profile_name)
            _statement = self.statement.where(User.profile_id == profile.id)
        users = await super().get_and_join_items(_statement, None)
        return self.map_to_user_read(users, profile_name)

    async def get_user_by_id(self,user_id):
        users = await super().get_and_join_items(self.statement.where(User.id == user_id), None)
        if len(users) == 0:
            raise self.not_found_exc
        return self.map_to_user_read(users)[0]

    async def get_user_by_email(self, email):
        user = await super().get_first_item_with_condition(User.email, email)
        return user

    async def block_users(self, users : BlockedIDs):
        for blocked_id in users.user_ids:
            self.session.exec(
                update(User)
                .where(User.id == blocked_id)
                .values(is_blocked=True)
            )

        self.session.commit()

    async def create_user(self, user : UserCreate, image):
        user = await add_image_to_entity(user, self.session, image)
        db_user = await super().create_item(user)
        return await self.get_user_by_id(db_user.id)

    async def update_user(self, user : UserUpdate, user_id : int, image):
        user = await add_image_to_entity(user, self.session, image)
        await super().update_item(updated_item=user, item_id=user_id)
        return await self.get_user_by_id(user_id)

    async def delete_user(self, user_id : int):
        await super().delete_item(item_id=user_id)
