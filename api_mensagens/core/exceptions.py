from fastapi import HTTPException
from http import HTTPStatus
from sqlalchemy.orm import Session


def not_found_exception(resource: str = None) -> HTTPException:
    exception = HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail=f"{resource} Not found",
    )

    raise exception


def get_or_404(db: Session, resource: any, object_id: int, resource_name: str = None):
    obj = db.get(resource, object_id)
    if not obj:
        not_found_exception(f'{resource_name} {object_id}')

    return obj


def credentials_exception(
    headers: bool = False, detail: str = "Could not validate credentials"
):
    if headers:
        token_headers = {"WWW-Authenticate": "Bearer"}
        return HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=detail,
            headers=token_headers,
        )

    return HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=detail)


conflict_exception = HTTPException(
    status_code=HTTPStatus.CONFLICT, detail="Email already exists."
)
