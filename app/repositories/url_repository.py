from sqlalchemy.orm import Session
from app.models.url import URL

def create_url(db: Session, original_url: str, short_code: str) -> URL:
    db_url = URL(original_url=original_url, short_code=short_code)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def get_by_code(db: Session, short_code: str) -> URL:
    return db.query(URL).filter(URL.short_code == short_code).first()

def  increment_click_count(db: Session, url: URL) -> None:
    url.click_count += 1
    db.commit()

def get_all_urls(db: Session):
    return db.query(URL).all()