from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.justwatch import router as justwatch_router

app = FastAPI(
    title="JustWatch Search API",
    description="API for searching movies and TV shows on JustWatch",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (API is public)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(justwatch_router)


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}


# Check if static files exist and mount them
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    # Mount static files, but don't override API routes
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")
