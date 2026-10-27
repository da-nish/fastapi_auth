
from fastapi import APIRouter, FastAPI, Request
from app.core.rate_limiter import limiter

router = APIRouter(prefix="/limit", tags=["Rate limit"])

@router.get("/api/products")
@limiter.limit("5/minute")
async def get_products(request: Request):
    return {"products": ["Laptop", "Phone"]}


@router.post("/api/login")
@limiter.limit("5/minute")
async def login(request: Request):
    return {"message": "Login endpoint"}
