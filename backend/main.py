from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.requests import router as requests_router
from app.api.auth import router as auth_router
from app.api.reviewer import router as reviewer_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS configuration for React frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],  # Yeh .env se http://localhost:5173 uthayega
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the newly created Auth Router
app.include_router(auth_router, prefix=f"{settings.API_V1_STR}/auth", tags=["Auth"])
app.include_router(requests_router, prefix=f"{settings.API_V1_STR}/requests", tags=["Requests"])
app.include_router(reviewer_router, prefix=f"{settings.API_V1_STR}/reviewer", tags=["Reviewer"])

@app.get("/health", tags=["Health"])
def health_check():
    """
    Assessment requirement: Ensure the API is responsive.
    """
    return {
        "status": "success", 
        "message": "API is up and running!",
        "project": settings.PROJECT_NAME
    }