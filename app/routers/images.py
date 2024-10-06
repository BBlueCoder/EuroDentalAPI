from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from starlette.responses import FileResponse

from app.db.dependencies import get_session
from app.models.images import Image

router = APIRouter(prefix="/images", tags=["images"])


@router.get("/{image_id}")
async def serve_image(*, session: Session = Depends(get_session), image_id: int):
    db_image = session.get(Image, image_id)
    if not db_image:
        raise HTTPException(status_code=404, detail="Image Not Found")
    image_path = Path(f"images/{db_image.image_name}")
    if not image_path.exists():
        raise HTTPException(status_code=404, detail="Image Not Found")
    return FileResponse(path=image_path, filename=db_image.image_name)
