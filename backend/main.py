from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.justwatch import router as justwatch_router

app = FastAPI(
    title="JustWatch Search API",
    description="API for searching movies and TV shows on JustWatch",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:4173"],  # Vite dev server ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(justwatch_router)


@app.get("/")
async def read_root():
    return {
        "message": "JustWatch Search API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/api/v1/health")
async def health_check():
    return {"status": "ok"}
