#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2019-10-28
'''
路由注册
'''
from fastapi import Depends
from fastapi import APIRouter
# app
from app.core.jwt import CurrentUser
from app.core.config import API_PREFIX
from .endpoints.auth import router as auth
from .endpoints.role import router as role
from .endpoints.user import router as user
from .endpoints.config import router as config
from .endpoints.oem import router as oem
from .endpoints.project import router as project
from .endpoints.project_update import router as project_update
from .endpoints.project_oem import router as project_oem
from .endpoints.contact import router as contact
from .endpoints.post import router as post
from .endpoints.comment import router as comment
from .endpoints.order import router as order
from .endpoints.order_update import router as order_update
from .endpoints.product import router as product
from .endpoints.design import router as design
from .endpoints.pilot import router as pilot
from .endpoints.standard_design import router as standard_design
from .endpoints.design_module import router as design_module
from .endpoints.workgroup import router as workgroup

all_routers = APIRouter(prefix=API_PREFIX)
# auth 不要求登录
all_routers.include_router(auth)
all_routers.include_router(config)
# 要求SU
all_routers.include_router(role)
all_routers.include_router(user)
# 要求OEM(每个API单独)
all_routers.include_router(oem)
# 要求Project(每个API单独)
all_routers.include_router(project)
all_routers.include_router(project_update)
all_routers.include_router(project_oem)
# 要求Project(每个API单独)
all_routers.include_router(contact)
all_routers.include_router(post)
all_routers.include_router(comment)
all_routers.include_router(order)
all_routers.include_router(order_update)
all_routers.include_router(product)
all_routers.include_router(design)
all_routers.include_router(standard_design)
all_routers.include_router(pilot)
all_routers.include_router(design_module)
all_routers.include_router(workgroup)
# 要求登录
# all_routers.include_router(design_info,
#                            prefix='/design_info',
#                            tags=['design_info'])
# all_routers.include_router(design,
#                            prefix='/design',
#                            tags=['design'])
