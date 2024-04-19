#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2021-07-17

'''
Summary: 项目更新
'''
from fastapi import APIRouter
# app level
from app.models.project.models import ProjectUpdateOrm
from app.models.project.schemas import ProjectUpdateCreatePD, ProjectUpdatePD, ProjectUpdateListPD
from app.api.v1 import create_crud_routers

router = APIRouter(prefix='/project_update',
                   tags=['project_update'])
# 此函数创建了 所有标准CRUD
create_crud_routers(
    router=router,
    orm_class=ProjectUpdateOrm,
    create_pd=ProjectUpdateCreatePD,
    edit_pd=ProjectUpdateCreatePD,
    list_pd=ProjectUpdateListPD,
    response_pd=ProjectUpdatePD,
    perm_list=['project'],
    model_name='project',
    cache_name=None,
    router_exclude=['download_one', 'download_many']
)
