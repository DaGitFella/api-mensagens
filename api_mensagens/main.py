from fastapi import FastAPI
from api_mensagens.api.v1 import (
    message_routes,
    user_routes,
    auth,
    comment_routes,
)

app = FastAPI()
app.title = "APIMensagens"

app.include_router(
    message_routes.router, prefix="/mensagens", tags=["mensagens"]
)
app.include_router(user_routes.router, prefix="/usuarios", tags=["usuarios"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(
    comment_routes.router,
    prefix="/mensagens/{id_mensagem}/comentarios",
    tags=["comentarios"],
)


@app.get("/")
def index():
    return {"message": "Hello, World!"}
