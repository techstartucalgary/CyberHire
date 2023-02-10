from fastapi import FastAPI
from .routers import metadata_router, user_router, user_profile_router, user_profile_skill_router

app = FastAPI()
app.include_router(user_router.router)
app.include_router(user_profile_router.router)
app.include_router(user_profile_skill_router.router)
app.include_router(metadata_router.router)
