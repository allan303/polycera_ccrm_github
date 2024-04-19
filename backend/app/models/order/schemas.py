from typing import Optional, List, Any
from pydantic import BaseModel
import datetime
# app
from app.models.base_pd import BaseDbWithOwnerPD, BaseListPD


class OrderProductCreatePD(BaseModel):
    '''
    Summary: 订单中的产品
    '''
    brand: str = 'Polycera'
    name: str = ''  # AUTO
    model: str = ''  # AUTO
    description: Optional[str] = ''  # 可手动
    unit_price: Optional[float] = 0
    unit:  Optional[str] = ''
    nums: Optional[float] = 0

    class Config:
        orm_mode = True


class OrderProductPd(OrderProductCreatePD):
    '''
    Summary: 无价格
    '''

    class Config:
        orm_mode = True


class ContactInfoPD(BaseModel):
    '''
    Summary: 收货/发票联系人
    '''
    name:  Optional[str] = ''
    phone:  Optional[str] = ''
    address:  Optional[str] = ''

    class Config:
        orm_mode = True


class OrderEditPD(BaseModel):
    '''
    Summary: 订单信息
    '''
    oem_sid:  Optional[str] = ''
    project_sid:  Optional[str] = ''
    oem_sid:  Optional[str] = ''
    contact_sid:  Optional[str] = ''
    products: List[OrderProductPd] = []  # 产品信息
    payment_term:  Optional[str] = f'100%全款'
    shipment_term:  Optional[str] = '1周内'
    shipment_contact: ContactInfoPD = ContactInfoPD()  # 收货信息
    invoice_contact: ContactInfoPD = ContactInfoPD()  # 发票邮寄
    remark:  Optional[str] = ''  # 备注
    share_list: List[str] = []  # 用于控制share
    free: bool = False

    class Config:
        orm_mode = True


class OrderCreatePD(OrderEditPD):
    '''
    Summary: 订单信息
    '''
    order_date: Optional[datetime.date] = None
    status: Optional[str] = ""

    class Config:
        orm_mode = True


class OrderSimplePD(OrderEditPD, BaseDbWithOwnerPD):
    '''
    Summary: 前台list
    '''
    oem_sid: Optional[str] = ''
    project_sid: Optional[str] = ''
    oem_sid: Optional[str] = ''
    contact_sid: Optional[str] = ''
    # auto
    name: Optional[str] = ''  # 自动生成的订单编号
    order_date: Optional[datetime.date] = None
    oem_name: Optional[str] = ''
    project_name: Optional[str] = ''
    oem_name: Optional[str] = ''
    contact_name: Optional[str] = ''
    price: Optional[float] = ''
    price_cn: Optional[str] = ''
    status: Optional[str] = ""

    class Config:
        orm_mode = True


class OrderPD(OrderSimplePD):
    '''
    Summary: 带价格信息
    '''
    products: List[OrderProductPd] = []  # 产品信息
    payment_term: Optional[str] = f'100%全款'
    shipment_term: Optional[str] = '1周内'
    shipment_contact: ContactInfoPD = ContactInfoPD()  # 收货信息
    invoice_contact: ContactInfoPD = ContactInfoPD()  # 发票邮寄
    price: Optional[float] = ''
    price_cn: Optional[str] = ''


class OrderListPD(BaseListPD):
    objs: List[OrderSimplePD] = []


'''
以下 order_update
'''


class OrderUpdateCreatePD(BaseModel):
    order_sid: Optional[str] = ''
    status: Optional[str] = ''
    remark: Optional[str] = ''

    class Config:
        orm_mode = True


class OrderUpdatePD(OrderUpdateCreatePD, BaseDbWithOwnerPD):
    # auto
    order_name: Optional[str] = ''
    owner_name: Optional[str] = ''

    class Config:
        orm_mode = True


class OrderUpdateListPD(BaseListPD):
    objs: List[OrderUpdatePD] = []
    # objs: List[Any] = []

    class Config:
        orm_mode = True
