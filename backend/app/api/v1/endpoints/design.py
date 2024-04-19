#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-09-11
'''
SU操作： 目前只有新建用户
'''

from fastapi import APIRouter, Depends
from starlette.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
from app.core.jwt import CurrentUser, MyExceptions

from app.models.user.models import UserOrm
from app.models.base_pd import MsgResponese, SidResponese, IntResponese
from app.models.design.models import DesignOrm
from app.models.design.schemas import (
    DesignCreatePD, DesignSimplePD, DesignPD, DesignListPD
)
from app.api.v1 import create_crud_routers

router = APIRouter(prefix='/design',
                   tags=['design'])

# 此函数创建了 所有标准CRUD
create_crud_routers(
    router=router,
    orm_class=DesignOrm,
    create_pd=DesignCreatePD,
    edit_pd=DesignCreatePD,
    list_pd=DesignListPD,
    response_pd=DesignPD,
    perm_list=['design'],
    model_name='design',
    cache_name='design',
    router_exclude=['download_many']
)


@router.post(path='/save-to-standard-design', response_model=SidResponese)
async def save_to_standard_design(cu: UserOrm = Depends(CurrentUser(perms=['standard_design']))):
    '''
    Summary: 保存到JSON，仅限 SU
    '''
    DesignModuleOrm.save_to_json()
    return {'msg': '成功保存到JSON文件'}
