#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/4/7 15:37
# @Author  : liuronggui
# @File    : auth.py
# app/auth.py
from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.database import user_db
from app.logger import logger
import uuid

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5
REFRESH_TOKEN_EXPIRE_MINUTES = 60


def authenticate_user(username: str, password: str):
    return user_db.get(username) == password


def create_access_token(username: str):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_payload = {
        "sub": username,
        "exp": expire,
        "iat": datetime.utcnow(),             # ✅ 签发时间
        "jti": str(uuid.uuid4())              # ✅ 唯一 token ID
    }
    token = jwt.encode(token_payload, SECRET_KEY, algorithm=ALGORITHM)
    logger.info(f"Access token created for {username}")
    return token


def create_refresh_token(username: str):
    expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    token_payload = {
        "sub": username,
        "exp": expire,
        "type": "refresh",
        "iat": datetime.utcnow(),             # ✅ 签发时间
        "jti": str(uuid.uuid4())              # ✅ 唯一 token ID
    }
    token = jwt.encode(token_payload, SECRET_KEY, algorithm=ALGORITHM)
    logger.info(f"Refresh token created for {username}")
    return token


def verify_token(token: str, refresh=False):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if refresh and payload.get("type") != "refresh":
            return None
        return payload.get("sub")
    except JWTError as e:
        logger.warning(f"Token verification failed: {e}")
        return None