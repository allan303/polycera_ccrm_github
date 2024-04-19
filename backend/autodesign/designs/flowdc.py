#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-03-18

'''
基础FLow 类
'''
from collections.abc import Mapping
from dataclasses import dataclass, field
from jackutils.units import UnitFlow, UnitPressure
from jackutils.mycounter import MyCounter
import copy
import numbers


@dataclass
class FlowDc():
    '''
    Summary: Flow实例
    Note ： 为了减少类的层级，尽量扁平化
    '''
    name: str = 'flow'
    wwtype: str = '地表水'
    ph: float = 7
    q: float = 0  # feed_q
    q_unit: str = 'm3/h'
    hpd: float = 24  # 系统的运行时间，单个产品的运行时间各异
    p: float = 0  # 压力
    p_unit: str = 'bar'  # 压力单位
    temp: float = 25  # 作为基础参数
    density_kg_l: float = 1  # 密度，用于换算 ppm
    concs_dt: dict = field(default_factory=dict)  # 不带单位
    remark: str = ''  # 可以注明
    water_solution: str = 'nacl'

    def __post_init__(self):
        # 前台传来可能是非数字
        
        for k, v in self.concs_dt.items():
            try:
                self.concs_dt[k] = float(v)
            except:
                continue

    @property
    def flow_uc(self):
        # 单位换算类
        return UnitFlow(val=self.q, unit=self.q_unit)

    @property
    def m3ph(self):
        if self.q_unit in ['m3/h', 'm3ph', '立方米/小时']:
            return self.q
        if self.q_unit in ['m3/d', 'm3pd', '立方米/天', '立方米/日']:
            return self.q/self.hpd

    @m3ph.setter
    def m3ph(self, val):
        if val < 0:
            raise ValueError('tph必须>0')
        self.q = val
        self.q_unit = 'm3/h'

    @property
    def m3pd(self):
        return self.m3ph * self.hpd

    @m3pd.setter
    def m3pd(self, val):
        if val < 0:
            raise ValueError('tpd必须>0')
        self.q = val
        self.q_unit = 'm3/d'

    @property
    def pressure_uc(self):
        # 压力class
        return UnitPressure(val=self.p, unit=self.p_unit)

    @property
    def bar(self):
        return self.pressure_uc.get('bar')

    @bar.setter
    def bar(self, val: numbers.Real):
        if not val > 0:
            raise ValueError(f'Flow Bar 设置必须>0, 当前{val}')
        self.p = val
        self.p_unit = 'bar'

    def __add__(self, other):
        '''
        Summary: 加法  flowdc + flowdc
        Note   : pressure没有逻辑相关性
        Return : new FlowDc
        '''
        if other is None:
            new = copy.deepcopy(self)
            new.name = new.name + '(clone)'
            return new
        if not isinstance(other, FlowDc):
            raise TypeError(f'{str(type(other))} can not + with FlowDc')
        if not self.hpd == other.hpd:
            raise TypeError(f'hpd is not same, can not + with FlowDc')
        new = FlowDc(hpd=self.hpd,
                     q_unit='m3/h',
                     p_unit='bar',
                     name=f'{self.name}+{other.name}'
                     )
        q1, q2 = self.m3ph, other.m3ph
        q3 = q1+q2
        # 合并压力
        p1, p2 = self.bar, other.bar
        p3 = (p1 * q1 + p2 * q2)/q3
        # 合并温度
        t1, t2 = self.temp, other.temp
        t3 = (t1*q1 + t2*q2)/q3
        # 合并浓度
        d1, d2 = self.concs_counter, other.concs_counter
        d3 = (q1 * d1 + q2 * d2)/q3  # MyCounter
        # 合并密度
        s1, s2 = self.density_kg_l, other.density_kg_l
        s3 = (s1 * q1 + s2 * q2)/q3
        # 赋值
        new.q = q3  # 单位已经设为m3/h
        new.p = p3  # 单位已经设为bar
        new.temp = t3
        new.density_kg_l = s3
        new.concs_counter = d3
        return new

    def __sub__(self, other):
        '''
        Summary: 减法  flowdc - flowdc
        Note   : pressure没有逻辑相关性
        Return : new FlowDc
        NOTE   : 尽量不用
        '''
        if not isinstance(other, FlowDc):
            raise TypeError(f'{str(type(other))} can not + with FlowDc')
        if not self.hpd == other.hpd:
            raise TypeError(f'hpd is not same, can not + with FlowDc')
        new = FlowDc(hpd=self.hpd,
                     q_unit='m3/h',
                     p_unit='bar',
                     name=f'{self.name}-{other.name}'
                     )
        q1, q2 = self.m3ph, other.m3ph
        q3 = q1-q2
        if q1 <= q2:
            raise Exception(f'Flow({q1}) - Flow({q2}) (q1<=q2)')
        # 压力
        p1, p2 = self.bar, other.bar
        p3 = (q1*p1 - q2*p2)/q3
        # 浓度
        d1, d2 = self.concs_counter, other.concs_counter
        d3 = (q1 * d1 - q2 * d2)/q3
        # 温度
        t1, t2 = self.temp, other.temp
        t3 = (q1*t1 - q2*t2)/q3
        # 密度
        s1, s2 = self.density_kg_l, other.density_kg_l
        s3 = (s1 * q1 - s2 * q2)/q3
        new.q = q3
        new.p = p3
        new.temp = t3
        new.density_kg_l = s3
        new.concs_counter = d3
        return new

    def clone_from(self, other):
        '''从另一个Flow上克隆信息，保留name'''
        if not isinstance(other, FlowDc):
            raise TypeError(f'{str(type(other))} can not use [clone_from]')
        name = self.name
        self = copy.deepcopy(other)
        self.name = name

    def __truediv__(self, i: float):
        '''
        Summary: 除法，直接作用于q
        '''
        self.q /= i

    def __mul__(self, i: float):
        '''
        Summary: 乘法，直接作用于q
        '''
        self.q *= i

    @property
    def tonph(self):
        '''
        Summary: m3ph(其实应该是m3/h) 换算为 ton/h
        '''
        return self.m3ph * self.density_kg_l

    @property
    def concs_counter(self) -> MyCounter:
        return MyCounter(self.concs_dt)

    @concs_counter.setter
    def concs_counter(self, data: Mapping):
        self.concs_dt = dict(data)


def get_flows_after_seperate(flow: FlowDc, rej_dt: dict = None, rec: float = 1):
    '''
    根据一个rejdt处理flowDc的去除率
    如果没有提供则为没有去除率(0%)
        - rej_dt = {'oil':0.9,'tds':0.8} 类似
        - rec : 回收率
    '''
    rec = rec or 1
    if rec > 1:
        raise ValueError(f'rec不能大于1')
    raw = copy.copy(flow)
    concs_counter = copy.deepcopy(raw.concs_counter)  # 新的浓度
    rej_dt = rej_dt or {}  # 初始化
    for x in concs_counter:
        if not x in rej_dt:
            continue  # 认为rej=0%
        if rej_dt[x] > 1:
            raise ValueError(f'Reject rate must <= 1')
        else:
            concs_counter[x] = concs_counter[x] * (1-rej_dt[x])
    perm = copy.copy(flow)
    perm.name = 'perm'
    perm.concs_counter = copy.deepcopy(concs_counter)  # 浓度变化
    if rec == 1:  # 回收率=1
        conc = None  # 浓水为空
    else:
        perm.q *= rec
        conc = raw - perm
        conc.name = 'conc'
    return {'perm': perm, 'conc': conc}
