#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2019-11-05

'''
入口文件
'''

import time
import jwt
from mongoengine.errors import NotUniqueError as MongoengineNotUniqueError
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from starlette.requests import Request
from app.core.utils import create_logger


# app
from app.core import config
# exception handler
from app.core.errors import (
    HTTPException_handler,
    HTTPException,
    StarletteHTTPException,  # 常规
    MongoengineNotUnique_handler,
    MongoengineNotUniqueError,  # database 字段重复
    JWTError_handler,
)
# email
from app.core.email import connect_email_server, disconnect_email_server
# db
from app.core.mongodb_utils import connect_mongodb, disconnect_mongodb
# routers
from app.api.v1.routers import all_routers
# mycache: 在startup 中进行处理
from app.mycache import create_mycache
'''
Summary: 构造主APP进程，基础组件加载
'''


def set_mycache():
    print("set_mycache")
    # MYCACHE初始为dict，用update方法，这样不会变化对象
    config.MYCACHE.update(create_mycache())


def create_app():
    # 初始化
    app = FastAPI(title=config.PROJECT_NAME, version=config.APP_VERSION)
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger = create_logger(name="update_version", path="./update_version.log")

    # static file path
    app.mount("/static", StaticFiles(directory=config.STATIC_DEST), name="static")

    # Database connect & disconnect
    app.add_event_handler("startup", connect_mongodb)
    app.add_event_handler("startup", set_mycache)
    # app.add_event_handler("startup", connect_email_server)
    # app.add_event_handler("shutdown", disconnect_email_server)
    app.add_event_handler("shutdown", disconnect_mongodb)

    # exception handle
    app.add_exception_handler(StarletteHTTPException,
                              HTTPException_handler,
                              )
    app.add_exception_handler(HTTPException,
                              HTTPException_handler,
                              )
    app.add_exception_handler(MongoengineNotUniqueError,
                              MongoengineNotUnique_handler
                              )
    app.add_exception_handler(jwt.DecodeError, JWTError_handler)
    app.add_exception_handler(jwt.ExpiredSignatureError, JWTError_handler)

    # middleware

    @app.middleware("http")
    async def middleware_logging_time(request: Request, call_next):
        '''
        Summary: 增加运行时间
        '''
        start_time = time.time()
        response = await call_next(request)
        if not response.status_code in [200, 401]:
            logger.error(
                f"ERROR: {response.status_code},{request.method},query_params: {request.query_params},path_params:{request.path_params},URL{request.url},Headers:{request.headers}")
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    # router 注册
    app.include_router(router=all_routers,
                       responses={404: {"description": "Not found"}},)
    #    prefix=config.API_PREFIX)

    return app
