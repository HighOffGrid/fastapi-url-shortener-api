from fastapi import Request, HTTPException
from app.core.redis import redis_client
import time

RATE_LIMIT = 100
WINDOW = 60

async def rate_limit(request: Request):

    ip = request.client.host
    key = f"rate_limit:{ip}"

    current = redis_client.get(key)

    if current and int(current) >= RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Too many requests"
        )

    pipe = redis_client.pipeline()

    pipe.incr(key)

    if not current:
        pipe.expire(key, WINDOW)

    pipe.execute()