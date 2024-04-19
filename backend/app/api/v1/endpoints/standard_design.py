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
from app.models.design.models import StandardDesignOrm
from app.models.design.schemas import (
    DesignOptionCreatePD, DesignOptionPD, DesignOptionListPD
)
from app.api.v1 import create_crud_routers

router = APIRouter(prefix='/standard_design',
                   tags=['standard_design'])
# 此函数创建了 所有标准CRUD
create_crud_routers(
    router=router,
    orm_class=StandardDesignOrm,
    create_pd=DesignOptionCreatePD,
    edit_pd=DesignOptionCreatePD,
    list_pd=DesignOptionListPD,
    response_pd=DesignOptionPD,
    perm_list=['standard_design'],
    model_name='standard_design',
    cache_name='standard_design',
    router_exclude=['download_one', 'download_many']
)
