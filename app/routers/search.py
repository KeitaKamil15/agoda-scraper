from fastapi import APIRouter, Request, Form, BackgroundTasks
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
import uuid
import os

# Import the Playwright simulation function
from app.routers.booking_utils.playwright_simulation import booking_list_scraping
from app.routers.booking_utils.background_task_manager import scraping_task_manager
from app.routers.agoda_utils.agoda_loader import agoda_list_scraping

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def perform_scraping(task_id: str, city: str, star_rating: str = "5", min_price: int = None, max_price: int = None):
    """
    Background task for Playwright simulation
    """
    try:
        # Perform scraping agoda
        output_folder = "app/routers/agoda_utils/jsons"
        dollar_to_bdt_rate = 120
        usd_min_price = min_price // dollar_to_bdt_rate
        usd_max_price = max_price // dollar_to_bdt_rate
        agoda_list_scraping(city, star_rating, usd_min_price, usd_max_price, output_folder)

        # Prepare the HTML file path
        html_output_dir = "app/routers/booking_utils/html_files"
        os.makedirs(html_output_dir, exist_ok=True)
        html_filename = f"{html_output_dir}/{city.lower()}_booking.html"
        
        # Perform scraping booking
        booking_list_scraping(city, html_filename)

        # Mark task as completed
        scraping_task_manager.complete_task(task_id)
        print(f"Playwright simulation completed for {city}")
    except Exception as e:
        # Mark task as completed
        scraping_task_manager.complete_task(task_id)
        print(f"Playwright simulation failed: {e}")

@router.post("/search")
async def search(
    request: Request,
    background_tasks: BackgroundTasks,
    city: str = Form(...),
    min_price: float = Form(...),
    max_price: float = Form(...),
    star_rating: int = Form(...)
):
    """
    Handles hotel search and triggers Playwright simulation.
    If the user is not logged in (no session exists), it redirects to the login page.
    """
    # Check if the user is logged in by verifying the session
    username = request.session.get("user")
    if not username:
        return RedirectResponse(url="/auth/login", status_code=HTTP_303_SEE_OTHER)
    
    # Generate a unique task ID
    task_id = str(uuid.uuid4())
    
    # Register the task
    scraping_task_manager.start_task(task_id, city)
    
    # Add background task
    # changing types for agoda simulation
    star_rating_agoda = str(star_rating)
    min_price_agoda = int(min_price)
    max_price_agoda = int(max_price)
    background_tasks.add_task(perform_scraping, task_id, city, star_rating_agoda, min_price_agoda, max_price_agoda)
    
    # Create a search result message based on the form inputs
    search_results = (
        f"Searching for hotels in {city} with price range {min_price}-{max_price} "
        f"and {star_rating}-star rating. Scraping in progress..."
    )
    
    # Store search parameters in session for later use
    request.session['search_params'] = {
        'task_id': task_id,
        'city': city,
        'min_price': min_price,
        'max_price': max_price,
        'star_rating': star_rating
    }
    
    # Render the landing page with the search results and user's username
    return templates.TemplateResponse(
        "landing.html",
        {
            "request": request,
            "username": username,
            "search_results": search_results,
            "is_scraping": True,
            "task_id": task_id
        }
    )

@router.get("/check-scraping-status")
async def check_scraping_status(request: Request, task_id: str):
    """
    Endpoint to check the status of scraping task
    """
    task_status = scraping_task_manager.get_task_status(task_id)
    return {
        "status": task_status.get('status', 'not_found'),
        "completed": task_status.get('completed', False)
    }