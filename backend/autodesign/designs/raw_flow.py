#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-04-23

'''
接收原水信息
'''

from typing import Optional
from pydantic.main import BaseModel


'''
接受输入的原水参数
'''
'''
=====================以下为 Option ====================
'''

# class ConcsDt(OrmModePD):
#     cod:float=0
#     tds:float=0
#     ss:float = 0
#     oil:float = 0
#     ntu:float = 0


class OptionRaw(BaseModel):
    '''
    Summary: 原水 option 
    '''
    name: str = '原水'
    wwtype: str = '地表水'
    ph: float = 7
    q: float = 0  # feed_q
    q_unit: str = 'm3/h'
    hpd: float = 24  # 系统的运行时间，单个产品的运行时间各异
    temp: float = 25  # 作为基础参数
    # density_kg_l: float = 1  # 密度，用于换算 ppm
    # 以下为浓度参数
    concs_dt: Optional[dict] = {
        'cod': 0,
        'tds': 0,
        'ss': 0,
        'ntu': 0,
        'oil': 0
    }
    remark: Optional[str] = ''  #
    water_solution: str = 'nacl'  # 用于RO系统  溶液体系，计算渗透压

    class Config:
        orm_mode = True
    # @validator('q')
    # def validate_q(cls, v):
    #     if v <= 0:
    #         raise ValueError('水量必须>0')
    #     return v


'''
=====================以下为 dc （直接使用FlowDc）====================
'''
