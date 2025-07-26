from fastapi import HTTPException
from http import HTTPStatus
from sqlalchemy.orm import Session


# === 404 Not Found ===
def not_found_exception(detail: str = "Resource not found") -> HTTPException:
    return HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=detail)


def get_or_404(
    db: Session, resource: any, object_id: int, resource_name: str = None
):
    obj = db.get(resource, object_id)
    if not obj:
        raise not_found_exception(
            f"Resource {resource_name} with id {object_id} not found"
        )

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


def forbidden_exception(detail: str = "Forbidden") -> HTTPException:
    return HTTPException(
        status_code=HTTPStatus.FORBIDDEN,
        detail=detail,
    )
