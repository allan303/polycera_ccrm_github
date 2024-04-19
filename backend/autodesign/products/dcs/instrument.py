#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# File    :   instrument.py
# Time    :   2019/01/14 00:10:03
# Author  :   Jack Li
# Contact :   allanth3@163.com


'''
包含各类仪表
**传递时候全部采用基本数据结构：list/tuple/dict，不传入自定义class
4) FlowGauge:流量计
5) PressureGauge: 压力表
6) LiquidGauge：液位计

'''

from dataclasses import dataclass
# app
from autodesign.products.base_product import BaseProductMixin

'''
instrument Mixin 
:: 完成DN和inch的自由转换
'''


@dataclass
class Instrument(BaseProductMixin):
    catalog: str = '3'
    cad_tag: str = ''  # cad_tag 标签
    # 方便起见
    q: float = 0  # 流量要求 --> 计算量程
    p: float = 0  # 压力--> 计算PN
    q_max: float = 0  # 上限
    p_max: float = 0  # p测试上限

    def __post_init__(self):
        # 设置流量
        super().__post_init__()
        if not self.q_max:  # 量程范围，1.5倍实际流量上限
            self.q_max = self.q * 1.5
        if not self.p_max:
            self.p_max = min(self.pn, self.p*1.5)
        self.set_pn()


@dataclass
class FlowGauge(Instrument):
    '''
    流量计
    '''
    catalog: str = '3.1.1'
    # old
    remark: str = ''  # 备注

    def set_spec(self):
        self.spec = f'平均流量{self.q:.0f}m3/h，请选择合适量程'


# @dataclass
# class FlowGaugeRotor(FlowGauge):
#     '''
#     Summary: 转子流量计
#     '''
#     catalog: str = '3.1.1.1'


@dataclass
class FlowGaugeMagnetic(FlowGauge):
    '''电磁流量计'''
    catalog: str = '3.1.1.2'
    description: str = '法兰对夹式'

    def set_spec(self):
        self.spec = f'DN{self.dn},{self.description},一体型'


# @dataclass
# class FlowTransducer(Instrument):
#     '''
#     流量变送器
#     '''
#     catalog: str = '3.1.2'


@dataclass
class PressureGauge(Instrument):
    '''
    压力表
    '''
    catalog: str = '3.2.1'
    p: float = 6

    def set_spec(self):
        self.spec = f'0-{self.p:.0f}bar {self.description}'


# @dataclass
# class PressureGaugeMechanical(PressureGauge):
#     '''
#     Summary:机械式压力表
#     '''
#     catalog: str = '3.2.1.1'
#     description: str = '注油防震,表盘直径60mm'


# @dataclass
# class PressureTransducer(Instrument):
#     '''
#     Summary: 压力传感器
#     '''
#     catalog: str = '3.2.2'
#     description: str = '4-20mA信号输出源,G1/4'

#     def set_spec(self):
#         self.spec = f'0-{self.pn}bar,{self.description}'


# @dataclass
# class PressureSwitchHigh(Instrument):
#     '''
#     高压开关
#     '''
#     catalog: str = '3.2.3.1'
#     cad_tag: str = 'PSH'
#     low: float = 0.2
#     high: float = 7
#     spec: str = ''
#     material: str = 'SS316L'
#     label: str = 'instrument'

#     def set_spec(self):
#         if not self.spec:
#             self.spec = f'膜片弹簧组合,可调范围{self.low}bar~{self.high}bar,带开关量输出'


# @dataclass
# class PressureSwitchLow(Instrument):
#     '''
#     低压开关
#     '''
#     catalog: str = '3.2.3.2'
#     cad_tag: str = 'PSL'
#     low: float = 0.2
#     high: float = 7
#     material: str = 'SS316L'

#     def set_spec(self):
#         self.spec = f'膜片弹簧组合,可调范围{self.low}bar~{self.high}bar,带开关量输出'


@dataclass
class ImpulseLine(Instrument):
    '''
    压力表 引管（到电控箱）
    '''
    catalog: str = '3.2.4'
    brand: str = '进口'
    lenght_m: float = 6  # m
    spec: str = '配套'

    def set_spec(self):
        self.spec = f'pn{self.pn}bar'


# @dataclass
# class LiquidLevelGauge(Instrument):
#     '''
#     液位计
#     '''
#     catalog: str = '3.3.1'
#     spec: str = '电极式液位开关（或超声波液位计）'


# @dataclass
# class LiquidTransducer(Instrument):
#     '''
#     液位变送器
#     '''
#     catalog: str = '3.3.2'
#     material: str = 'SS316L'
#     # spec: str = '接口：G1/4"'


# @dataclass
# class LiquidSwitch(Instrument):
#     '''
#     液位开关
#     '''
#     catalog: str = '3.3.3'
#     cad_tag: str = 'LS'
#     spec: str = '对夹浮球开关'


# @dataclass
# class PHGauge(Instrument):
#     '''
#     PH计
#     '''
#     catalog: str = '3.4.1'
#     name: str = 'PH计'
#     ph_range: str = '0-14'
#     signal: str = '4-20mA'

#     def set_spec(self):
#         self.spec = f'pH{self.ph_range},{self.signal}'


# @dataclass
# class ORPGauge(Instrument):
#     '''
#     ORP计
#     '''
#     catalog: str = '3.5.1'
#     cad_tag: str = 'ORP'
#     signal: str = '4-20mA'

#     def set_spec(self):
#         self.spec = '{}'.format(self.signal)


@dataclass
class TempGauge(Instrument):
    '''
    Summary: 温度计
    '''
    catalog: str = '3.6.1'

    def set_spec(self):
        self.spec = f'量程{self.temp_range}'


# @dataclass
# class TurbidityGauge(Instrument):
#     '''
#     Summary: 浊度仪
#     '''
#     catalog: str = '3.7.1'


@dataclass
class ConductivityGauge(Instrument):
    '''
    电导率仪 三联件
    '''
    catalog: str = '3.8.1'
    cad_tag: str = 'EC'
    brand: str = 'GF'
    ec_range: str = '0 - 100,000 us/cm'
    remark: str = '三联件'

    def __post_init__(self):
        self.spec = f'量程{self.ec_range} {self.remark}'
