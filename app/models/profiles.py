from sqlmodel import Field, SQLModel

class ProfileBase(SQLModel):
    profile_name: str  = Field(
        ..., max_length=25, description="profile name, up to 25 characters",unique=True
    )

class Profile(ProfileBase, table=True):
    __tablename__ = "profiles"
    id: int | None = Field(None, primary_key=True)
    pass


class ProfileCreate(ProfileBase):
    pass


class ProfileRead(ProfileBase):
    id: int
    pass


class ProfileUpdate(ProfileBase):
    pass


