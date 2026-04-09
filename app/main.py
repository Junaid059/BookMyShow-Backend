from fastapi import FastAPI
from .Registration import router as auth_router
from .routers.users import router as users_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(users_router, prefix="/users", tags=["Users"])

