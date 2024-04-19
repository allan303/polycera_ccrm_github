#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-09-11


from fastapi import APIRouter
# app level

from app.models.comment.models import CommentOrm
from app.models.comment.schemas import CommentCreatePD, CommentPD, CommentListPD
from app.api.v1 import create_crud_routers


router = APIRouter(prefix='/comment',
                   tags=['comment'])

create_crud_routers(
    router=router,
    orm_class=CommentOrm,
    create_pd=CommentCreatePD,
    edit_pd=CommentCreatePD,
    list_pd=CommentListPD,
    response_pd=CommentPD,
    perm_list=['post', 'comment'],
    model_name='comment',
    cache_name='comment',
    router_exclude=['download_one', 'download_many']
)
