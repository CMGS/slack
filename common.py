#!/usr/bin/python
#coding:utf-8

import config
import logging
from redis import ConnectionPool

logging.BASIC_FORMAT = "%(asctime)s [%(name)s] %(message)s"
logging.basicConfig(level=logging.DEBUG if config.DEBUG else logging.INFO)

session_pool = ConnectionPool(
        host=config.SESSION_HOST, \
        port=config.SESSION_PORT, \
        db=config.SESSION_DB, \
        password=config.SESSION_PASSWORD, \
        max_connections=config.SESSION_POOL_SIZE)

redis_pool = ConnectionPool(
        host=config.REDIS_HOST, \
        port=config.REDIS_PORT, \
        db=config.REDIS_DB, \
        password=config.REDIS_PASSWORD, \
        max_connections=config.REDIS_PASSWORD)

