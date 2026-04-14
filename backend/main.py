from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.database import test_connection

app = FastAPI(
    title="Medical Recommendation & Pharmacy Marketplace",
    version="1.0.0",
)

# ── CORS — allows frontend (Vite on :5173) to call the API ───
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Startup ───────────────────────────────────────────────────
@app.on_event("startup")
def startup():
    test_connection()

# ── Health check ──────────────────────────────────────────────
@app.get("/")
def root():
    return {"status": "ok", "project": "Medical Recommendation System"}

@app.get("/health")
def health():
    ok = test_connection()
    return {"db": "connected" if ok else "error"}

# ── Routers (wire in as each api file is ready) ───────────────
# from api import patients, diseases, medications, marketplace, recommendations
# app.include_router(patients.router,        prefix="/patients",        tags=["Patients"])
# app.include_router(diseases.router,        prefix="/diseases",        tags=["Diseases"])
# app.include_router(medications.router,     prefix="/medications",     tags=["Medications"])
# app.include_router(marketplace.router,     prefix="/marketplace",     tags=["Marketplace"])
# app.include_router(recommendations.router, prefix="/recommendations", tags=["Recommendations"])