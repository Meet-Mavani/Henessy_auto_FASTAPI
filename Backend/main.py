from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from Database.schema.starting_schema import Base
from Database.schema.connect import engine

from .middleware.logging import logging_middleware
from .routes import base, document

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Document Processing API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware
@app.middleware("http")
async def add_logging_middleware(request: Request, call_next):
    return await logging_middleware(request, call_next)

# Include routers
app.include_router(base.router)
app.include_router(document.router, prefix="/documents", tags=["documents"])

# For backwards compatibility, include the original endpoints
app.include_router(base.router, prefix="/legacy")
app.include_router(document.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)