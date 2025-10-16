import logging
from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from jose import jwt
from datetime import datetime
import pytz
from pydantic import BaseModel

from app.schemas import LoginIn, ProfileIn, TokenOut
from app.auth import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    verify_refresh_token,
    JWT_SECRET,
    JWT_ALGORITHM,
)
from app.db import get_db, engine, Base
from app import crud

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("jwt-marketplace")
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="JWT Marketplace API - Kelompok 7",
    description=(
        "🚀 API untuk Marketplace dengan JWT Authentication.<br><br>"
        "**Langkah penggunaan:**<br>"
        "1️⃣ Gunakan `/auth/login` untuk mendapatkan `access_token` dan `refresh_token`.<br>"
        "2️⃣ Klik tombol **Authorize** di atas.<br>"
        "3️⃣ Masukkan token seperti ini: `Bearer <access_token>`"
    ),
    version="1.0.0",
)

@app.middleware("http")
async def add_local_time_header(request: Request, call_next):
    response = await call_next(request)
    jakarta_time = datetime.now(pytz.timezone("Asia/Jakarta")).strftime("%Y-%m-%d %H:%M:%S %Z")
    response.headers["X-Local-Time"] = jakarta_time
    return response

class WIBFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        tz = pytz.timezone("Asia/Jakarta")
        dt = datetime.fromtimestamp(record.created, tz)
        return dt.strftime("%Y-%m-%d %H:%M:%S %Z")

for handler in logging.getLogger().handlers:
    handler.setFormatter(WIBFormatter("%(asctime)s - %(levelname)s - %(message)s"))

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": str(exc.detail)})

@app.post("/auth/login", response_model=TokenOut, tags=["Auth"])
def login(payload: LoginIn, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, payload.email)
    if not user or not crud.verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(subject=str(user.id), email=user.email)
    refresh_token = create_refresh_token(subject=str(user.id), email=user.email)
    logger.info(f"✅ {user.email} berhasil login")

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }

class RefreshTokenRequest(BaseModel):
    refresh_token: str
    
@app.post("/auth/refresh", response_model=TokenOut, tags=["Auth"])
def refresh_token(request_data: RefreshTokenRequest):
    refresh_token = request_data.refresh_token
    payload = verify_refresh_token(refresh_token)
    new_access_token = create_access_token(subject=payload["sub"], email=payload["email"])
    return {
        "access_token": new_access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }

@app.get("/items", tags=["Marketplace"])
def get_items(db: Session = Depends(get_db)):
    items = crud.get_items(db)
    return {"items": [{"id": i.id, "name": i.name, "price": i.price} for i in items]}

@app.put("/profile", tags=["User"])
def update_profile(
    profile_in: ProfileIn,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Update profil user & regenerasi token"""
    updates = profile_in.dict_non_none()
    if not updates:
        return JSONResponse(
            status_code=400,
            content={"error": "At least one field (name or email) must be provided"}
        )

    new_email = updates.get("email")
    if new_email and new_email != current_user.email and crud.get_user_by_email(db, new_email):
        return JSONResponse(status_code=400, content={"error": "Email already in use"})

    updated_user = crud.update_user_profile(
        db,
        current_user,
        name=updates.get("name"),
        email=new_email
    )

    new_access_token = create_access_token(subject=str(updated_user.id), email=updated_user.email)
    new_refresh_token = create_refresh_token(subject=str(updated_user.id), email=updated_user.email)

    logger.info(f"✅ Profil {updated_user.email} berhasil diperbarui dan token diregenerasi")

    return {
        "message": "Profile updated",
        "profile": {
            "name": updated_user.name,
            "email": updated_user.email
        },
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }

from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    openapi_schema["securityDefinitions"] = {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Masukkan JWT Anda dalam format: **Bearer &lt;token&gt;**"
        }
    }

    for path in openapi_schema["paths"].values():
        for method in path.values():
            if "security" not in method:
                method["security"] = [{"Bearer": []}]

    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi