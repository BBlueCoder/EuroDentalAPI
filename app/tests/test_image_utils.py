import pytest

from app.errors.image_size_too_big import ImageSizeTooBig
from app.errors.image_type_not_supported import ImageTypeNotSupported
from app.tests.conftest import UploadFileMock
from app.utils.image_utils import validate_image


def test_validating_valid_image(upload_file_mock : UploadFileMock):
    validate_image(upload_file_mock)
    assert True

def test_validating_unsupported_type(upload_file_mock: UploadFileMock):
    upload_file_mock.content_type = "application/pdf"
    with pytest.raises(ImageTypeNotSupported):
        validate_image(upload_file_mock)

def test_validating_image_too_big(upload_file_mock_big_size : UploadFileMock):
    with pytest.raises(ImageSizeTooBig):
        validate_image(upload_file_mock_big_size)

