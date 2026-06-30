from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.database import Base, engine, SessionLocal
from app.models import User, Application, AccessRequest
from sqlalchemy.orm import joinedload


# Cria automaticamente as tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PermissionFlow",
    version="1.0.0"
)

templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    db = SessionLocal()

    applications = (
        db.query(Application)
        .options(joinedload(Application.owner))
        .all()
    )

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "applications": applications
        }
    )


@app.get("/request", response_class=HTMLResponse)
def request_page(request: Request):

    db = SessionLocal()

    applications = db.query(Application).all()

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="request.html",
        context={
            "applications": applications
        }
    )

@app.post("/request")
def submit_request(
    application: int = Form(...),
    access_profile: str = Form(...),
    justification: str = Form(...),
    desired_date: str = Form(...)
):

    db = SessionLocal()

    new_request = AccessRequest(
        user_id=2,                 # Gonçalo
        application_id=application,
        access_profile=access_profile,
        justification=justification,
        desired_date=desired_date
    )

    db.add(new_request)
    db.commit()

    db.close()

    return RedirectResponse("/", status_code=303)


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

@app.get("/requests")
def list_requests():
    db = SessionLocal()

    requests = db.query(AccessRequest).all()

    result = []

    for request in requests:
        result.append({
            "id": request.id,
            "user_id": request.user_id,
            "application_id": request.application_id,
            "access_profile": request.access_profile,
            "justification": request.justification,
            "desired_date": request.desired_date,
            "status": request.status,
            "owner_comment": request.owner_comment
        })


@app.get("/my_requests", response_class=HTMLResponse)
def my_requests(request: Request):

    db = SessionLocal()

    requests = (
    db.query(AccessRequest)
    .options(
        joinedload(AccessRequest.application)
        .joinedload(Application.owner)
    )
    .filter(AccessRequest.user_id == 2)
    .all()
)

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="my_requests.html",
        context={
            "requests": requests
        }
    )

@app.get("/owner", response_class=HTMLResponse)
def owner_dashboard(request: Request):

    db = SessionLocal()

    requests = (
        db.query(AccessRequest)
        .options(
            joinedload(AccessRequest.user),
            joinedload(AccessRequest.application)
        )
        .filter(AccessRequest.status == "Pending")
        .all()
    )

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="owner.html",
        context={
            "requests": requests
        }
    )

@app.post("/approve/{request_id}")
def approve_request(
    request_id: int,
    comment: str = Form(...)
):

    db = SessionLocal()

    access_request = (
        db.query(AccessRequest)
        .filter(AccessRequest.id == request_id)
        .first()
    )

    access_request.status = "Approved"
    access_request.owner_comment = comment

    db.commit()
    db.close()

    return RedirectResponse("/owner", status_code=303)

@app.post("/reject/{request_id}")
def reject_request(
    request_id: int,
    comment: str = Form("")
):

    db = SessionLocal()

    access_request = (
        db.query(AccessRequest)
        .filter(AccessRequest.id == request_id)
        .first()
    )

    access_request.status = "Rejected"
    access_request.owner_comment = comment

    db.commit()
    db.close()

    return RedirectResponse("/owner", status_code=303)

    db.close()

    return result