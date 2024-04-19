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
from app.models.order.models import OrderUpdateOrm
from app.models.order.schemas import (
    OrderUpdateCreatePD, OrderUpdatePD, OrderUpdateListPD,
)
from app.api.v1 import create_crud_routers


router = APIRouter(prefix='/order_update',
                   tags=['order_update'])
# 此函数创建了 所有标准CRUD
create_crud_routers(
    router=router,
    orm_class=OrderUpdateOrm,
    create_pd=OrderUpdateCreatePD,
    edit_pd=OrderUpdateCreatePD,
    list_pd=OrderUpdateListPD,
    response_pd=OrderUpdatePD,
    perm_list=['order'],
    model_name='order',
    cache_name=None,
    router_exclude=['download_one', 'download_many']
)
