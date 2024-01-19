import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers import auth

# Creating additional metadata for the tags used to group path operations
tags_metadata = [
    {
        "name": "Authorization",
        "description": "Operations with user authorization",
    }
]

# Creating an "instance" of the class FastAPI
app = FastAPI(
    title="ML DEV - Backend",
    description="ML DEV course project",
    contact={"name": "KELONMYOSA", "url": "https://github.com/KELONMYOSA"},
    version="0.0.1",
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/docs/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)

# Start the uvicorn ASGI server with the specified parameters
if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8080
    uvicorn.run(app, host=host, port=port)
