#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-02-10

'''
系统Config
'''
import os

CURRENT_DEST = os.path.abspath(os.path.dirname(__file__))  # 当前
BASE_DEST = os.path.dirname(CURRENT_DEST)  # 主路径
DOC_TPL_DEST = os.path.join(BASE_DEST, 'doctpl')
JSON_DEST = os.path.join(BASE_DEST, 'jsons')
JSON_DEST_DESIGN_OPTION = os.path.join(JSON_DEST, 'design_option')
# MongoDB config
MONGO_DB_HOST = 'localhost'
MONGO_DB_PORT = 27017
MONGO_DB_NAME = 'autodesign'
MONGO_DB_ALIAS = 'autodesign'  # Model时指定数据库连接
MONGO_DB_USERNAME = ''
MONGO_DB_PASSWORD = ''
MONGO_DB_AUTH_DB = None
