from fastapi import APIRouter
from api_mensagens.schemas.user import UserPublic, UserCreate

router = APIRouter()


@router.get("/", response_model=UserPublic)
def get_user(): ...


@router.post("/", response_model=UserCreate)
def create_user(user: UserCreate): ...


@router.get("/me", response_model=UserPublic)
def get_me(): ...


@router.put("/me", response_model=UserPublic)
def update_me(): ...


@router.delete("/me", response_model=UserPublic)
def delete_me(): ...
