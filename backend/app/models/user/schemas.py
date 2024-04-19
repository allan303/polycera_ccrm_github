from bson import ObjectId
from pydantic import BaseModel
import datetime
from typing import Optional, Sequence, List
# app
from app.models.base_pd import BaseDbPD, BaseListPD
from app.models.role.schemas import RoleSimplePD


class UserConfig(BaseModel):
    locale: Optional[str] = 'zh'
    use_half: Optional[bool] = False

    class Config:
        orm_mode = True


class UserBasePD(BaseModel):
    company: Optional[str] = ''
    title: Optional[str] = ''
    country: Optional[str] = 'China'
    province: Optional[str] = 'shanghai'  # 地区
    gender: Optional[str] = ''  # 1 男 2女 0未知
    remark: Optional[str] = ''


class ProfileEditPD(UserBasePD):
    '''
    Summary: 编辑 profile,仅本人可以更新 自己的config
    '''
    user_config: UserConfig = UserConfig()

    class Config:
        orm_mode = True


class UserCreatePD(UserBasePD):
    '''
    Summary: 创建用户(SU)
    '''
    username: Optional[str] = ''
    name: Optional[str] = ''
    name_en: Optional[str] = ''
    email: Optional[str] = ''
    phone: Optional[str] = ''
    role_sid: Optional[str] = ''
    workgroup_sid: Optional[str] = ''
    remark: Optional[str] = ''
    user_config: UserConfig = UserConfig()

    class Config:
        orm_mode = True


class UserSimplePD(BaseDbPD, UserCreatePD):
    '''
    Summary: DB 提取
    '''
    user_config: UserConfig
    role_name: str = ''
    workgroup_name: str = ''
    is_su: bool = False
    last_seen_local: Optional[datetime.datetime] = None

    class Config:
        orm_mode = True


class UserDbPD(UserSimplePD):
    '''
    Summary: 带有 Role 信息
    '''
    perm: dict = {}

    class Config:
        orm_mode = True


class UserListPD(BaseListPD):
    objs: List[UserSimplePD] = []
