#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-09-11
'''
SU操作： 目前只有新建用户
'''

from fastapi import APIRouter, Depends
from app.core.jwt import CurrentUser
from app.models.workgroup.models import WorkgroupOrm
from app.models.workgroup.schemas import WorkgroupCreatePD, WorkgroupPD, WorkgroupListPD
from app.api.v1 import create_crud_routers

router = APIRouter(prefix='/workgroup',
                   tags=['workgroup'],
                   dependencies=[
                       Depends(CurrentUser(su_required=True))
                   ])
# 此函数创建了 所有标准CRUD
create_crud_routers(
    router=router,
    orm_class=WorkgroupOrm,
    create_pd=WorkgroupCreatePD,
    edit_pd=WorkgroupCreatePD,
    list_pd=WorkgroupListPD,
    response_pd=WorkgroupPD,
    perm_list=['workgroup'],
    model_name='workgroup',
    cache_name='workgroup',
    router_exclude=['download_one', 'download_many']
)
