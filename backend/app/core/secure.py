#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2019-10-24
'''密码 salt/hash/vertify'''

import bcrypt
from passlib.context import CryptContext

# 算法
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_salt() -> str:
    # 加盐
    return bcrypt.gensalt().decode()


def verify_password_raw(password, password_hash, salt='') -> bool:
    # 验证密码
    return pwd_context.verify(salt+password, password_hash)


def get_password_hash(password, salt='') -> str:
    # 获得 hash passowrd
    return pwd_context.hash(salt+password)
