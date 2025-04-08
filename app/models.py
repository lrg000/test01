#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/4/7 15:37
# @Author  : liuronggui
# @File    : models.py
# app/models.py

from pydantic import BaseModel


class LoginForm(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshForm(BaseModel):
    refresh_token: str
