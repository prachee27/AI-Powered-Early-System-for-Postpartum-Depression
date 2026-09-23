from pathlib import Path
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

load_dotenv()

from backend.api.routes import router as analyze_router
from backend.api.assessment_routes import router as assessment_router

app = FastAPI(
    title="Postpartum Depression Early Warning System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze_router)
app.include_router(assessment_router)

FRONTEND_DIR = Path(__file__).resolve().parents[1] / "frontend"
app.mount("/app", StaticFiles(directory=FRONTEND_DIR), name="frontend")


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok", "service": "PPD-EWS"}
