from fastapi import HTTPException
from http import HTTPStatus
from sqlalchemy.orm import Session


def not_found_exception(resource: str = None) -> HTTPException:
    exception = HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail=f"{resource} Not found",
    )

    raise exception


def get_or_404(db: Session, object, object_id: int):
    obj = db.get(object, object_id)
    if not obj:
        not_found_exception(object_id)

    return obj


credentials_exception = HTTPException(
    status_code=HTTPStatus.UNAUTHORIZED,
    detail="Could not validate credentials.",
    headers={"WWW-Authenticate": "Bearer"},
)

login_exception = HTTPException(
    status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid username or Email"
)

login_exception_password = HTTPException(
    status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid password or Email"
)

conflict_exception = HTTPException(
    status_code=HTTPStatus.CONFLICT, detail="Email already exists."
)
