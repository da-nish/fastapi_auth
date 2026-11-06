import os

import redis
from fastapi import APIRouter, HTTPException
from redis.exceptions import RedisError


router = APIRouter(tags=["Redis"])
redis_client = redis.Redis.from_url(
    os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    decode_responses=True,
    socket_connect_timeout=2,
    socket_timeout=2,
)


@router.get("/redis-test")
def test_redis():
    try:
        redis_client.set("fastapi:redis-test", "connected", ex=10)
        value = redis_client.get("fastapi:redis-test")
    except RedisError as exc:
        raise HTTPException(status_code=503, detail="Redis is unavailable") from exc

    if value != "connected":
        raise HTTPException(status_code=503, detail="Redis read/write test failed")

    return {"status": "ok", "redis": value}
