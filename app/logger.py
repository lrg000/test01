#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/4/7 15:37
# @Author  : liuronggui
# @File    : logger.py
# app/logger.py

import logging

logger = logging.getLogger("api_logger")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
