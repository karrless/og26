from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.auth import router as auth_router
from api.faq import router as faq_router
from config import FRONT_URI

app = FastAPI(title="og26 admin API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        FRONT_URI
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(faq_router)