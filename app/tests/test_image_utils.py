from pathlib import Path

import pytest
from sqlmodel import Session

from app.errors.image_size_too_big import ImageSizeTooBig
from app.errors.image_type_not_supported import ImageTypeNotSupported
from app.models.images import Image
from app.tests.conftest import UploadFileMock
from app.utils.image_utils import save_image_to_db, save_image_to_disk, validate_image


def test_validating_valid_image(upload_file_mock: UploadFileMock):
    validate_image(upload_file_mock)
    assert True


def test_validating_unsupported_type(upload_file_mock: UploadFileMock):
    upload_file_mock.content_type = "application/pdf"
    with pytest.raises(ImageTypeNotSupported):
        validate_image(upload_file_mock)


def test_validating_image_too_big(upload_file_mock_big_size: UploadFileMock):
    with pytest.raises(ImageSizeTooBig):
        validate_image(upload_file_mock_big_size)


@pytest.mark.asyncio
async def test_save_image_to_disk(upload_file_mock: UploadFileMock):
    image_name = await save_image_to_disk(path="images/", image=upload_file_mock)
    assert Path(f"images/{image_name}").exists()


@pytest.mark.asyncio
async def test_save_image_to_disk_with_invalid_path(upload_file_mock: UploadFileMock):
    with pytest.raises(FileNotFoundError):
        await save_image_to_disk(path="invalid/", image=upload_file_mock)


@pytest.mark.asyncio
async def test_save_image_to_db(session: Session):
    image_name = "image.png"
    await save_image_to_db(session, image_name)
    db_image = session.get(Image, 1)
    assert db_image
    assert db_image.image_name == image_name
