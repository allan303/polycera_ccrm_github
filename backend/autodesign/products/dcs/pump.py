#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-03-06


'''
PowerEquipment:包含各类动力设备：水泵、搅拌机等
**传递时候全部采用基本数据结构：list/tuple/dict，不传入自定义class
1）Agitator:搅拌机
3）Pump:水泵
'''
from dataclasses import dataclass
# app
from jackutils.list_tool import find_x
from autodesign.core import const
from autodesign.products.base_product import BaseProductMixin
from jackutils.units import UnitFlow, UnitPressure

'''
通常只用考虑 初始化时候的计算
因此可以考虑直接初始化缓存
'''


@dataclass
class Pump(BaseProductMixin):
    '''泵'''
    # 以下为数据库固定参数
    catalog: str = '4'
    description: str = ''
    unit: str = 'set'
    spec: str = ''
    pn: int = 0  # 公称压力
    material: str = ''
    # 以下为电动工具
    kw: float = 0
    kw_install: float = 0  # 装机
    kw_k: float = 0.8  # 泵效率
    ##########
    density_kg_l: float = 1  # 液体密度
    p1: float = 0  # 轴功率
    p2_k: float = 1.2
    p2: float = 0  # 实际电机功率
    p_inlet_min: float = 0  # 泵入口压力要求  bar
    q_inlet_min: float = 0  # 泵入口流量要求  m3/h
    p_inlet_max: float = 0  # 泵入口最大压力  bar
    q_inlet_max: float = 0  # 泵入口最大流量  m3/h
    p_inlet: float = 0  # 泵入口最大压力  bar
    q_inlet: float = 0  # 泵入口最大流量  m3/h
    p: float = 0  # 额定扬程，运行压力
    p_max: float = 0  # 装机推荐
    q: float = 0  # 额定流量 m3/h
    q_max: float = 0
    hz: float = 50  # 赫兹
    use_vfd: bool = False  # 采用变频

    @property
    def pressure_uc(self):
        return UnitPressure(self.p, 'bar')

    @property
    def flow_uc(self):
        return UnitFlow(self.q, 'm3/h')

    def set_spec(self):
        '''
        Summary: 设定规格
        '''
        height = self.p_max * 10
        if self.kw and self.power == 'electric':
            self.spec = f'Q={self.q_str},H={height:.0f}m,{self.kw_install}kw'
        else:
            self.spec = f'Q={self.q_str},H={height:.0f}m'
        if self.use_vfd:
            self.spec = self.spec + ',变频'

    @property
    def kw_water(self):
        # 根据要输送的物料 计算理论消耗做功,单位kw
        return self.density_kg_l * self.q / 3600 * self.p * 10 * 9.81

    @property
    def kw_water_install(self):
        # 根据要输送的物料 计算理论消耗做功,单位kw
        return self.density_kg_l * self.q_max / 3600 * self.p_max * 10 * 9.81

    @property
    def q_str(self):
        # 显示的q
        if self.q < 0.1:
            return f'{self.q_max * 1000:.1f}L/h'
        else:
            return f'{self.q_max:.1f}m3/h'

    def set_kw(self):
        '''
        Summary: 此处为离心泵
        p1 = ρQgH/η  密度*m3ph*head*9.81/kw_k
        '''
        if not self.q_max:
            self.q_max = self.q
        if not self.p_max:
            self.p_max = self.p
        if self.kw or not self.power == 'electric':
            return None
        # 轴功率 (/3600)
        self.p1 = self.kw_water / self.kw_k
        # 实际功率 (实际电机功率P2=γP1，γ表示电机的安全余量(γ的取值范围1.1—1.3，一般选1.2))
        self.p2 = self.p1 * self.p2_k
        self.kw = self.p2
        # 电机功率选择
        # self.kw = find_x(x=self.p2,
        #                  y_list=const.KW_LIST)  # 选择更靠近的

    def set_kw_install(self):
        if not self.use_vfd:
            super().set_kw_install()
            return None
        self.kw_install = find_x(x=(self.kw_water_install / self.kw_k*self.p2_k),
                                 y_list=const.KW_LIST)


