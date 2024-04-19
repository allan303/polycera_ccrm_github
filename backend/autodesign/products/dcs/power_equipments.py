#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# File    :   pump.py
# Time    :   2019/01/14 00:10:18
# Author  :   Jack Li
# Contact :   allanth3@163.com


'''
PowerEquipment:包含各类动力设备：(除水泵)、搅拌机等
'''
from dataclasses import dataclass, field
from jackutils.list_tool import find_x
from autodesign.core import const
from autodesign.products.base_product import BaseProductMixin


'''
搅拌机
'''


@dataclass
class Agitator(BaseProductMixin):
    catalog: str = '7.1.1'
    # spec: str = '直联式桨叶'
    material: str = '碳钢衬胶轴浆'
    kw: float = 0  # 功率
    blade_width_ratio: float = 0.25  # 桨径罐径比，涡轮式叶轮的d/D一般为0.25~0.5
    blade_length_mm: int = 500  # 桨叶长度 = tank_L * blade_width_ratio ,元整到 500mm
    # InitVar
    tank: field = None  # 用tank进行初始化

    def __post_init__(self):
        if self.tank:
            self.kw = find_x(x=self.tank.v * 0.23,
                             y_list=const.KW_LIST, use_larger=True)  # mm
            self.set_blade_length_mm()
        if not self.spec:
            self.set_spec()

    @property
    def diameter(self):
        # 水池 直径
        if not self.tank:
            return None
        if self.tank.form == 'square':
            diameter = min(self.tank.L, self.tank.W)  # 长宽取小
        else:
            diameter = self.tank.diameter
        if not diameter:
            return None
        return diameter

    def set_blade_length_mm(self):
        if not self.diameter:
            self.blade_length_mm = 500
        self.blade_length_mm = find_x(x=self.diameter * self.blade_width_ratio*1000,
                                      y_list=const.BLADE_D_LIST)

    def set_spec(self):
        # self.spec = '叶轮直径{}mm,{}kw'.format(
        #     self.blade_length_mm, self.kw)
        self.spec = f'{self.kw}kw'

    @property
    def real_d_D(self):
        # 实际桨径比
        if self.diameter:
            return self.blade_length_mm/self.diameter / 1000
        return None


'''
加热器
'''


@dataclass
class HeatExchanger(BaseProductMixin):
    catalog: str = '7.2'
    v: float = 0

    def set_kw(self):
        dt = const.HEAT_EXCHANGE_KW
        ls = list(dt.keys())
        v = find_x(x=self.v, y_list=ls)
        self.kw = dt[v]

    def set_spec(self):
        self.spec = f'{self.kw}kw,380V,配温度控制'


@dataclass
class AirCompressor(BaseProductMixin):
    '''
    空压机
    '''
    catalog: str = '7.3'
    q: float = 0.3
    p: float = 8  # 压力
    kw: float = 1.1
    kw_k: float = 0.3

    def __post_init__(self):
        self.spec = f'{self.q}m3/min,{self.p}bar,{self.kw}kw'
