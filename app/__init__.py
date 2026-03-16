from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import os
import redis

# Conectar com Redis
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.from_url(redis_url, decode_responses=True)

# Configurar Limiter com Redis
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=redis_url,
    default_limits=["100/minute"]  # Exemplo: 100 requests por minuto por IP
)

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/")
@limiter.limit("10/minute")  # Limite específico por rota
async def root(request: Request):
    return {"message": "Hello, World!"}