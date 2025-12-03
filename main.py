# Wire routers + CORS in main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.database import engine
from app.models import Base
from app.routes.student_routes import router as student_router
from app.routes.auth_routes import router as auth_router
from app.config import settings

print(">>> Loaded SECRET:", settings.JWT_SECRET_KEY)

app = FastAPI(
    title="Task4React API",
    description="Student CRUD with Auth & Role-based Access",
    version="1.0.0"
)

# ---------------------------
# CREATE DATABASE TABLES HERE
# ---------------------------
Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="My API",
        version="1.0.0",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    for path in openapi_schema["paths"].values():
        for operation in path.values():
            security = operation.get("security", [])
            security.append({"BearerAuth": []})
            operation["security"] = security

    app.openapi_schema = openapi_schema
    return app.openapi_schema

@app.get("/")
def root():
    return {"message": "Processing Student Details"}

app.include_router(auth_router)
app.include_router(student_router)

app.openapi = custom_openapi
