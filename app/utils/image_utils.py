import time

from fastapi import UploadFile
from sqlmodel import Session
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
    image_name = await save_image_to_disk(image, "images")
    return await save_image_to_db(session=session,image_name=image_name)