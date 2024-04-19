#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2021-07-17

'''
Summary: 项目OEM 备案管理
'''
from fastapi import APIRouter
# app level
from app.models.project.models import ProjectOemOrm
from app.models.project.schemas import ProjectOemCreatePD, ProjectOemPD, ProjectOemListPD
from app.api.v1 import create_crud_routers

router = APIRouter(prefix='/project_oem',
                   tags=['project_oem'])
# 此函数创建了 所有标准CRUD
create_crud_routers(
    router=router,
    orm_class=ProjectOemOrm,
    create_pd=ProjectOemCreatePD,
    edit_pd=ProjectOemCreatePD,
    list_pd=ProjectOemListPD,
    response_pd=ProjectOemPD,
    perm_list=['project', 'oem'],
    model_name='project',
    cache_name=None,
    router_exclude=['download_one', 'download_many']
)
