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
from app.models.user.schemas import UserDbPD, UserCreatePD, UserSimplePD, UserListPD
from app.api.v1 import create_crud_routers
from app.core import config

router = APIRouter(prefix='/user',
                   tags=['user'],
                   dependencies=[
                       Depends(CurrentUser(su_required=True))
                   ])
# 此函数创建了 所有标准CRUD
create_crud_routers(
    router=router,
    orm_class=UserOrm,
    create_pd=UserCreatePD,
    edit_pd=UserCreatePD,
    list_pd=UserListPD,
    response_pd=UserDbPD,
    perm_list=['user'],
    model_name='user',
    cache_name='user',
    router_exclude=['download_one', 'download_many']
)


@router.post('/reset-password/{sid}', response_model=UserCreatePD)
async def reset_password(sid: str, cu: UserOrm = Depends(CurrentUser(su_required=True))):
    '''
    Summary: 重置密码为 邮箱
    '''
    user = UserOrm.get_active_by_sid_or_404(sid=sid)
    user.password = config.DEFAULT_USER_PASSWORD
    user.save()
    return user
