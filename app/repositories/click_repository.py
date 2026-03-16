from sqlalchemy.orm import Session
from app.models.click import Click

def create_click(db: Session, url_id: int, ip: str, agent: str):

    click = Click(
        url_id=url_id,
        ip=ip,
        user_agent=agent
    )

    db.add(click)
    db.commit()
    db.refresh(click)

    return click