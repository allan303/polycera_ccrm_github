#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-04-24

from dataclasses import dataclass, field
import copy
import numbers


@dataclass
class FlowBalance:
    '''
    Summary: 水量的集合，均为瞬时流量（之后可以根据不同的耗时来计算总量）
    '''
    # 来自外部
    q2: float = 0  # 循环量（已知） cir pump
    q6: float = 0  # 产水量（已知） perm
    q7: float = 0  # 回流量（已知） backflow
    q9: float = 0  # 反洗流量 backwash
    # q10,q11,q12都是直接父组件赋值，为0即代表无
    q10: float = 0  # 反洗回流到原水箱的话，换算成一个制水周期内的平均流量
    q11: float = 0  # 反洗时候的冲洗 backwash wash
    rec: float = 1  # 回收率（已知）
    # 计算
    q0: float = 0  # 原水量 raw
    q1: float = 0  # 原水泵 feed
    q3: float = 0
    q4: float = 0
    q5: float = 0  # 浓水量 conc
    q8: float = 0  # 实际循环回来的量 cir delt

    @property
    def q0_consider_q10(self):
        return self.q0 - self.q10

    def set_balance(self):
        '''
        Summary: 所有水量平衡
            前提是已经获得所有已知条件
                rec = perm/(perm+conc)
                rec*perm + conc*rec = perm
                conc*rec = perm-perm*rec
                conc = perm*(1-rec) / rec
        '''
        self.q5 = self.q6*(1-self.rec)/self.rec
        self.q1 = self.q7+self.q6+self.q5  # 原水泵
        self.q0 = self.q6+self.q5  # 虚拟的原水量（仅仅在运行时）
        if self.q2 <= self.q1:  # 循环量<供水量
            self.q2 = self.q1
            self.q8 = 0
        else:
            self.q8 = self.q2 - self.q1
        self.q4 = self.q7 + self.q8
        self.q3 = self.q2 - self.q6

    @property
    def rec_once(self):
        return self.q6/self.q2

    def __truediv__(self, i: numbers.Real):
        '''
        Summary: 除法
        '''
        if not isinstance(i, numbers.Real) or i <= 0:
            raise ValueError(f'{i} is not a valid float')
        new = copy.deepcopy(self)
        new.q2 /= i
        new.q6 /= i
        new.q7 /= i
        new.q9 /= i
        new.q10 /= i
        new.q11 /= i
        new.set_balance()
        return new

    def __mul__(self, i: float):
        '''
        Summary: 乘法
        '''
        ii = 1/i
        return self/ii


@dataclass
class FlowInfo():
    '''
    Summary: 保存流量分配
    '''
    total: FlowBalance = field(default_factory=FlowBalance)
    serie: FlowBalance = field(default_factory=FlowBalance)
    group: FlowBalance = field(default_factory=FlowBalance)
    train: FlowBalance = field(default_factory=FlowBalance)
