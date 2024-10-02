from io import BytesIO

import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from starlette.testclient import TestClient
from app.db.dependencies import get_session
from app.main import app
from pathlib import Path

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
