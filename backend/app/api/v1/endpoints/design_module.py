#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-09-11
'''
SU操作： 目前只有新建用户
'''

from fastapi import APIRouter, Depends
# app level
from app.core.jwt import CurrentUser
from app.models.user.models import UserOrm
from app.models.base_pd import MsgResponese, SidResponese, IntResponese
from app.models.design_module.models import DesignModuleOrm
from app.models.design_module.schemas import DesignModuleCreatePD, DesignModulePD, DesignModuleListPD
from app.api.v1 import create_crud_routers

router = APIRouter(prefix='/design_module',
                   tags=['design_module'])
# 此函数创建了 所有标准CRUD
create_crud_routers(
    router=router,
    orm_class=DesignModuleOrm,
    create_pd=DesignModuleCreatePD,
    edit_pd=DesignModuleCreatePD,
    list_pd=DesignModuleListPD,
    response_pd=DesignModulePD,
    perm_list=['design_module'],
    model_name='design_module',
    cache_name='design_module',
    router_exclude=['download_one', 'download_many']
)

'''
================== 非标
'''


@router.post(path='/save-to-json', response_model=MsgResponese)
async def save_to_json(cu: UserOrm = Depends(CurrentUser(su_required=True, perms=['product']))):
    '''
    Summary: 保存到JSON，仅限 SU
    '''
    DesignModuleOrm.save_to_json()
    return {'msg': '成功保存到JSON文件'}
