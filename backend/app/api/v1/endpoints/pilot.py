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
from app.models.pilot.models import PilotOrm
from app.models.pilot.schemas import PilotCreatePD, PilotPD, PilotListPD
from app.api.v1 import create_crud_routers

router = APIRouter(prefix='/pilot',
                   tags=['pilot'])
# 此函数创建了 所有标准CRUD
create_crud_routers(
    router=router,
    orm_class=PilotOrm,
    create_pd=PilotCreatePD,
    edit_pd=PilotCreatePD,
    list_pd=PilotListPD,
    response_pd=PilotPD,
    perm_list=['pilot'],
    model_name='pilot',
    cache_name='pilot',
    router_exclude=['download_one', 'download_many']
)
