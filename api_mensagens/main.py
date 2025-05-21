from fastapi import FastAPI
from api_mensagens.api.v1 import message_routes

app = FastAPI()
app.title = "APIMensagens"
app.include_router(message_routes.router, prefix="/api/messages", tags=["messages"])

@app.get("/")
def index():
    return {"message": "Hello, World!"}
