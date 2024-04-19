from pydantic import BaseModel
from typing import List, Optional
from app.models.base_pd import BaseDbPD, BaseListPD


class ProductCreatePD(BaseModel):
    name: Optional[str] = ''
    brand: Optional[str] = ''
    model: Optional[str] = ''
    description: Optional[str] = ''
    unit_price: Optional[float] = 0
    unit: Optional[str] = '支'
    remark: Optional[str] = ''

    class Config:
        orm_mode = True


class ProductPD(ProductCreatePD, BaseDbPD):
    '''
    Summary: 用于订单 的产品
    NOTE： 默认包含所有膜元件产品，还可以添加其他
    '''


class ProductListPD(BaseListPD):
    objs: List[ProductPD] = []
