from typing import Optional, List
import datetime
from pydantic import BaseModel
from app.models.base_pd import BaseModel, BaseDbPD, BaseDbWithOwnerPD, BaseListPD


class ProjectOemCreatePD(BaseModel):
    project_sid: str = ''
    oem_sid: str = ''
    is_filing: bool = False
    remark: str = ''


class ProjectOemPD(ProjectOemCreatePD, BaseDbWithOwnerPD):
    # AUTO
    ...


class ProjectOemListPD(BaseListPD):
    objs: List[ProjectOemPD] = []


class ProjectUpdateCreatePD(BaseModel):
    project_sid: str = ''
    pjstage: Optional[str] = '线索'  # 项目阶段
    win_percentage: Optional[int] = 10  # 成功率权重
    forecast_date: Optional[datetime.date] = None
    remark: str = ''

    class Config:
        orm_mode = True


class ProjectUpdatePD(ProjectUpdateCreatePD, BaseDbWithOwnerPD):
    ...


class ProjectUpdateListPD(BaseListPD):
    objs: List[ProjectUpdatePD] = []


class ProjectEditPD(BaseModel):
    name: Optional[str] = ''
    location: Optional[str] = ''  # 地区
    industry: Optional[str] = ''  # 行业
    pjtype: Optional[str] = ''  # 新建
    source: Optional[str] = ''  # 来源
    remark: Optional[str] = ''
    forecast_amount: Optional[float] = 0
    module: Optional[str] = ''
    module_nums: Optional[int] = 0
    share_list: List[str] = []  # 用于控制share

    class Config:
        orm_mode = True


class ProjectCreatePD(ProjectEditPD):
    pjstage: Optional[str] = ''  # 项目阶段(当前)
    win_percentage: Optional[int] = 0  # 成功率权重(当前)
    forecast_date: Optional[datetime.date] = None
    forecast_amount_cal: Optional[float] = 0

    class Config:
        orm_mode = True


class ProjectSimplePD(ProjectCreatePD, BaseDbWithOwnerPD):
    '''
    Summary: 前台list(Project 先全部)
    '''
    pjstage: Optional[str] = ''  # 项目阶段(当前)
    win_percentage: Optional[int] = 0  # 成功率权重(当前)
    forecast_date: Optional[datetime.date] = None
    forecast_amount_cal: Optional[float] = 0
    filing_summary: Optional[str] = ''

    class Config:
        orm_mode = True


class ProjectPD(ProjectSimplePD):
    '''
    Summary:
    '''
    # have_pilot: bool = False
    ...

    class Config:
        orm_mode = True


class ProjectListPD(BaseListPD):
    objs: List[ProjectSimplePD] = []


class ProjectManyToExcelPD(BaseModel):
    '''
    Summary: to excel 的pd，直接用这个比较方便
    '''
    _columns = ['创建时间', 'OWNER', '项目名称', '地区', '行业', '类型', '来源', '阶段', '成功率',
                '备案情况', '膜型号', '膜数量', '预测日期',  '备注']
    create_date_local_str: Optional[str] = ''
    owner_name: str = ''
    name: Optional[str] = ''
    location: Optional[str] = ''  # 地区
    industry: Optional[str] = ''  # 行业
    pjtype: Optional[str] = ''  # 新建
    source: Optional[str] = ''  # 来源
    pjstage: Optional[str] = ''  # 项目阶段(当前)
    win_percentage: Optional[int] = 0  # 成功率权重(当前)
    filing_summary: Optional[str] = ''  # 备案情况
    module: Optional[str] = ''  # 膜型号
    module_nums: Optional[int] = 0
    forecast_date: Optional[datetime.date] = None
    remark: Optional[str] = ''

    class Config:
        orm_mode = True
