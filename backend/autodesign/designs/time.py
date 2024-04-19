#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-08-09

'''
时间分配计算
'''
from dataclasses import dataclass, field
from typing import List
import copy
# app
from jackutils.units import UnitTime


@dataclass
class Times():
    '''
    Summary: 分别为 秒、分钟、小时
    '''
    total: float = 0  # 全部工作时间
    cip: float = 0  # 单位小时
    ceb: float = 0  # 单位小时
    backwash: float = 0  # 合计时间 （小时/每天）
    wash: float = 0
    operate: float = 0  # 实际运行时间
    total_waste: float = 0  # 总计无效时间

    def __mul__(self, i: float):
        '''
        Summary: 乘法
        '''
        new = copy.copy(self)
        new.total *= i
        new.cip *= i
        new.ceb *= i
        new.backwash *= i
        new.wash *= i
        new.operate *= i
        new.total_waste *= i
        return new

    def __truediv__(self, i: float):
        '''
        Summary: 除法
        '''
        return self * (1/i)


@dataclass
class TimeDetail():
    '''
    Summary: 单个操作时间
    '''
    name: str = ''
    interval: UnitTime = field(default_factory=UnitTime)  # 周期
    duration: UnitTime = field(default_factory=UnitTime)  # 单次时间
    duration_add: UnitTime = field(default_factory=UnitTime)  # 单次 额外时间
    remark: str = ''
    label: str = ''
    times_per_day: float = 0
    waste_seconds_per_day: float = 0
    # 计算
    # 反洗周期 应该是 制水周期+反洗消耗时间，CEB和CIP还是按照模糊计算

    @property
    def duration_all(self) -> UnitTime:
        # 包含 其他消耗的计算
        return self.duration + self.duration_add

    @property
    def backwash_interval(self):
        # 反洗周期 应该是 制水周期+反洗消耗时间，CEB和CIP还是按照模糊计算
        return self.interval+self.duration_all

    def get_times_per_day(self, hpd: float) -> float:
        '''
        Summary: 每日 次数
        '''
        if self.name in ['backwash', 'wash']:
            # 如果是backwash，则采用 制水周期
            return hpd/self.backwash_interval.get('hours')
        # CEB 和 CIP 还是按照模糊计算
        if self.interval.unit in ['day', 'd', '天']:
            # 如果周期 是 以天为单位，最简单
            return 1 / self.interval.val
        else:
            # 如果周期不是天，则要计算 每天的次数
            return hpd / self.interval.get('hours')

    def get_waste_seconds_per_day(self, hpd: float = 24) -> float:
        '''
        Summary: 根据每天实际开机时间，来计算每天需要占用的时间
        '''
        return self.duration_all.get('s') * self.get_times_per_day(hpd=hpd)

    def cal(self, hpd: float):
        '''
        Summary: 赋值
        '''
        self.times_per_day = self.get_times_per_day(hpd=hpd)
        self.waste_seconds_per_day = self.get_waste_seconds_per_day(
            hpd=hpd)


@dataclass
class TimeInfo():
    '''
    Summary: 时间分配
    1）按照优先级 cip -> ceb -> backwash 计算非运行时间耗时
    2）得到运行时间
    NOTE: 此部分计算和水量无关
    '''
    hours: Times = field(default_factory=Times)
    minutes: Times = field(default_factory=Times)
    seconds: Times = field(default_factory=Times)
    time_detail_list: List[TimeDetail] = field(default_factory=list)

    def cal_waste_time(self):
        # 通过 time_detail_list 计算所有信息
        ls = self.time_detail_list  # 没有地方浪费
        # 以下顺序为优先级，hpd 要逐步减去以下占用时间
        self.seconds.cip = sum(
            [x.waste_seconds_per_day for x in ls if x.label == 'cip'])
        self.seconds.ceb = sum(
            [x.waste_seconds_per_day for x in ls if x.label == 'ceb'])
        self.seconds.backwash = sum([
            x.waste_seconds_per_day for x in ls if x.label == 'backwash'])
        self.seconds.wash = sum(
            [x.waste_seconds_per_day for x in ls if x.label == 'wash'])
        self.seconds.total_waste = sum(
            [x.waste_seconds_per_day for x in self.time_detail_list])
        self.seconds.operate = self.seconds.total - self.seconds.total_waste
        self.minutes = self.seconds / 60
        self.hours = self.minutes / 60