@dataclass
class CentrifugalPump(Pump):
    '''离心泵'''
    catalog: str = '4.1'


@dataclass
class PistonPump(Pump):
    '''柱塞泵'''
    catalog: str = '4.2'
    kw_k: float = 0.8
    p2_k: float = 1  # 提供的公式似乎直接考虑了效率

    def set_kw(self):  # 柱塞泵功率计算
        self.p1 = self.flow_uc.gpm * self.pressure_uc.psi/1460/self.kw_k  # 碟滤提供
        # p2 = self.flo：w_uc.lpm * self.pressure_uc.mpa / 60/self.kw_k
        # print('网络P2', p2*1.1)
        self.p2 = self.p1 * self.p2_k
        self.kw = self.p2
        # self.kw = find_x(x=self.p2,
        #                  y_list=const.KW_LIST)



@dataclass
class ScrewPump(Pump):
    '''螺杆泵'''
    catalog: str = '4.3'
    kw_k: float = 0.4
    nc: float = 0  # Nc =P*Q / 1000 , Pa * m3/s / 1000
    nf: float = 2  # Nf = K * n * 1.5 * diameter**2 * viscosity * m
    p2_k: float = 1.2

    def set_kw(self):
        # self.p1 = self.q/3600*self.p*1000000*1.5/1000/self.kw_k
        # Nc =P*Q / 1000 , Pa * m3/s / 1000
        self.nc = self.flow_uc.get('m3/s')*self.pressure_uc.get('pa')/1000
        # Nf = K * n * 1.5 * diameter**2 * viscosity * m
        self.nf = 1.7
        self.p1 = self.nc * self.nf / self.kw_k
        self.p2 = self.p1 * self.p2_k
        self.kw = self.p2

    def set_kw_install(self):
        if not self.use_vfd:
            super().set_kw_install()
            return None
        # self.p1 = self.q/3600*self.p*1000000*1.5/1000/self.kw_k
        # Nc =P*Q / 1000 , Pa * m3/s / 1000
        self.nc = self.flow_uc.get('m3/s')*self.pressure_uc.get('pa')/1000 / \
            self.kw_k/self.q*self.q_max/self.p*self.p_max
        # Nf = K * n * 1.5 * diameter**2 * viscosity * m
        self.nf = 1.7
        self.p1 = self.nc * self.nf / self.kw_k
        self.p2 = self.p1 * self.p2_k
        self.kw_install = find_x(x=self.p2,  # 帕*m3/s / 1000
                                 y_list=const.KW_LIST)


@dataclass
class DiaphragmPump(Pump):
    '''隔膜泵'''
    catalog: str = '4.4'
    kw_k: float = 0.5

    def set_kw(self):
        self.p1 = self.p * self.flow_uc.get('l/h') / 36000 / self.kw_k
        self.p2 = self.p1 * self.p2_k
        self.kw = self.p2




@dataclass
class DiaphragmMeteringPump(DiaphragmPump):
    '''隔膜计量泵'''
    catalog: str = '4.4.1'

    def set_spec(self):
        '''
        Summary: 设定规格
        '''
        height = self.p_max * 10
        self.spec = f'Q={self.q_max*1000/60:.1f}LPM,H={height:.0f}m'
        if self.use_vfd:
            self.spec = self.spec + ',变频'


# @dataclass
# class GasDiaphragmPump(DiaphragmPump):
#     '''气动隔膜泵'''
#     catalog: str = '4.4.2'
#     material: str = 'PP或氟塑料/GFRPP'
#     remark: str = 'PP气动隔膜泵(或耐酸碱卧式离心泵)'
#     p: float = 2.5


@dataclass
class BoostPump(Pump):
    '''增压泵'''
    catalog: str = '4.5'
    p: float = 8  # 增压
    # kw: float = 7.5  # 功率
    kw_k: float = 0.8


@dataclass
class BarrelPump(Pump):
    '''桶泵'''
    catalog: str = '4.6'
    q: float = 3
    p: float = 0.5
    kw: float = 0.37
    kw_k: float = 0.3
    p2_k: float = 2
