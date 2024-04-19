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
from app.models.product.models import ProductOrm
from app.models.product.schemas import ProductPD, ProductCreatePD, ProductListPD
from app.core.config import MYCACHE
from app.api.v1 import create_crud_routers

router = APIRouter(prefix='/product',
                   tags=['product'])
# 此函数创建了 所有标准CRUD
create_crud_routers(
    router=router,
    orm_class=ProductOrm,
    create_pd=ProductCreatePD,
    edit_pd=ProductCreatePD,
    list_pd=ProductListPD,
    response_pd=ProductPD,
    perm_list=['product'],
    model_name='product',
    cache_name='product',
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
    ProductOrm.save_to_json()
    return {'msg': '成功保存到JSON文件'}


@router.post('/reset-product-database', response_model=MsgResponese)
async def reset_product_database(use_json: bool = True, cu: UserOrm = Depends(CurrentUser(su_required=True, perms=['product']))):
    '''
    Summary: 重置产品数据库
    '''
    ProductOrm.init_model(use_json=use_json)
    MYCACHE['product'] = ProductOrm.get_cache()
    return {'msg': '成功恢复'}
