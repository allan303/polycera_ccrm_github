#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2021-11-03
'''
Summary: 将所有modelOrm 集中到此处，Mapping，便于使用
'''
from typing import List
from .user.models import UserOrm
from .role.models import RoleOrm
from .project.models import ProjectOrm, ProjectOemOrm, ProjectUpdateOrm
from .product.models import ProductOrm
from .post.models import PostOrm
from .pilot.models import PilotOrm
from .order.models import OrderOrm, OrderUpdateOrm
from .oem.models import OemOrm
from .design_module.models import DesignModuleOrm
from .design.models import DesignOrm, StandardDesignOrm
from .contact.models import ContactOrm
from .config.models import ConfigOrm
from .comment.models import CommentOrm
from .workgroup.models import WorkgroupOrm


def get_models_list() -> List:
    return [UserOrm,
            RoleOrm,
            ProjectOrm, ProjectOemOrm, ProjectUpdateOrm,
            ProductOrm,
            PostOrm,
            PilotOrm,
            OrderOrm, OrderUpdateOrm,
            OemOrm,
            DesignModuleOrm,
            DesignOrm, StandardDesignOrm,
            ContactOrm,
            ConfigOrm,
            CommentOrm]


def get_models_dt():
    models_ls = get_models_list()
    return {x._classname: x for x in models_ls}


MODELS_DT = get_models_dt()
