from fastapi import FastAPI

from api.auth import router as auth_router
from api.faq import router as faq_router

app = FastAPI(title="og26 admin API")
app.include_router(auth_router)
app.include_router(faq_router)