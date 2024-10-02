import time
from fastapi import UploadFile
from sqlmodel import Session

from app.errors.image_size_too_big import ImageSizeTooBig
from app.errors.image_type_not_supported import ImageTypeNotSupported
from app.models.images import ImageCreate, Image


async def save_image_to_disk(image : UploadFile, path: str):
    current_time_millis = int(time.time() * 1000)
    image_name = f"{current_time_millis}_{image.filename}"
    with open(f"{path}/{image_name}", "wb") as image_file:
        image_file.write(await image.read())
    return image_name

async def save_image_to_db(session : Session, image_name : str):
    image = ImageCreate(image_name=image_name)
    db_image = Image.model_validate(image)
    session.add(db_image)
    session.commit()
    session.refresh(db_image)
    return db_image

async def save_image(image: UploadFile, session : Session):
    validate_image(image)
    image_name = await save_image_to_disk(image, "images")
    return await save_image_to_db(session=session,image_name=image_name)

def validate_image(image : UploadFile):
    max_size_in_bytes = 5 * 1024 * 1024 # 5 MB

    accepted_file_types = ["image/png", "image/jpeg", "image/jpg", "image/heic", "image/heif", "image/heics", "png",
                           "jpeg", "jpg", "heic", "heif", "heics"
                           ]

    image_type = image.content_type
    if image_type not in accepted_file_types:
        raise ImageTypeNotSupported()

    image_size = 0
    for chunk in image.file:
        image_size += len(chunk)
        if image_size > max_size_in_bytes:
            raise ImageSizeTooBig()