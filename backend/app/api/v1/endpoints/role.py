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
from app.models.role.models import RoleOrm
from app.models.role.schemas import RoleCreatePD, RolePD, RoleListPD, RoleEditPD
from app.api.v1 import create_crud_routers
from app.models.base_pd import MsgResponese

router = APIRouter(prefix='/role',
                   tags=['role'],
                   dependencies=[
                       Depends(CurrentUser(su_required=True))
                   ])
# 此函数创建了 所有标准CRUD
create_crud_routers(
    router=router,
    orm_class=RoleOrm,
    create_pd=RoleCreatePD,
    edit_pd=RoleEditPD,
    list_pd=RoleListPD,
    response_pd=RolePD,
    perm_list=['role'],
    model_name='role',
    cache_name='role',
    router_exclude=['download_one', 'download_many']
)


@router.post(path='/save-to-json', response_model=MsgResponese)
async def save_to_json():
    '''
    Summary: 保存到JSON，仅限 SU
    '''
    RoleOrm.save_perms_to_json()
    return {'msg': '成功保存到JSON文件'}
