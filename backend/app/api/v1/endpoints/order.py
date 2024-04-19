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
from app.models.order.models import OrderOrm
from app.models.order.schemas import (
    OrderCreatePD, OrderPD, OrderSimplePD, OrderListPD, OrderEditPD
)
from app.api.v1 import create_crud_routers


router = APIRouter(prefix='/order',
                   tags=['order'])
# 此函数创建了 所有标准CRUD
create_crud_routers(
    router=router,
    orm_class=OrderOrm,
    create_pd=OrderCreatePD,
    edit_pd=OrderEditPD,
    list_pd=OrderListPD,
    response_pd=OrderPD,
    perm_list=['order'],
    model_name='order',
    cache_name='order',
    router_exclude=['download_many']
)
