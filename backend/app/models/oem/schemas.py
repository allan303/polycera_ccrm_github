from typing import Optional, List
from pydantic import BaseModel
from app.models.base_pd import BaseDbWithOwnerPD, BaseDbPD, BaseListPD


class OemCreatePD(BaseModel):
    name: str = ''
    location: str = ''
    oemtype: str = ''
    # 开票信息
    company_code: str = ''  # 税号
    company_address: str = ''  # 开票地址
    company_bank: str = ''  # 银行
    company_bank_account: str = ''  # 银行账户
    company_telephone: str = ''  # 电话
    company_zipcode: str = ''  # 邮编
    # 通讯地址
    remark: str = ''  # 备注
    share_list: List[str] = []  # 用于控制share

    class Config:
        orm_mode = True


class OemSimplePD(BaseDbWithOwnerPD):
    '''
    Summary: 提供前台list
    '''
    name: str = ''
    location: str = ''
    oemtype: str = ''
    remark: str = ''  # 备注


class OemPD(OemSimplePD):
    '''
    Summary: 不含owner信息，用于list-me
    '''
    # 开票信息
    company_code: str = ''  # 税号
    company_address: str = ''  # 开票地址
    company_bank: str = ''  # 银行
    company_bank_account: str = ''  # 银行账户
    company_telephone: str = ''  # 电话
    company_zipcode: str = ''  # 邮编
    # 通讯地址
    remark: str = ''  # 备注

    class Config:
        orm_mode = True


class OemListPD(BaseListPD):
    objs: List[OemSimplePD] = []
