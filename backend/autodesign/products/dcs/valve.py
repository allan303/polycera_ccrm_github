#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# File    :   valves.py
# Time    :   2019/01/14 00:10:32
# Author  :   Jack Li
# Contact :   allanth3@163.com


'''
Valve: 包含各种阀门
**传递时候全部采用基本数据结构：list/tuple/dict，不传入自定义class
'''
from dataclasses import dataclass
# app
from autodesign.products.base_product import BaseProductMixin


@dataclass
class Valve(BaseProductMixin):
    '''
    阀门: Valve
    '''
    catalog: str = '2'
    cad_tag: str = 'V'
    brand: str = ''
    standard: str = 'cn'
    description: str = ''
    unit: str = 'pcs'
    pn: int = 0  # 公称压力 bar
    dn: int = 0
    material: str = ''
    # 以下为dataclass 动态值
    pid_id: str = ''
    label: str = 'valve'  # 在系统内的标签：主材,阀门..等
    place: str = ''  # 安装位置
    sort_id: float = 0  # 排序值
    required: bool = True  # 可选？
    warning: str = ''
    remark: str = ''
    spec: str = ''
    valve_type: str = ''
    #
    power: str = ''  # 控制方式

    @property
    def control_str(self):
        dt = {
            'manual': '手动',
            'gas': '气动',
            'electric': '电动'
        }
        return dt.get(self.power, '')

    def set_spec(self):
        '''
        Summary: 根据 level2 进行设置
        '''
        if not self.valve_type:
            if self.dn <= 50:
                self.valve_type = '球阀'
            else:
                self.valve_type = '蝶阀'
            if not self.spec:
                if str(self.standard).lower() == 'us':
                    self.spec = f'{self.dn_inch},{self.control_str}{self.valve_type}'
                else:
                    self.spec = f'DN{self.dn},{self.control_str}{self.valve_type}'
        else:
            if not self.spec:
                if str(self.standard).lower() == 'us':
                    self.spec = f'{self.dn_inch},{self.product_name}'
                else:
                    self.spec = f'DN{self.dn},{self.product_name}'
