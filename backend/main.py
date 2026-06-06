import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.api import router as api_router
from backend.database import engine
from backend.db_models import Base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialisation de la base de données
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ATS API")

logger.info("ATS API Started")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "ATS API is running"}