from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database.db import init_db
from app.routes import auth, chat, document

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Runs once on startup: creates DB tables."""
    print(" Starting up — initialising database...")
    init_db()
    yield
    print("Shutting down.")


app = FastAPI(
    title=settings.app_name,
    description="RAG-based Intelligent Enterprise Assistant",
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS ─────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Tighten this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(document.router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "app": settings.app_name}