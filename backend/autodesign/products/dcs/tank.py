#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# File    :   tanks.py
# Time    :   2019/01/14 00:10:23
# Author  :   Jack Li
# Contact :   allanth3@163.com


'''
Tank:包含池子、以及与池子密切相关的设备
**传递时候全部采用基本数据结构：list/tuple/dict，不传入自定义class
1）Tank:水池/水槽
2）TankRound:圆形水池
3) TankSquare:方形水池

'''
from dataclasses import dataclass
from autodesign.core import const
from autodesign.products.base_product import BaseProductMixin
from .pipe import Pipe

'''
Tank:池子(0)
'''


@dataclass
class Tank(BaseProductMixin):  # 池子
    catalog: str = '5.2'
    description: str = ''
    unit: str = 'set'
    # self
    q: float = 0  # 流入的流量
    hrt: float = 0  # 停留时间，默认0.5hr
    v: float = 0  # 有效体积
    material: str = ''  # 材质
    height: float = 0  # Height高度 m 实际高度，不包括H_add
    h_add: float = 0.4  # 超高 m
    bottom_area: float = 0
    tank_size: str = ''
    spec: str = ''

    def set_spec(self):
        if not self.v:
            if self.q and self.hrt:
                self.v = self.q * self.hrt
        if self.v >= 10:
            self.spec = f'有效容积{self.v:.0f}m3'
        else:
            self.spec = f'有效容积{self.v:.1f}m3'

    @property
    def h_total(self):
        # 总高 （考虑超高）
        return self.height + self.h_add

    def get_drain_pipe(self, minutes: float = 10):
        '''
        Summary: 排空阀DN计算，默认按照30分钟排空
        '''
        return Pipe(s=1, q=self.v/minutes*60)


'''
Tank： Square 方形池子(1)
'''


@dataclass
class TankSquare(Tank):
    '''方形池子'''
    # old
    catalog: str = '5.2.1'
    form: str = 'square'
    width: float = 0  # Width宽度 m
    length: float = 0  # Length长度 m
    height_width: float = 1  # 默认比例 height/width = height_width
    length_width: float = 1  # length/width = length_width
    remark: str = ''

    def __post_init__(self):  # 可以接受所有 FatherClass的参数
        super().__post_init__()
        if not self.tank_size and self.v:
            self.set_size()

    def set_size(self):
        self.height_width = self.height_width or 1
        self.length_width = self.length_width or 1
        '''计算 v,height,length,width'''
        if self.height:  # 提供高度
            # 如传入H,计算底面积
            self.bottom_area = self.v / self.height
            if self.width:  # 有w 无 length
                self.length = self.bottom_area / self.width
            elif self.length:  # 有L无W
                self.width = self.bottom_area / self.length
            else:  # 都没有，则通过底面积和 W_L比例进行计算
                self.width = (self.bottom_area / self.length_width)**(1/2)
                self.length = self.width * self.length_width
                self.height_width = self.height/self.width  # 重置比例
                self.length_width = self.length/self.width  # 重置比例
        else:  # 未提供高度（用上高度和宽度比例）
            if self.width and self.length:  # 有W有L
                # 通过W计算L
                self.bottom_area = self.width * self.length
                self.length_width = self.length/self.width  # 重置比例
                self.height = self.v/self.bottom_area
            elif self.width and not self.length:
                self.length = self.width * self.length_width
                self.bottom_area = self.length * self.width
                self.height = self.v/self.bottom_area
                self.height_width = self.height/self.width  # 重置比例
            elif self.length and not self.width:  # 有L无W
                self.width = self.length / self.length_width
                self.bottom_area = self.length * self.width
                self.height = self.v/self.bottom_area
                self.height_width = self.height/self.width  # 重置比例
            elif not self.length and not self.width:  # 长宽高都没有，只有v，全部根据比例计算
                self.width = (self.v / self.height_width /
                              self.length_width)**(1/3)
                self.length = self.width * self.length_width
                self.bottom_area = self.length * self.width
                self.height = self.v/self.bottom_area
        self.tank_size = 'H{:.1f}×L{:.1f}×W{:.1f}m'.format(
            self.h_total, self.length, self.width)


'''
Tank： Round 圆形池子(2)
'''


@dataclass
class TankRound(Tank):
    '''圆形池子'''
    catalog: str = '5.2.2'
    form: str = 'round'
    diameter: float = 0  # 底面直径 m
    height_diameter: float = None  # Height / 直径 的比例

    def __post_init__(self):  # 可以接受所有 FatherClass的参数
        super().__post_init__()
        if not self.tank_size and self.v:
            self.set_size()

    def set_size(self):
        self.height_diameter = self.height_diameter or 1.2
        if self.height:  # 有高度
            self.bottom_area = self.v / self.height
            self.diameter = (self.bottom_area/const.PI)**(1/2) * 2
            self.height_diameter = self.height/self.diameter
        elif self.diameter:  # 有直径
            self.bottom_area = (self.diameter/2)**2*const.PI
            self.height = self.v / self.bottom_area
            self.height_diameter = self.height / self.diameter
        else:  # 没有H和D
            self.diameter = (
                4 * self.v / (self.height_diameter*const.PI))**(1/3)
            self.height = self.height_diameter * self.diameter
            self.bottom_area = self.v / self.height
        self.tank_size = 'H{:.1f}×φ{:.1f}m'.format(self.h_total, self.diameter)
