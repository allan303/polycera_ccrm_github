#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-09-11
'''
SU操作： 目前只有新建用户
'''

from fastapi import APIRouter, Depends
from typing import List, Optional
# from starlette.responses import StreamingResponse


from app.core.jwt import CurrentUser, UserOrm

from app.models.project.models import ProjectOrm, ProjectOemOrm, ProjectUpdateOrm
from app.models.project.schemas import (ProjectCreatePD, ProjectPD, ProjectSimplePD, ProjectListPD,
                                        ProjectOemPD, ProjectUpdatePD, ProjectOemCreatePD, ProjectUpdateCreatePD,
                                        ProjectEditPD)

from app.api.v1 import create_crud_routers

router = APIRouter(prefix='/project',
                   tags=['project'])
# 此函数创建了 所有标准CRUD
create_crud_routers(
    router=router,
    orm_class=ProjectOrm,
    create_pd=ProjectCreatePD,
    edit_pd=ProjectEditPD,
    list_pd=ProjectListPD,
    response_pd=ProjectPD,
    perm_list=['project'],
    model_name='project',
    cache_name='project',
    router_exclude=[]
)
