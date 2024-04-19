#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-09-11


import datetime
from fastapi import APIRouter, Depends
# app level
from app.core.errors import HTTPException, MyExceptions
from app.core.jwt import CurrentUser
from app.models.user.models import UserOrm
from app.models.post.models import PostOrm
from app.models.post.schemas import PostCreatePD, PostPD, PostListPD
from app.models.base_pd import MsgResponese
from app.models.comment.models import CommentOrm
from app.models.comment.schemas import CommentCreatePD, CommentPD
from app.api.v1 import create_crud_routers


router = APIRouter(prefix='/post',
                   tags=['post'])

create_crud_routers(
    router=router,
    orm_class=PostOrm,
    create_pd=PostCreatePD,
    edit_pd=PostCreatePD,
    list_pd=PostListPD,
    response_pd=PostPD,
    perm_list=['post'],
    model_name='post',
    cache_name='post',
    router_exclude=['download_one']
)

'''
==================================== 非标
'''


@router.post(path='/{sid}/add-comment', response_model=CommentPD)
async def add_comment(sid: str, data: CommentCreatePD, cu: UserOrm = Depends(CurrentUser(perms=['post', 'comment']))):
    '''
    Summary:添加评论，返回添加的评论，在页面上可以直接增加
    '''
    post = PostOrm.get_by_sid_or_404(sid=sid)
    if not post.allowed_comment:
        raise HTTPException(status_code=403, detail='此日志不允许评论')
    comment = CommentOrm(**data.dict())
    comment.post_sid = post.sid
    comment.owner_sid = cu.sid
    comment.save()
    return comment


@router.post(path='/{sid}/delete-newest-comment', response_model=MsgResponese)
async def delete_newest_comment(sid: str, cu: UserOrm = Depends(CurrentUser(perms=['post', 'comment']))):
    '''
    Summary: 删除最新的 一个 comment
    '''
    obj = CommentOrm.objects(post_sid=sid, is_deleted=False).order_by(
        '-update_time').first()
    if not obj:
        return {'msg': 'No Comment under this Post'}
    if not cu.can(model='comment', action='delete', obj=obj):
        raise MyExceptions.permission_deny
    obj.delete()
    post = PostOrm.get_by_sid_or_404(sid=sid)
    post.save()
    return {'msg': 'Delete Newest comment success'}


@router.post(path='/{sid}/delete-oldest-comment', response_model=MsgResponese)
async def delete_newest_comment(sid: str, cu: UserOrm = Depends(CurrentUser(perms=['post', 'comment']))):
    '''
    Summary: 删除最old的 一个 comment
    '''
    obj = CommentOrm.objects(post_sid=sid, is_deleted=False).order_by(
        '+update_time').first()
    if not obj:
        return {'msg': 'No Comment under this Post'}
    if not cu.can(model='comment', action='delete', obj=obj):
        raise MyExceptions.permission_deny
    obj.delete()
    post = PostOrm.get_by_sid_or_404(sid=sid)
    post.save()
    return {'msg': 'Delete Oldest comment success'}
