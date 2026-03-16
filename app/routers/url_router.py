from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from app.database.connection import get_db
from app.services import url_service
from app.schemas.url import URLCreate, URLResponse
from app.repositories import url_repository

router = APIRouter(prefix="/urls", tags=["urls"])

@router.post("/", response_model=URLResponse)
def create_url(url_create: URLCreate, db: Session = Depends(get_db)):
    url = url_service.create_short_url(db, url_create)
    return URLResponse.from_orm(url)

@router.get("/{code}")
def redirect_url(code: str, request: Request, db: Session = Depends(get_db)):
    url_service.check_rate_limit(request)
    url = url_service.get_original_url(db, code)

    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    url_repository.increment_click_count(db, url)

    url_service.register_click(db, url, request)

    return RedirectResponse(url.original_url)

@router.get("/{code}/stats")
def get_stats(code: str, db: Session = Depends(get_db)):

    url = url_service.get_url_by_code(db, code)

    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    return {
        "original_url": url.original_url,
        "short_code": url.short_code,
        "clicks": url.click_count
    }