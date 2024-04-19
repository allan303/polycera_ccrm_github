from typing import Optional, List
from pydantic import BaseModel, EmailStr
from app.models.base_pd import BaseDbPD,  BaseListPD


class SendEmail(BaseModel):
    # 用于 发送邮件
    title: str = ''
    message: str = ''
    tos: List[EmailStr] = []


class PjstagePD(BaseModel):
    name: str
    win_percentage: int


class WwtypePD(BaseModel):
    name: str
    flux_min: float
    flux_max: float


class ChemPD(BaseModel):
    text: str
    value: str


class ConfigPD(BaseModel):
    '''
    Summary: 所有 config 
    '''
    location: List[str]
    source: List[str]
    industry: List[str]
    pjtype: List[str]
    wwtype: List[str]
    pjstage: List[PjstagePD]
    oemtype: List[str]
    department: List[str]
    title: List[str]
    product_units: List[str]
    order_status: List[str]
    chem: List[ChemPD]

    class Config:
        orm_mode = True


class ConfigListPD(BaseListPD):
    objs: List[ConfigPD] = []
