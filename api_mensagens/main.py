from fastapi import FastAPI
from api_mensagens.api.v1 import message_routes, user_routes, auth

app = FastAPI()
app.title = "APIMensagens"
app.include_router(message_routes.router, prefix="/messages", tags=["messages"])
app.include_router(user_routes.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])


@app.get("/")
def index():
    return {"message": "Hello, World!"}
