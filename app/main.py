from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import joinedload

from app.database import Base, SessionLocal, engine
from app.models import Application, AccessRequest

# -----------------------
# Database
# -----------------------

Base.metadata.create_all(bind=engine)

# -----------------------
# FastAPI
# -----------------------

app = FastAPI(
    title="PermissionFlow",
    version="1.0.0"
)

templates = Jinja2Templates(directory="app/templates")

# -----------------------
# Home Page
# -----------------------

@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    success = request.query_params.get("success")

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
            "applications": applications,
            "success": success
        }
    )

# -----------------------
# Request Access
# -----------------------

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
        user_id=2,  # Temporary employee (authentication not implemented)
        application_id=application,
        access_profile=access_profile,
        justification=justification,
        desired_date=desired_date
    )

    db.add(new_request)
    db.commit()

    db.close()

    return RedirectResponse("/?success=1", status_code=303)

# -----------------------
# My Requests
# -----------------------

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

# -----------------------
# Owner Dashboard
# -----------------------

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

# -----------------------
# Approve Request
# -----------------------

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

    if access_request:
        access_request.status = "Approved"
        access_request.owner_comment = comment
        db.commit()

    db.close()

    return RedirectResponse("/owner", status_code=303)

# -----------------------
# Reject Request
# -----------------------

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

    if access_request:
        access_request.status = "Rejected"
        access_request.owner_comment = comment
        db.commit()

    db.close()

    return RedirectResponse("/owner", status_code=303)