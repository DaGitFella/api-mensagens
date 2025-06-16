from fastapi import HTTPException
from http import HTTPStatus
from sqlalchemy.orm import Session


def get_or_404(db: Session, object, object_id: int):
    obj = db.get(object, object_id)
    if not obj:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=f"Resource {object_id} not found"
        )

    return obj
