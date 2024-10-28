from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from starlette.responses import FileResponse

from app.db.dependencies import get_session
from app.models.images import Image
from app.models.users import User
from app.routers.auth import authorize
from app.utils.global_utils import global_prefix

router = APIRouter(prefix=f"{global_prefix}/images", tags=["images"])


@router.get("/{image_id}")
async def serve_image(*, session: Session = Depends(get_session), image_id: int):
    db_image = session.get(Image, image_id)
    if not db_image:
        raise HTTPException(status_code=404, detail="Image Not Found 1")
    image_path = Path(f"images/{db_image.image_name}")
    if not image_path.exists():
        raise HTTPException(status_code=404, detail="Image Not Found 2")
    return FileResponse(path=image_path, filename=db_image.image_name)
