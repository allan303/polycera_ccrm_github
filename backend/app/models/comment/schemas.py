from typing import Optional, List
from pydantic import BaseModel
from mongoengine import StringField, DateTimeField
# app
from app.models.base_pd import BaseDbPD, BaseDbWithOwnerPD, BaseListPD


class CommentCreatePD(BaseModel):
    '''
    Summary: 评论（包含在 Post 中）
    '''
    post_sid: str = ''
    body: str = ''
    at_users_sid: List[str] = []  # @ 的用户，后期用于 消息提醒
    quote_comment: str = ''

    class Config:
        orm_mode = True


class CommentPD(CommentCreatePD, BaseDbWithOwnerPD):
    '''
    Summary: 
    '''
    class Config:
        orm_mode = True


class CommentListPD(BaseListPD):
    objs: List[CommentPD] = []
