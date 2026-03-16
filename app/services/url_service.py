from sqlalchemy.orm import Session
from fastapi import Request, HTTPException
from app.repositories import url_repository, click_repository
from app.schemas.url import URLCreate
from app.core.redis import redis_client
from app.utils.base62 import encode
import time

RATE_LIMIT = 100  # requisições
RATE_LIMIT_WINDOW = 60  # segundos (1 minuto)

def create_short_url(db: Session, url_create: URLCreate):
    # 1️⃣ Cria URL no banco sem short_code
    url = url_repository.create_url(
        db,
        original_url=url_create.original_url,
        short_code=""
    )

    # 2️⃣ Gera short_code usando Base62 do ID
    short_code = encode(url.id)

    # 3️⃣ Atualiza a URL com short_code correto
    url.short_code = short_code
    db.commit()
    db.refresh(url)

    # 4️⃣ Salva no Redis cache (opcional)
    try:
        redis_client.set(short_code, url.original_url, ex=3600)
    except:
        pass

    return url

def get_original_url(db: Session, code: str):
    # 1️⃣ Tenta buscar no cache
    try:
        cached = redis_client.get(code)
        if cached:
            url = url_repository.get_by_code(db, code)
            return url
    except:
        pass

    # 2️⃣ Busca no banco
    url = url_repository.get_by_code(db, code)
    if not url:
        return None

    # 3️⃣ Salva no cache
    try:
        redis_client.set(code, url.original_url, ex=3600)
    except:
        pass

    return url

def register_click(db: Session, url, request: Request):
    ip = request.client.host
    agent = request.headers.get("user-agent")
    click_repository.create_click(db, url.id, ip, agent)
    url_repository.increment_click_count(db, url)

def get_url_by_code(db: Session, code: str):
    return url_repository.get_by_code(db, code)

# =========================
# 🔹 Rate Limiter
# =========================
def check_rate_limit(request: Request):
    ip = request.client.host
    key = f"rate_limit:{ip}"
    try:
        current = redis_client.get(key)
        if current:
            current = int(current)
            if current >= RATE_LIMIT:
                raise HTTPException(status_code=429, detail="Rate limit exceeded")
            redis_client.incr(key)
        else:
            redis_client.set(key, 1, ex=RATE_LIMIT_WINDOW)
    except:
        # Se Redis falhar, deixamos passar
        pass
