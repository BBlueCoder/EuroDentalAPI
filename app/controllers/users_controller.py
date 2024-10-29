from sqlmodel import Session, asc, select, update

from app.controllers.BaseController import BaseController
from app.controllers.profiles_controllers import ProfileController
from app.errors.login_credentials_invalid import LoginCredentialsInvalid
from app.models.profiles import Profile
from app.models.users import User, UserCreate, UserByProfile, UserUpdate, BlockedIDs
from app.utils.generate_password import generate_password
from app.utils.global_utils import hash_password, verify_hashed_password
from app.utils.image_utils import add_image_to_entity
from app.utils.map_model_to_model_read import model_to_model_read
from app.utils.send_new_password_email import send_new_password_email
from app.utils.send_password_email import send_password_email


class UsersController(BaseController):
    statement = select(User, Profile).join(Profile, isouter=True).order_by(asc(User.id))

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

    async def get_users(self, profile_name, current_user_id: int):
        _statement = self.statement
        if profile_name:
            profile_controller = ProfileController(self.session)
            profile = await profile_controller.get_profile_by_name(profile_name)
            _statement = self.statement.where(User.profile_id == profile.id and User.id != current_user_id)
        else :
            _statement = self.statement.where(User.id != current_user_id) 
        users = await super().get_and_join_items(_statement, None)
        return self.map_to_user_read(users, profile_name)

    async def get_user_by_id_without_join(self, user_id):
        return await super().get_first_item_by_id(user_id)

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
                .values(is_blocked=users.block)
            )

        self.session.commit()

    async def change_password(self, user_id,old_password, new_password):
        user_db = await super().get_first_item_by_id(user_id)
        if not verify_hashed_password(old_password,user_db.password_hash):
            raise LoginCredentialsInvalid(message="Old password is incorrect")

        self.session.exec(
            update(User)
            .where(User.id == user_id)
            .values(password_hash=hash_password(new_password))
        )

        self.session.commit()
        await self.update_requires_password_change(user_id,False)

    async def reset_password(self,email):
        user_db = await self.get_user_by_email(email)
        generated_password = generate_password()
        self.session.exec(
            update(User)
            .where(User.email == email)
            .values(password_hash=hash_password(generated_password))
        )

        self.session.commit()
        await self.update_requires_password_change(user_db.id, True)
        send_new_password_email(generated_password,email)

    async def create_user(self, user : UserCreate, image):
        user = await add_image_to_entity(user, self.session, image)
        generated_password = generate_password()
        user.password_hash = hash_password(generated_password)
        if not user.image_id:
            user.image_id = 1
        db_user = await super().create_item(user)
        await self.update_requires_password_change(db_user.id,True)
        send_password_email(generated_password,user.email)
        return await self.get_user_by_id(db_user.id)

    async def update_requires_password_change(self,user_id,requires_password_change):
        self.session.exec(
            update(User)
            .where(User.id == user_id)
            .values(requires_password_change=requires_password_change)
        )

        self.session.commit()

    async def update_user(self, user : UserUpdate, user_id : int, image):
        user = await add_image_to_entity(user, self.session, image)
        await super().update_item(updated_item=user, item_id=user_id)
        return await self.get_user_by_id(user_id)

    async def delete_user(self, user_id : int):
        await super().delete_item(item_id=user_id)
