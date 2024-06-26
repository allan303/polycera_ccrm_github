#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-09-11
from typing import Optional, List
# app
from app.models.base_pd import BaseDbPD, BaseModel, BaseListPD


class RoleCreatePD(BaseModel):
    '''
    Summary: create Role
    '''
    name: str  # 以name 作为 PK
    remark: Optional[str]
    perm: dict

    class Config():
        orm_mode = True


class RoleEditPD(BaseModel):
    '''
    Summary: create Role
    '''
    remark: Optional[str]
    perm: dict

    class Config():
        orm_mode = True


class RoleSimplePD(BaseDbPD):
    name: str  # 以name 作为 PK
    remark: Optional[str]

    class Config():
        orm_mode = True


class RolePD(BaseDbPD):
    name: str  # 以name 作为 PK
    remark: Optional[str]
    perm: dict


class RoleListPD(BaseListPD):
    objs: List[RoleSimplePD] = []
