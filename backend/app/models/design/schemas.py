from typing import Optional, List, Dict, Any
from pydantic import BaseModel
import datetime
# app
from app.models.base_pd import BaseDbWithOwnerPD, BaseDbPD, BaseListPD
from autodesign.designs.module_for_design import ModuleForDesignPD
from autodesign.designs.base_options import OptionAll, OptionRaw


class DesignDownloadContextPD(BaseModel):
    '''
    Summary: 下载时候传入的参数
    '''
    show_bom: bool = True
    show_tree: bool = False
    show_kw_consumer: bool = True
    show_cip: bool = True
    show_ceb: bool = True
    show_time: bool = True
    show_chem_consumer: bool = True


class DesignOptionCreatePD(BaseModel):
    '''
    Summary: Design option create
    '''
    name: Optional[str] = ''
    options: OptionAll = OptionAll()
    remark: Optional[str] = ''
    share_list: List[str] = []  # 用于控制share

    class Config:
        orm_mode = True


class DesignCreatePD(DesignOptionCreatePD):
    '''
    Summary: create
    '''
    project_sid: Optional[str] = ''
    oem_sid: Optional[str] = ''

    class Config:
        orm_mode = True


class OptionAllSimplePD(BaseModel):
    module: ModuleForDesignPD = ModuleForDesignPD()  # 膜组件
    raw_flow: OptionRaw = OptionRaw()  # 原水

    class Config:
        orm_mode = True


class DesignOptionSimplePD(BaseDbWithOwnerPD):
    '''
    Summary: Design option 选项
    '''
    name: Optional[str] = ''
    remark: Optional[str] = ''
    module_name: Optional[str] = ''

    class Config:
        orm_mode = True


class DesignSimplePD(DesignOptionSimplePD):
    '''
    Summary: 包含db信息、owner信息
    '''
    project_sid: Optional[str] = ''
    oem_sid: Optional[str] = ''
    project_name: Optional[str] = ''
    oem_name: Optional[str] = ''
    contact_name: Optional[str] = ''
    module_nums: Optional[int] = 0

    class Config:
        orm_mode = True


class DesignOptionPD(DesignOptionSimplePD):
    options: OptionAll = OptionAll()

    class Config:
        orm_mode = True


class DesignPD(DesignSimplePD):
    design_result: dict = {}  # 保存设计结果 通过clean
    options: OptionAll = OptionAll()

    class Config:
        orm_mode = True


class DesignOptionListPD(BaseListPD):
    objs: List[DesignOptionSimplePD] = []


class DesignListPD(BaseListPD):
    objs: List[DesignSimplePD] = []
