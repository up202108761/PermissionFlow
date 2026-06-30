from fastapi import FastAPI

from app.database import Base, engine
from app.models import User, Application, AccessRequest

# Cria automaticamente as tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PermissionFlow",
    version="1.0.0"
)


@app.get("/")
def home():
    return {"message": "Welcome to PermissionFlow!"}