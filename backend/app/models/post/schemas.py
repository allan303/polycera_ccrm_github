from typing import Optional, List
from pydantic import BaseModel
from mongoengine import StringField, DateTimeField
# app
from app.models.base_pd import BaseDbPD, BaseDbWithOwnerPD, BaseListPD
from app.models.comment.schemas import CommentPD


class PostCreatePD(BaseModel):
    '''
    Summary: 评论（包含在 Post 中）
    '''
    project_sid: Optional[str] = ''
    oem_sid: Optional[str] = ''
    contact_sid: Optional[str] = ''
    order_sid: Optional[str] = ''
    pilot_sid: Optional[str] = ''
    body: Optional[str] = ''
    share_list: List[str] = []  # 用于控制share

    class Config:
        orm_mode = True


class PostPD(PostCreatePD, BaseDbWithOwnerPD):
    '''
    Summary: 
    '''
    last_comment_time_str: str = ''
    comments_count: int = 0
    project_name: str = ''
    oem_name: str = ''
    contact_name: str = ''
    order_name: str = ''
    pilot_name: str = ''
    comments: List[CommentPD] = []
    is_system: bool = False

    class Config:
        orm_mode = True


class PostListPD(BaseListPD):
    objs: List[PostPD] = []


class PostManyToExcelPD(BaseModel):
    '''
    Summary: to excel 的pd，直接用这个比较方便
    '''
    _columns = ['创建时间', 'OWNER', '关联项目', '关联客户', '关联联系人', '关联订单', '关联实验', '内容']
    create_date_local_str: Optional[str] = ''
    owner_name: str = ''
    project_name: str = ''
    oem_name: str = ''
    contact_name: str = ''
    order_name: str = ''
    pilot_name: str = ''
    body_str: str = ''

    class Config:
        orm_mode = True
