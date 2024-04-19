#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# File    :   PiplineRelates.py
# Time    :   2019/01/14 00:10:12
# Author  :   Jack Li
# Contact :   allanth3@163.com


'''
PiplineRelate：包含与管道密切相关的设备：管道、连接件等
'''
from dataclasses import dataclass

from jackutils.list_tool import find_x
# app
from autodesign.core import const
from autodesign.products.base_product import BaseProductMixin


@dataclass
class Pipe(BaseProductMixin):  # 管道：接受一个Flow
    '''管道'''
    catalog: str = '1.1'
    s: float = 1  # 流速： 压力管道默认2m/s,无压力默认1m/s
    length_m: float = 0  # 长度 m
    dn: int = 0  # 手动可以传入 公称直径
    material: str = 'PVC'  # 材质
    dn_max: float = 0  # DN最大值
    dn_min: float = 0  # DN最小值
    p: float = 0
    q: float = 0
    real_s: float = 0
    spec: str = ''

    def __post_init__(self):
        if not self.s:
            self.s = 1
        super().__post_init__()
        self.set_real_s()

    @property
    def cross_area(self):
        return (self.dn/1000/2)**2 * const.PI  # m2

    def set_dn(self):
        # 设置标准DN
        if not self.dn:
            cross_area = self.q/self.s/3600   # m3/h /(m/s) / (m/h) = m2
            self.dn = (cross_area/const.PI)**(1/2)*2 * 1000  # 精确的直径mm
        super().set_dn()

    def set_real_s(self):
        # 实际流速
        if not self.q:
            self.real_s = self.s
        else:
            if self.dn:
                self.real_s = self.q / self.cross_area / 3600     # m3/h / m2 / 3600

    @property
    def useful_info(self) -> dict:
        return {
            'name': self.name,
            'dn': self.dn,
            's': self.s,
            'real_s': self.real_s,
            'q': self.q,
            'remark': self.remark
        }


@dataclass
class SoftpiplineDtro(Pipe):
    '''
    DTRO 高压软管
    '''
    catalog: str = '1.1.2'
    material: str = 'SS316L'
    brand: str = 'par-LOK'
    length_m: float = 0.9  # mm
    max_p: int = 90  # bar 最大耐压
    diameter: int = 12

    def __post_init__(self, *args, **kwargs):
        super().__post_init__(*args, **kwargs)
        self.spec = f'φ{self.diameter}×{self.lenght}mm高压软管,{self.material},{self.max_p}'


@dataclass
class ReducerPipe(BaseProductMixin):
    '''
    异径管
    可以传入pp1,pp2进行init
    '''
    catalog: str = '1.1.3'
    dn_small: float = 0
    inch_small: str = None
    dn_large: float = 0
    inch_large: str = None
    label: str = 'pipe'

    def __post_init__(self, ):
        self.dn_large = find_x(x=self.dn_large, y_list=const.DN_LIST)
        self.dn_small = find_x(x=self.dn_small, y_list=const.DN_LIST)
        self.inch_small = const.GB9119.get(self.dn_small)
        self.inch_large = const.GB9119.get(self.dn_large)
        if self.standard == 'us':
            self.spec = '{}-{},{}'.format(self.inch_small,
                                          self.inch_large, self.material)
        else:
            self.spec = 'DN{:.0f}-DN{:.0f} {}'.format(self.dn_small,
                                                      self.dn_large,
                                                      self.material)


@dataclass
class BackWashPillar(Pipe):
    '''
    反洗柱 BackWashPillar
    根据需要的V、D/hight 比例计算 得到 D，H
    '''
    catalog: str = '1.1.4'
    material: str = 'UPVC'
    v: float = 0   # 体积作为初始值 m3
    hight: float = 0  # 长度m
    diameter: float = 0  # 直径m
    diameter_height: float = 1/3  # 直径/高度
    duration_s: float = 0  # 放空时间
    remark: str = ''
    dn_max: float = 300

    def __post_init__(self):
        if not self.v:
            if self.duration_s and self.q:
                self.v = self.duration_s/3600 * self.q
            else:
                raise Exception(
                    'Must provided [V] or [duration_s,q] for BackWashPillar')
        # hight = diameter/diameter_height
        # diameter**2 * const.PI / 4 * diameter / diameter_height = v
        self.diameter = (self.v * self.diameter_height *
                         4 / const.PI)**(1/3)
        self.dn = find_x(x=self.diameter*1000, y_list=const.DN_LIST,
                         maximum=self.dn_max, minium=self.dn_min, func=lambda x: x**2)
        self.cross_area = (self.dn/2/1000)**2*const.PI  # 截面积
        self.hight = self.v / self.cross_area
        if not self.spec:
            self.spec = f'V={self.v * 1000:.0f}L,DN{self.dn} {self.material}管道,H={self.hight*1000:.0f}mm'
        if self.q:  # 有流量
            self.duration_s = self.v/self.q*3600
        self.remark = f'不大于DN{self.dn_max}的PVC或SS304管道，根据实际选择高径比'
        super().__post_init__()

    @property
    def real_v(self):
        return (self.dn/2/1000)**2 * const.PI * self.hight


@dataclass
class PiplineRelated(Pipe):
    '''
    管道连接相关的通用特性
    '''

    def set_spec(self):
        if self.standard == 'us':
            self.spec = f'{self.dn_inch},{self.material}'
        else:
            self.spec = f'DN{self.dn},{self.material}'


# @dataclass
# class Flange(PiplineRelated):
#     '''
#     Flange: 法兰
#     '''
#     catalog: str = '1.2.1'
#     unit: str = 'set'
#     material: str = '铸铁'


# @dataclass
# class Elbow(PiplineRelated):
#     '''
#     Elbow：弯头
#     '''
#     catalog: str = '1.2.2'


# @dataclass
# class Coupling(PiplineRelated):
#     '''
#     卡箍/拷贝林 Coupling
#     '''
#     catalog: str = '1.2.3'
#     material: str = '铸铁'
#     dn: int = 0  # dn
#     unit: str = 'pair'


# @dataclass
# class Saddle(PiplineRelated):
#     '''
#     马鞍座 Saddle
#     '''
#     catalog: str = '1.2.4'
#     material: str = '橡胶'

#     def __post_init__(self):
#         super().__post_init__()
#         self.spec = f'支撑DN{self.dn}'


# @dataclass
# class Joint(PiplineRelated):
#     '''
#     接头
#     '''
#     catalog: str = '1.2.5'
#     unit: str = 'pcs'  # 默认单位
