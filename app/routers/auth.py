from fastapi import APIRouter, Depends, Request, Form, HTTPException
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from app import models, schemas, security, database

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

@router.get("/register")
def register_page(request: Request):
    """
    Serve the register page.
    """
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
def register(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(database.get_db)
):
    """
    Handle user registration.
    """
    existing_user = db.query(models.User).filter(models.User.email == email).first()
    if existing_user:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Email already registered"})

    hashed_password = security.hash_password(password)
    new_user = models.User(username=username, email=email, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return RedirectResponse(url="/auth/login", status_code=HTTP_303_SEE_OTHER)

@router.get("/login")
def login_page(request: Request):
    """
    Serve the login page.
    """
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(database.get_db)
):
    """
    Handle user login and create a session.
    """
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not security.verify_password(password, user.password_hash):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid credentials"}
        )

    # Store user session
    request.session["user"] = user.username
    request.session["email"] = user.email

    return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)

@router.get("/logout")
def logout(request: Request):
    """
    Handle user logout by clearing session.
    """
    request.session.clear()
    return RedirectResponse(url="/auth/login", status_code=HTTP_303_SEE_OTHER)