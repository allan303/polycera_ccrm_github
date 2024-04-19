from typing import Optional, List, Union
from pydantic import BaseModel
import datetime
# appp
from app.models.base_pd import BaseModel, BaseDbPD, BaseDbWithOwnerPD, BaseListPD


class PilotCreatePD(BaseModel):
    '''
    Summary: 
    '''
    name: str = ''
    project_sid: str = ''
    oem_sid: str = ''
    location: str = ''
    industry: str = ''
    start: Optional[datetime.date] = None
    end: Optional[datetime.date] = None
    remark: str = ''
    share_list: List[str] = []  # 用于控制share

    class Config:
        orm_mode = True


class PilotSimplePD(BaseDbWithOwnerPD):
    '''
    Summary: # 只提取前台 listComponent需要的参数
    '''
    name: str = ''
    project_sid: str = ''
    oem_sid: str = ''
    location: str = ''
    industry: str = ''
    remark: str = ''  # 备注
    # auto
    project_name: str = ''
    oem_name: str = ''

    class Config:
        orm_mode = True


class PilotPD(PilotSimplePD):
    '''
    Summary: 详细信息中
    '''
    start: Optional[datetime.date] = None
    end: Optional[datetime.date] = None
    remark: str = ''

    class Config:
        orm_mode = True


class PilotListPD(BaseListPD):
    objs: List[PilotSimplePD] = []
