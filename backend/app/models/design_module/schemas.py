from pydantic import BaseModel
from typing import List, Optional, Dict, Optional
from app.models.base_pd import BaseDbPD, BaseListPD


class DesignModuleCreatePD(BaseModel):
    name: Optional[str] = ''
    material: Optional[str] = ''  # 材质
    membrane_type: Optional[str] = ''
    module_type: Optional[str] = ''
    brand: Optional[str] = ''
    model: Optional[str] = ''
    fa: float = 0
    is_contained_pv: bool = False
    flux_per_bar_25: float = 80
    liter_inside: float = 20
    spacer_mil: float = 0
    module_size: Optional[str] = ''
    rej_dt: Optional[Dict] = {}
    description: Optional[str] = ''

    class Config:
        orm_mode = True


class DesignModulePD(DesignModuleCreatePD, BaseDbPD):
    '''
    Summary: 用于订单 的产品
    NOTE： 默认包含所有膜元件产品，还可以添加其他
    '''
    class Config:
        orm_mode = True


class DesignModuleListPD(BaseListPD):
    objs: List[DesignModulePD] = []

    class Config:
        orm_mode = True
