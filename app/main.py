from fastapi import FastAPI
from .Registration import router as auth_router
from .routers.users import router as users_router
from .routers.shows import router as shows_router
from .routers.bookings import router as bookings_router
from .routers.reviews import router as reviews_router
from .routers.cities import router as cities_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(users_router)
app.include_router(shows_router)
app.include_router(bookings_router)
app.include_router(reviews_router)
app.include_router(cities_router)


