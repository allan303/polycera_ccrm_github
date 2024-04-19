#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2019-12-11
from dataclasses import dataclass


@dataclass
class FlowPipe():
    '''
    Summary: 某个管道内瞬时水流情况
    '''
    name: str = 'flow'
    tab: str = ''
    c: float = 0  # 浓度 mg/L
    m3ph: float = 0  # 水量 m3/h

    @property
    def ts(self):
        return self.c * self.m3ph  # 绝干固体量 mg/L * m3/h = g/h

    @ts.setter
    def ts(self, val: float):
        '''
        Summary: 根据tph 和 ts 设定mg_l
        '''
        self.c = val / self.m3ph

    def __add__(self, other):
        '''合并Flow'''
        if not isinstance(other, FlowPipe):
            raise TypeError('Only allow FlowPipe+FlowPipe')
        new = FlowPipe()
        new.m3ph = self.m3ph + other.m3ph
        new.ts = self.ts + other.ts
        return new

    def __sub__(self, other):
        '''减法'''
        if not isinstance(other, FlowPipe):
            raise TypeError('Only allow FlowPipe - FlowPipe')
        new = FlowPipe()
        new.m3ph = self.m3ph - other.m3ph
        new.ts = self.ts - other.ts
        if new.m3ph <= 0 or new.ts <= 0:
            raise Exception('FlowPipe - FlowPipe 减去值太大')
        return new

    def clone_from(self, other):
        '''从另一个Flow上克隆信息，保留name'''
        self.m3ph = other.m3ph
        self.c = other.c
