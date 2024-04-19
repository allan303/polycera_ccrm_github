#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-09-11
from fastapi import Depends, APIRouter, Request
from app.core.jwt import CurrentUser
from typing import Optional
# app level
from app.models.user.models import UserOrm
from app.models.config.models import ConfigOrm, create_default_config
from app.models.config.schemas import ConfigPD, ConfigListPD
from app.core.config import MYCACHE
from app.api.v1 import create_crud_routers
from app.models.permission.schemas import perm_option

# 实例化 APIRouter，并将本页所有URL挂到此router下
router = APIRouter(prefix='/config',
                   tags=['config'])

# 此函数创建了 所有标准CRUD
# create_crud_routers(
#     router=router,
#     orm_class=ConfigOrm,
#     create_pd=ConfigPD,
#     list_pd=ConfigListPD,
#     response_pd=ConfigPD,
#     perm_list=['config'],
#     model_name='config',
#     cache_name='config'
# )


@router.get('/read', response_model=ConfigPD)
async def read(cu: UserOrm = Depends(CurrentUser(admin_required=True))):
    '''
    Summary: 配置 信息
    '''
    c = ConfigOrm.objects.first()
    return c


@router.post('/edit', response_model=ConfigPD)
async def edit(data: ConfigPD, cu: UserOrm = Depends(CurrentUser(admin_required=True))):
    '''
    Summary: 配置 信息
    '''
    c = ConfigOrm.objects.first()
    c.update(**data.dict())
    MYCACHE['config'] = ConfigOrm.get_cache()
    return c


@router.post('/reset/{key}', response_model=ConfigPD)
async def reset(key: Optional[str], cu: UserOrm = Depends(CurrentUser(admin_required=True))):
    '''
    Summary: 配置 恢复默认
    '''
    c = ConfigOrm.objects.first()
    if not key:
        ConfigOrm.init_model()  # 全部重置
        c = ConfigOrm.objects.first()
    else:
        default = create_default_config()
        if hasattr(c, key):
            setattr(c, key, default[key])
        c.save()
    MYCACHE['config'] = ConfigOrm.get_cache()
    return c


@router.post('/perm-option')
async def perm_option(cu: UserOrm = Depends(CurrentUser())):
    '''
    Summary: Perm相关配置
    '''
    return {'perm_option': perm_option}
