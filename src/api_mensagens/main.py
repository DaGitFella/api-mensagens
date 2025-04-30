from fastapi import FastAPI
from api_mensagens.api.v1 import message_routes
from api_mensagens.db.init_db import init_db

app = FastAPI()
app.include_router(message_routes.router, prefix="/api/messages", tags=["messages"])

@app.on_event("startup")
def on_startup():
    return init_db()