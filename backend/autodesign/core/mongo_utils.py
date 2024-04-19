#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-02-28

import logging
from mongoengine import connect
from pymongo import MongoClient
import pymongo.collection
from .config import (MONGO_DB_ALIAS, MONGO_DB_NAME,
                     MONGO_DB_USERNAME, MONGO_DB_PASSWORD, MONGO_DB_AUTH_DB,
                     MONGO_DB_HOST, MONGO_DB_PORT)


def connect_to_autodesign_mongoengine():
    logging.info('connecting to autodesgin...')
    connect(MONGO_DB_NAME, username=MONGO_DB_USERNAME,
            password=MONGO_DB_PASSWORD, authentication_source=MONGO_DB_AUTH_DB,
            alias=MONGO_DB_ALIAS)
    logging.info('Success connect to autodesgin!')


def get_db_collection(collection_name: str):
    client = MongoClient(MONGO_DB_HOST, MONGO_DB_PORT)
    db = client[MONGO_DB_NAME]
    return db[collection_name]
