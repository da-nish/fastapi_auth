
from typing import Annotated

from fastapi import APIRouter, FastAPI, Depends, Security, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes

router = APIRouter(prefix="/admin", tags=["admin"])

# --------------------------------------------------
# 1. SECURITY SCHEME
# --------------------------------------------------

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",

    # Uncomment later to document OAuth2 scopes in Swagger:
    # scopes={
    #     "items:read": "Permission to read items",
    #     "items:write": "Permission to create or update items",
    # },
)


# --------------------------------------------------
# 2. FAKE DATABASE (FOR DEMONSTRATION)
# --------------------------------------------------

fake_users_db = {
    "alice-token": {
        "username": "alice",
        "scopes": ["items:read"],
    },
    "bob-token": {
        "username": "bob",
        "scopes": ["items:read", "items:write"],
    },
}


# --------------------------------------------------
# 3. AUTHENTICATION + AUTHORIZATION DEPENDENCY
# --------------------------------------------------

async def get_current_user(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)],
):
    # Find user associated with the supplied token
    user = fake_users_db.get(token)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check every scope required by the endpoint
    for scope in security_scopes.scopes:
        if scope not in user["scopes"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing required permission: {scope}",
            )

    return user


# --------------------------------------------------
# 4. PUBLIC ENDPOINT
# --------------------------------------------------

@router.get("/")
async def home():
    return {"message": "Welcome! This endpoint is public."}


# --------------------------------------------------
# 5. AUTHENTICATED ENDPOINT USING Depends()
# --------------------------------------------------

@router.get("/profile")
async def get_profile(
    user: Annotated[dict, Depends(get_current_user)],
):
    return {
        "username": user["username"],
        "message": "You are authenticated",
    }


# --------------------------------------------------
# 6. ENDPOINT REQUIRING READ PERMISSION
# --------------------------------------------------

@router.get("/items")
async def read_items(
    user: Annotated[
        dict,
        Security(get_current_user, scopes=["items:read"]),
    ],
):
    return {
        "username": user["username"],
        "items": ["Laptop", "Phone", "Book"],
    }


# --------------------------------------------------
# 7. ENDPOINT REQUIRING WRITE PERMISSION
# --------------------------------------------------

@router.post("/items")
async def create_item(
    user: Annotated[
        dict,
        Security(get_current_user, scopes=["items:write"]),
    ],
):
    return {
        "username": user["username"],
        "message": "Item created successfully",
    }


# --------------------------------------------------
# 8. OPTIONAL SWAGGER / OPENAPI SCOPE DOCUMENTATION
# --------------------------------------------------

# Later, uncomment the scopes dictionary in OAuth2PasswordBearer
# above. Security() already declares the scopes required by
# each endpoint, so FastAPI can include them in OpenAPI.


# --------------------------------------------------
# 9. DEMO TOKEN ENDPOINT
# --------------------------------------------------

@router.post("/token")
async def login(username: str):
    # Demo only: no password validation or real token issuance.
    # Use proper password verification and token generation in
    # a real application.
    if username == "alice":
        return {"access_token": "alice-token", "token_type": "bearer"}

    if username == "bob":
        return {"access_token": "bob-token", "token_type": "bearer"}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unknown user",
    )
