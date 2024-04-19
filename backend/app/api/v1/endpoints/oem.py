#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-09-11
'''
SU操作： 目前只有新建用户
'''

from fastapi import APIRouter
# app level
from app.models.oem.models import OemOrm
from app.models.oem.schemas import OemCreatePD, OemPD, OemSimplePD, OemListPD
from app.api.v1 import create_crud_routers


router = APIRouter(prefix='/oem',
                   tags=['oem'])

# 此函数创建了 所有标准CRUD
create_crud_routers(
    router=router,
    orm_class=OemOrm,
    create_pd=OemCreatePD,
    edit_pd=OemCreatePD,
    list_pd=OemListPD,
    response_pd=OemPD,
    perm_list=['oem'],
    model_name='oem',
    cache_name='oem',
    router_exclude=['download_one', 'download_many']
)
