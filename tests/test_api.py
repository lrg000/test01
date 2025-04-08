#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/4/7 15:38
# @Author  : liuronggui
# @File    : test_api.py
# tests/test_api.py

import pytest
import httpx

BASE_URL = "http://127.0.0.1:8000"


@pytest.fixture(scope="session")
def client():
    return httpx.Client(base_url=BASE_URL)


def test_register_login_flow(client):
    user = {"username": "pytestuser", "password": "123456"}

    # 注册
    r = client.post("/register", json=user)
    assert r.status_code in [200, 400]

    # 登录
    r = client.post("/login", json=user)
    assert r.status_code == 200
    data = r.json()
    assert "access_token" in data
    assert "refresh_token" in data

    # 访问受保护接口
    headers = {"Authorization": f"Bearer {data['access_token']}"}
    r = client.get("/protected", headers=headers)
    assert r.status_code == 200

    # 刷新 token
    r = client.post("/refresh", json={"refresh_token": data["refresh_token"]})
    assert r.status_code == 200
    new_data = r.json()
    assert new_data["access_token"] != data["access_token"]


def test_file_upload(client):
    files = {'files': ('test.txt', b"Hello file")}
    r = client.post("/upload", files=files)
    assert r.status_code == 200
    assert "uploaded_files" in r.json()
