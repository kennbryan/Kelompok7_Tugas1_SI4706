import os
from datetime import datetime, timedelta
from typing import Optional

from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import HTTPException, status, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from app.db import get_db
from app import models
from app.crud import get_user_by_email

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
if not JWT_SECRET:
    raise RuntimeError("JWT_SECRET is not set. Please check your .env file")

JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

bearer_scheme = HTTPBearer(auto_error=False)

def create_access_token(subject: str, email: str) -> str:
    exp = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": subject, "email": email, "type": "access", "exp": exp}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def create_refresh_token(subject: str, email: str) -> str:
    exp = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {"sub": subject, "email": email, "type": "refresh", "exp": exp}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(bearer_scheme),
    db: Session = Depends(get_db)
):
    print("=== DEBUG AUTH START ===")
    if not credentials or credentials.scheme.lower() != "bearer":
        print("⛔ Missing or invalid Authorization header")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header",
        )

    token = credentials.credentials
    print(f"Token diterima (potongan): {token[:40]}...")

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        print("✅ Token berhasil didecode:", payload)

        sub = payload.get("sub")
        email = payload.get("email")
        token_type = payload.get("type")

        if not sub or not email or token_type != "access":
            print("⛔ Payload tidak lengkap atau bukan access token")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
            )

        # Coba cari user dari email dulu
        user = get_user_by_email(db, email=email)
        if not user:
            print(f"⚠️ User dengan email {email} tidak ditemukan, coba berdasarkan ID {sub}")
            user = db.query(models.User).filter(models.User.id == sub).first()

        if not user:
            print("❌ User tidak ditemukan di database")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        print(f"✅ User ditemukan: ID={user.id}, Email={user.email}")
        print("=== DEBUG AUTH END ===")
        return user

    except ExpiredSignatureError:
        print("⛔ Token expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        )
    except JWTError as e:
        print("⛔ JWTError saat decode token:", str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

def verify_refresh_token(token: str) -> dict:
    print("=== DEBUG REFRESH TOKEN ===")
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        print("✅ Refresh token decoded:", payload)

        if payload.get("type") != "refresh":
            print("⛔ Token bukan refresh type")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token type",
            )
        return payload
    except ExpiredSignatureError:
        print("⛔ Refresh token expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired"
        )
    except JWTError as e:
        print("⛔ JWTError di refresh token:", str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )