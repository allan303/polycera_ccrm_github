#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2019-10-24

'''
自定义 Exception
用于 全局 Exception Handle
'''
import logging
from fastapi import HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette import status
from mongoengine.errors import NotUniqueError as MongoengineNotUniqueError
from jwt import PyJWTError
from enum import Enum


HTTPException_headers = {"WWW-Authenticate": "Bearer"}


async def HTTPException_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    # 常规 HTTPException(StarletteHTTPException)
    detail = getattr(exc, 'detail', '')
    # 无则返回基本的错误信息
    return JSONResponse(status_code=exc.status_code,
                        content={"detail": str(exc.detail)},
                        headers=HTTPException_headers)


async def MongoengineNotUnique_handler(request: Request, exc: Exception) -> JSONResponse:
    # Database 关键字段重复错误
    return JSONResponse(status_code=status.HTTP_409_CONFLICT,
                        content={"detail": "名称不允许重复"},
                        headers=HTTPException_headers)


async def JWTError_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                        content={"detail": '登录过期'},
                        headers=HTTPException_headers)


class MyExceptions:
    '''
    detail 为 Error Class，非str
    '''
    # 集中所有自定义HTTPException
    login_required = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='请先登录',
    )
    # 集中所有自定义HTTPException
    bad_username_password = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='错误的用户名或密码',
    )
    # 集中所有自定义HTTPException
    bad_old_password = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='原密码错误',
    )
    # Token 过期
    token_expire = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="登录过期"
    )
    # Token Decode error
    token_decode_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="登录过期",
    )
    # 用户锁定
    locked_user = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="用户已被冻结",
    )
    # 404
    not_found = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="未找到资源"
    )
    user_not_found = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="未找到用户"
    )
    # Permission Deny
    permission_deny = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="权限拒绝"
    )
    # su_only
    su_only = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="仅限SU用户"
    )
    # su_user
    su_user_not_allowed = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="用户名不可与SU_USERNAME相同"
    )
    # admin_only
    admin_only = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="仅限ADMIN用户"
    )
    # not allowed edit
    bad_vcode = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="验证码错误"
    )
    vcode_expired = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="验证码过期"
    )
    email_or_phone_required = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="EMAIL或者PHONE必须有一项"
    )
    email_already_exist = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="EMAIL已被注册"
    )
    phone_already_exist = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="PHONE已被注册"
    )
    role_already_exist = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="此ROLE已被注册"
    )
    project_oem_already_exist = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="已存在此客户-项目关系"
    )
    oem_already_exist = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="已存在此客户"
    )
    contact_already_exist = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="此公司下已存在此联系人，如果同名同姓请加入编号以区别"
    )
    too_quick_vcode = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="请稍等再申请验证码"
    )
    tpl_not_found = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="未找到模板"
    )
    comments_not_allowed = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="评论已关闭"
    )
    su_not_allowed_edit = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="不允许修改/删除默认SU角色"
    )
    exist_project_oem = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="已经存在此关联客户，不能在同一个项目下重复添加"
    )
    need_order_sid = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="必须关联Order"
    )
    wrong_file_type = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="错误的文件类型"
    )
    name_needed = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="必须提供name"
    )
