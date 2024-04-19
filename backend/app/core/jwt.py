#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2019-10-24

'''JWT'''
import time
from fastapi.security import SecurityScopes
import copy
from functools import lru_cache
from dataclasses import dataclass
from typing import Union, Sequence, Callable, Any
from starlette import status
from pydantic import BaseModel
import jwt
from typing import List, Optional
from fastapi import Depends, HTTPException
from starlette.requests import Request
from fastapi.security import OAuth2PasswordBearer
# app level
from app.models.user.models import UserOrm
from .config import SECRET_KEY, JWT_ALGORITHM, API_PREFIX
from .errors import MyExceptions

# Token 地址
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{API_PREFIX}/auth/login")


async def create_access_token(*, data: dict, expire_minutes: float) -> str:
    '''
    Summary: 创建 token,
    - 可以传入 一个 dict作为 payload
    - 设置过期时间（具体的未来时间）
    - 用户如何更新？: >60分钟且<120分钟时候，通过token更新token时间
    '''
    to_encode = data.copy()
    now = time.time()  # utc timestamp
    expire_timestamp = now + expire_minutes * 60  # int计算
    to_encode.update({"exp": expire_timestamp})  # exp 为 标准key，过期时间
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


async def decode_access_token(*, token: str) -> dict:
    '''
    Summary: 根据access_token 和 本地设定的 SECRET_KEY, ALGORITHM 进行解码，返回payload(dict)
    '''
    # try:
    if not token:
        return {}
    payload = jwt.decode(jwt=token,
                         key=SECRET_KEY,
                         algorithms=[JWT_ALGORITHM],
                         # 这样payload中会始终包含 "exp":timestamp
                         # frontend 可以每次收到exp进行对比，如果小于10分钟了，则进行更新
                         options={"require": ["exp"]}
                         )
    return payload


async def get_user_by_token(token: str = '') -> UserOrm:
    '''
    Summary: 根据token 获得user
    '''
    payload = await decode_access_token(token=token)
    sid = payload.get('sub')
    if not sid:
        raise MyExceptions.token_decode_error
    user = UserOrm.get_by_sid(sid)
    if not user:
        raise MyExceptions.token_decode_error
    if user.is_deleted:
        raise MyExceptions.locked_user
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    '''
    Summary: decode token得到payload获得username，获得数据库User()
    增加 perms，用于筛选大模块权限
    '''
    user = await get_user_by_token(token=token)
    if not user:
        raise MyExceptions.token_decode_error
    if user.is_su:
        # 超级管理员都能访问
        return user
    return user


class CurrentUser:
    '''
    Summary: 多一层级别，用于 Depends 传参
    '''

    def __init__(self,
                 perms: Sequence[str] = None,
                 admin_required: bool = False,
                 su_required: bool = False
                 ):
        self.perms = perms or []
        self.admin_required = admin_required
        self.su_required = su_required

    async def __call__(self, token: str = Depends(oauth2_scheme)):
        '''
        Summary: decode token得到payload获得username，获得数据库User()
        Note   : security_scopes 可以传入 要求的scopes 限制访问
        '''
        user = await get_current_user(token=token)
        user.update_last_seen()  # 此处已经说明用户登录成功，可以更新活动时间了
        # need su
        if self.su_required:
            if not user.is_su:
                raise MyExceptions.su_only
        # need admin
        if self.admin_required:
            if not user.is_admin:
                raise MyExceptions.admin_only
        # # 验证权限
        if not self.perms:
            return user
        perm = user.perm  # 用户拥有的权限
        # 检索需要的权限是否都在
        for x in self.perms:
            if x in perm:
                if not user.can(model=x):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"PERMISSION DENY: {x}",
                        headers={"WWW-Authenticate": "Bearer"}
                    )
        return user


# TODO:以下添加各种 Permission 验证，比如 拥有 Post 权限等，
# 之后通过 @router.post('/path',depends=[...])进行注入
# 和 decorator 一样，只是形式不一样
