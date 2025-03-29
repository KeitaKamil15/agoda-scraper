from fastapi import FastAPI, Request, Depends
from app.database import Base, engine
from app.routers import auth, users, search, results, bookmark
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(title="FastAPI Auth System")

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key="your_secret_key", session_cookie="session_id")

# Mount static files (for Tailwind CSS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Set up Jinja2 templates directory
templates = Jinja2Templates(directory="app/templates")


# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(search.router)
app.include_router(results.router)
app.include_router(bookmark.router)

@app.get("/")
def home(request: Request):
    """
    Root endpoint: Redirect to login if no session, else show landing page.
    """
    if request.session.get("user") is None:
        return RedirectResponse(url="/auth/login")
    
    return templates.TemplateResponse("landing.html", {"request": request, "username": request.session["user"]})
