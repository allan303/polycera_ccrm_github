#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2021-07-19

'''Config'''

import os
from dotenv import load_dotenv

load_dotenv(".env")
# Project Base
ENV = os.getenv("ENV", 'dev')
PORT = int(os.getenv("PORT", 8000))
BASE_URL = os.getenv("BASE_URL", "")  # 基础路由
PROJECT_NAME = os.getenv("PROJECT_NAME", "Polycera CCRM")
API_PREFIX = "/api"
APP_VERSION = os.getenv("APP_VERSION") or '1.0.0'
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 1  # 6 hours
SECRET_KEY = os.getenv("SECRET_KEY", str(os.urandom(20)))
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
# 默认 SU 密码
SU_PASSWORD = 'admin1111'
DEFAULT_USER_PASSWORD = os.getenv("DEFAULT_USER_PASSWORD", 'abc123')
# CORS
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "")
SU_USERNAME = os.getenv("SU_USERNAME", 'su_user')

# mongodb config
# MAX_CONNECTIONS_COUNT = int(os.getenv("MAX_CONNECTIONS_COUNT", 100))
# MIN_CONNECTIONS_COUNT = int(os.getenv("MIN_CONNECTIONS_COUNT", 100))
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
MONGO_USER = os.getenv("MONGO_USER", "")
MONGO_PASS = os.getenv("MONGO_PASSWORD", "")
if ENV == 'dev':
    MONGO_USER = ''
    MONGO_PASS = ''
MONGO_DB = os.getenv("MONGO_DB",'polycera_ccrm')


class MailConfig:
    # 邮箱设置
    MAIL_PREFIX = 'Polycera'
    MAIL_HOST = os.getenv("MAIL_HOST", "")
    MAIL_PORT = os.getenv("MAIL_PORT", "")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", False)
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", False)
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")


# default
NEW_USER_DEFAULT_PASSWORD = os.getenv('NEW_USER_DEFAULT_PASSWORD', 'aaaaaa')

# 各种Path

# 路径配置
CONFIG_DEST = os.path.abspath(os.path.dirname(__file__))  # /app/core
APP_DEST = os.path.dirname(CONFIG_DEST)  # /app
ROOT_DEST = os.path.dirname(APP_DEST)  # /根目录
# static根目录
STATIC_DEST = os.path.join(APP_DEST,  'static')  # /app/static
EXCEL_DEST = os.path.join(STATIC_DEST, 'excel')

# 默认权限json
DEFAULT_PERMISSIONS_DEST = os.path.join(STATIC_DEST, 'default_permissions')
# 照片上传位置
# /app/static/upload/images
UPLOADED_PHOTO_DEST = os.path.join(STATIC_DEST, 'upload', 'images')

# 上传文件位置
UPLOADED_ATTACHMENT_DEST = os.path.join(
    STATIC_DEST, 'upload', 'files')  # /app/static/upload/files
# word模板位置
# /app/static/doc_templates
DOC_TPL_DEST = os.path.join(STATIC_DEST, 'doc_templates')
# /app/static/excel_templates
# EXCEL_TPL_DEST = os.path.join(STATIC_DEST, 'excel_templates')
# product excel dir
PRODUCT_EXCEL_DEST = os.path.join(ROOT_DEST, 'src', "datasheet_src")
PER_PAGE = 20
# 缓存
MYCACHE = {}
