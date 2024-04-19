from typing import Optional, List
from pydantic import BaseModel
from app.models.base_pd import BaseDbWithOwnerPD,  BaseDbPD, BaseListPD


class ContactCreateRawPD(BaseModel):
    name: str = ''
    oem_sid: str = ''
    department: str = ''
    title: str = ''
    phone: str = ''
    email: str = ''
    address: str = ''
    remark: str = ''
    share_list: List[str] = []  # 用于控制share

    class Config:
        orm_mode = True


class ContactCreatePD(ContactCreateRawPD):

    new_oemname: Optional[str] = None
    new_oemtype: Optional[str] = None

    class Config:
        orm_mode = True


class ContactSimplePD(BaseDbWithOwnerPD):
    '''
    Summary: 不含owner 信息，用于 list-me
    '''
    name: str = ''
    oem_sid: str = ''
    department: str = ''
    title: str = ''
    oem_name: str = ''
    remark: str = ''

    class Config:
        orm_mode = True


class ContactPD(ContactSimplePD):
    '''
    Summary: 不含owner 信息，用于 list-me
    '''
    phone: str = ''
    email: str = ''
    address: str = ''
    remark: str = ''

    class Config:
        orm_mode = True


class ContactListPD(BaseListPD):
    objs: List[ContactSimplePD] = []


class ContactCreateWithOemNamePD(BaseModel):
    '''
    Summary: 新增联系人，带公司名称
    '''
    contact: ContactCreateRawPD = ContactCreateRawPD()
    oem_name: Optional[str] = ''
