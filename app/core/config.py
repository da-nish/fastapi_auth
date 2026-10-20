import os


JWT_SECRET_KEY = "___secret_key___" #os.getenv("JWT_SECRET_KEY")
# if not JWT_SECRET_KEY or len(JWT_SECRET_KEY) < 32:
#     raise RuntimeError("Set JWT_SECRET_KEY to a random value with at least 32 characters")

JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1