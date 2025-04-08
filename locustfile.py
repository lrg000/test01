#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/4/7 15:38
# @Author  : liuronggui
# @File    : locustfile.py
# locustfile.py
from locust import HttpUser, task, between
import uuid


class WebsiteUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.username = f"locustuser_{uuid.uuid4().hex[:8]}"
        self.password = "123456"

        self.client.post("/register", json={"username": self.username, "password": self.password})

        r = self.client.post("/login", json={"username": self.username, "password": self.password})
        if r.status_code == 200:
            self.token = r.json()["access_token"]
        else:
            self.token = None

    @task
    def get_protected(self):
        if self.token:
            self.client.get("/protected", headers={"Authorization": f"Bearer {self.token}"})
