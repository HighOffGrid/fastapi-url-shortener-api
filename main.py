from fastapi import  FastAPI, Depends, Request, HTTPException
from app.routers import url_router
from app.database.connection import engine, Base, get_db
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from app.services import url_service
from app.middleware.rate_limit import rate_limit

Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Shortener API", version="1.0")

app.include_router(url_router.router)

@app.get("/{code}")
def redirect_short_url(code: str, request: Request, db: Session = Depends(get_db)):

    url = url_service.get_original_url(db, code)

    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    url_service.register_click(db, url, request)

    return RedirectResponse(url.original_url)

@app.middleware("http")
async def rate_limit_middleware(request, call_next):

    await rate_limit(request)

    response = await call_next(request)

    return response