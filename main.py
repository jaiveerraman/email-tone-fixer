"""
main.py
FastAPI application entry point for the AI Email Tone Fixer.
"""

from fastapi import FastAPI
from api.routes import router
from config import API_TITLE, API_DESCRIPTION, API_VERSION

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
)

app.include_router(router, prefix="/api/v1")


@app.get("/", tags=["System"])
def root():
    return {
        "service": API_TITLE,
        "version": API_VERSION,
        "docs":    "/docs",
        "health":  "/api/v1/health",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
