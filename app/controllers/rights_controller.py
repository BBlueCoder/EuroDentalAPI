from sqlmodel import Session, asc, select
from app.controllers.BaseController import BaseController
from app.errors.item_not_found import ItemNotFound
from app.models.profiles import Profile
from app.models.rights import Right
from app.models.rights import RightRead
from app.models.users import User


class RightController(BaseController):
    statement = (
        select(Right, Profile)
        .join(Profile, isouter=True)
        .order_by(asc(Right.id_profile))
    )
    
    def __init__(self, session: Session):
        super().__init__(session, Right, ItemNotFound("Right Not Found"))

    async def get_rights(self):
        return await super().get_and_join_items(self.statement,self.map_to_rights_read)
    
    async def get_right_by_user_id(self,user_id):
        statement = self.statement.join(User, isouter=True).where(User.id == user_id)
        rights = await super().get_and_join_items(statement,self.map_to_rights_read)
        return rights[0]
    
    def map_to_rights_read(self, rights):
        mapped_rights : list[RightRead] = []
        for right, profile in rights:
            right_read = RightRead(**right.model_dump())
            if profile:
                right_read.profile_name = profile.profile_name

            mapped_rights.append(right_read)

        return mapped_rights
    
    def map_to_right_read(self, right, profile_name:str):
        right_read = RightRead(**right.model_dump())
        right_read.profile_name = profile_name

        return right_read
    
    async def create_right(self, right : RightRead):
        return await super().create_item(right)

    async def update_right(self, right : RightRead, right_id : int):
        return await super().update_item(updated_item=right, item_id=right_id)
