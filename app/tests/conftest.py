from io import BytesIO

import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from starlette.testclient import TestClient
from app.db.dependencies import get_session
from app.main import app
from app.models.categories import Category
from app.models.clients import Client
from app.models.products import Product
from app.models.profiles import Profile
from app.models.users import UserUpdate, User

engine = create_engine(
    "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
)


@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    yield TestClient(app)

    app.dependency_overrides.clear()

@pytest.fixture(name="profile")
def profile_fixture(session : Session):
    profile = Profile(profile_name="profile1")
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile

@pytest.fixture(name="user_db")
def user_db_fixture(session : Session,profile : Profile):
    user = User(email="user@mail.com", profile_id=profile.id, password_hash="password")
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@pytest.fixture(name="category")
def category_fixture(session : Session):
    category = Category(category="category1")
    session.add(category)
    session.commit()
    session.refresh(category)
    return category

@pytest.fixture(name="product")
def product_fixture(session : Session, category : Category):
    product = Product(reference="ref001",product_name="product1",id_category=category.id)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

@pytest.fixture(name="client_db")
def client_db_fixture(session : Session):
    client = Client(email="client@mail.com")
    session.add(client)
    session.commit()
    session.refresh(client)
    return client

class UploadFileMock:
    def __init__(self, content_type, file_content, filename = "image.png"):
        self.content_type = content_type
        self.file = BytesIO(file_content)
        self.filename = filename

    async def read(self):
        return self.file.read()

@pytest.fixture(name="upload_file_mock")
def upload_file_mock_fixture():
    file_content = b'a' * (1024 * 1024)
    upload_file = UploadFileMock("image/jpeg",file_content)
    return upload_file

@pytest.fixture(name="upload_file_mock_big_size")
def upload_file_mock_big_size_fixture():
    file_content = b'a' * (6 * 1024 * 1024)
    upload_file = UploadFileMock("image/jpeg",file_content)
    return upload_file
