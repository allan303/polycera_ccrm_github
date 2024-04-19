#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2021-08-26

'''
Summary: Design  对 module 需要的必要参数接口
'''
from typing import Dict, Optional, List
from pydantic import BaseModel
from dataclasses import dataclass, field


class ModuleForDesignPD(BaseModel):
    '''
    Summary: 定义接口，设计必备的module信息
    '''
    name: Optional[str] = ''
    module_type: Optional[str] = 'spiral'
    brand: Optional[str] = ''
    model: Optional[str] = ''  # 型号
    fa: float = 0  # 面积
    is_contained_pv: bool = False  # 是否包含PV
    flux_per_bar_25: float = 80  # 标准透水性
    liter_inside: float = 40  # 内部体积
    spacer_mil: Optional[int] = 40  # 有格网
    module_size: Optional[str] = '8040'
    rej_dt: Dict = {'tds': 0, 'ss': 1}
    description: Optional[str] = ''

    class Config:
        orm_mode = True


@dataclass
class ModuleForDesign():
    '''
    Summary: 定义接口，设计必备的module信息
    '''
    name: Optional[str] = ''
    module_type: Optional[str] = 'spiral'
    brand: Optional[str] = ''
    model: Optional[str] = ''  # 型号
    fa: float = 0  # 面积
    is_contained_pv: bool = False  # 是否包含PV
    flux_per_bar_25: float = 80  # 标准透水性
    liter_inside: float = 40  # 内部体积
    spacer_mil: Optional[int] = 40  # 有格网
    module_size: Optional[str] = '8040'
    rej_dt: Dict = field(default_factory=dict)
    description: Optional[str] = ''
