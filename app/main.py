from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.database import Base, engine, SessionLocal
from app.models import User, Application, AccessRequest

# Cria automaticamente as tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PermissionFlow",
    version="1.0.0"
)
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title": "PermissionFlow"
        }
    )


@app.get("/users")
def list_users():
    db = SessionLocal()

    users = db.query(User).all()

    result = []

    for user in users:
        result.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        })

    db.close()

    return result