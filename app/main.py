#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/4/7 15:37
# @Author  : liuronggui
# @File    : main.py
# app/main.py

from fastapi import FastAPI, HTTPException, Header, UploadFile, File
from app.models import LoginForm, RefreshForm, TokenResponse
from app.auth import *
from app.database import user_db
from app.logger import logger
import uvicorn

app = FastAPI()


@app.post("/register")
def register(form: LoginForm):
    if form.username in user_db:
        raise HTTPException(status_code=400, detail="User already exists")
    user_db[form.username] = form.password
    logger.info(f"New user registered: {form.username}")
    return {"message": "Registration successful"}


@app.post("/login", response_model=TokenResponse)
def login(form: LoginForm):
    if not authenticate_user(form.username, form.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {
        "access_token": create_access_token(form.username),
        "refresh_token": create_refresh_token(form.username)
    }


@app.post("/refresh", response_model=TokenResponse)
def refresh_token(form: RefreshForm):
    username = verify_token(form.refresh_token, refresh=True)
    if not username:
        raise HTTPException(status_code=403, detail="Invalid refresh token")
    return {
        "access_token": create_access_token(username),
        "refresh_token": create_refresh_token(username)
    }


@app.get("/protected")
def protected_resource(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")
    token = authorization.split(" ")[1]
    username = verify_token(token)
    if not username:
        raise HTTPException(status_code=403, detail="Token expired or invalid")
    return {"data": f"Hello {username}, you have access to protected resource."}


@app.post("/upload")
async def upload_file(files: list[UploadFile] = File(...)):
    filenames = []
    for file in files:
        content = await file.read()
        logger.info(f"Received file: {file.filename} ({len(content)} bytes)")
        filenames.append(file.filename)
    return {"uploaded_files": filenames}

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)