from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import metadata_router, user_router, user_profile_router, \
                     user_profile_skill_router, job_router, job_skill_router

app = FastAPI()

origins = [
    "http://localhost:8000",
    "https://chapi.techstartucalgary.com/docs",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(user_router.router)
app.include_router(user_profile_router.router)
app.include_router(user_profile_skill_router.router)
app.include_router(metadata_router.router)
app.include_router(job_router.router)
app.include_router(job_skill_router.router)