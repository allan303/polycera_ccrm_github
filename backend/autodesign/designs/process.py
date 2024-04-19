#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-04-27

'''
与化学药剂有关的工艺：CEB CIP
通用的功能 在此处
'''
from pydantic import BaseModel
from typing import List, Dict
from dataclasses import dataclass, field, InitVar
# app
from jackutils.units import UnitPd, UnitPd, UnitTime
from autodesign.designs.info import Consumer
from autodesign.designs.chem import OptionChemDosing, ChemDosing, ChemConsumer
from .time import TimeDetail


class OptionCleanProcess(BaseModel):
    '''
    Summary: 针对 一个 确定的process 的option
    '''
    name: str = ''
    # temp: float = 25  # 温度
    duration: UnitPd = UnitPd(val=30, unit='second')  # 时间，option传入

    @property
    def duration_s(self) -> float:
        return UnitTime(**self.duration.dict()).get('s')

    class Config:
        orm_mode = True


class OptionOneClean(BaseModel):
    '''
    Summary: CIP/CEB/MC等都可以统一
             new: backwash 也应该统一到此处
    '''
    # 单个ceb中的操作流程
    name: str = ''  # 必须有名称
    temp: float = 25  # 温度
    process_list: List[OptionCleanProcess] = []
    interval: UnitPd = UnitPd(val=1, unit='day')  # 周期
    duration_add: UnitPd = UnitPd(val=5, unit='minutes')  # 每次额外损耗时间
    chem_dosings: List[OptionChemDosing] = []  # 选择的药剂，可以是混合

    @property
    def duration_s(self) -> float:
        '''
        Summary: 耗时
        '''
        return sum([x.duration_s for x in self.process_list])

    @property
    def duration_add_s(self) -> float:
        return UnitTime(**self.duration_add.dict()).get('s')

    @property
    def interval_s(self) -> float:
        return UnitTime(**self.interval.dict()).get('s')

    @property
    def chem_names(self):
        '''
        Summary: 所有用到化学品名称
        '''
        return ','.join([x.name for x in self.chem_dosings])

    class Config:
        orm_mode = True


'''
============================ 以下为 dc ==========================
'''

PROCESS_MAP_CEB = {
    'ceb': '加药反洗',
    'wash': '冲洗',
    'backwash': '反洗',
    'soak': '浸泡',
    'wash+backwash': '冲洗+反洗',
}

PROCESS_MAP_CIP = {
    'soak': '浸泡',
    'circulate': '循环',
    'wash': '冲洗',
    'backwash': '反洗',
    'drain': '排空'
}

PROCESS_MAP_ALL = {
    **PROCESS_MAP_CIP, **PROCESS_MAP_CEB
}


@dataclass
class CleanProcess():
    '''
    Summary: 其中一种工艺
        - ceb,wash,backwash
        - soak 只需要时间一个参数就行
    NOTE: 只计算此process 单次的，不考虑多少组、间隔等系统参数
          同时用于CEB/CIP/MC等 清洗工序，包含多道小工序
        - CEB的水耗计算是连续流
        - CIP的水耗计算为连续流（wash） + 静态（CIPtank尺寸，通常为产水配药）
    '''
    # 来自option
    name: str  # 工艺名称
    duration: UnitTime   # 时间，option传入
    # parent
    ceb_m3ph: InitVar[float] = 0   # ceb 流量
    backwash_m3ph: InitVar[float] = 0   # backwash 流量
    wash_m3ph: InitVar[float] = 0   # wash 流量
    wash_water: str = 'other'  # 冲洗的水源
    # 计算(raw 和 perm 肯定都外排，不考虑回用)
    perm_m3_use: float = 0
    raw_m3_use: float = 0
    other_feed_not_operate: float = 0
    name_cn: str = ''
    one_time: Consumer = field(default_factory=Consumer)

    def __post_init__(self, ceb_m3ph=0, backwash_m3ph=0, wash_m3ph=0):
        self.ceb_m3ph = ceb_m3ph
        self.backwash_m3ph = backwash_m3ph
        self.wash_m3ph = wash_m3ph
        self.name = str(self.name).lower()
        if self.name in PROCESS_MAP_ALL:
            self.name_cn = PROCESS_MAP_ALL.get(self.name)
        else:
            return None
        self.set_unit_uc()
        self.set_by_name()
        self.set_consumer()

    def set_unit_uc(self):
        '''
        Summary: 单位转换为dc
        '''
        self.duration = UnitTime(**self.duration)

    @property
    def duration_s(self):
        return self.duration.get('s')

    def set_by_name(self):
        '''
        Summary: 分工艺段计算
            - 确定name后移除可能导致的干扰参数
        '''
        hour = self.duration.get('h')
        if self.name in ['ceb']:
            self.perm_m3_use = self.ceb_m3ph * hour
        elif self.name in ['backwash']:
            self.perm_m3_use = self.backwash_m3ph * hour
        elif self.name in ['soak', 'circulate', 'drain']:
            ...
        elif self.name in ['wash']:
            if self.wash_water == 'raw':
                self.raw_m3_use = self.wash_m3ph * hour
            elif self.wash_water == 'perm':
                self.perm_m3_use = self.wash_m3ph * hour
            else:
                self.other_feed_not_operate = self.wash_m3ph * hour
        elif self.name in ['wash+backwash', 'backwash+wash']:
            self.perm_m3_use = self.backwash_m3ph * hour
            # self.raw_m3_use = self.wash_m3ph * hour
            if self.wash_water == 'raw':
                self.raw_m3_use = self.wash_m3ph * hour
            elif self.wash_water == 'perm':
                self.perm_m3_use = self.wash_m3ph * hour
            else:
                self.other_feed_not_operate = self.wash_m3ph * hour

    def set_consumer(self):
        '''
        Summary: 此处只计算水耗，在父级计算药剂费用
        #NOTE：CEB不需要考虑水耗，为外部水源
        '''
        self.one_time.perm_m3_use = self.perm_m3_use
        self.one_time.drain_m3_not_operate = self.raw_m3_use + \
            self.perm_m3_use+self.other_feed_not_operate
        if self.wash_water == 'raw':
            self.one_time.raw_m3_use_not_operate = self.wash_m3ph
        self.one_time.other_feed_not_operate = self.other_feed_not_operate

    # def set_description(self):
        # s = self.duration.get('s')
        # if self.name in ['wash']:
        #     self.description = f'{self.name_cn}, {s:.0f}(s), Q={self.wash_m3ph:.1f}m3/h'
        # elif self.name in ['backwash']:
        #     self.description = f'{self.name_cn}, {s:.0f}(s), Q={self.backwash_m3ph:.1f}m3/h'
        # elif self.name in ['soak', 'circulate', 'drain']:
        #     self.description = f'{self.name_cn}, {s:.0f}(s)'
        # elif self.name in ['wash+backwash', 'backwash+washs']:
        #     self.description = f'{self.name_cn}, {s:.0f}(s), Wash={self.wash_m3ph:.1f}m3/h, Backwash={self.backwash_m3ph:.1f}m3/h'
        # elif self.name in ['ceb']:
        #     self.description = f'{self.name_cn}, {s:.0f}(s), Q={self.ceb_m3ph:.1f}m3/h'
    @property
    def description(self):
        s = self.duration.get('s')
        return f'{self.name_cn}, {s:.0f}(s)'

    @property
    def cip_pump_hr(self):
        '''
        Summary: CIP泵运行时间
        '''
        if self.name == 'circulate':
            return self.duration.get('hours')
        return 0

    @property
    def backwash_pump_hr(self):
        '''
        Summary: Backwash泵运行时间
        '''
        if self.name in ['ceb', 'backwash', 'wash+backwash', 'backwash+washs']:
            return self.duration.get('hours')
        return 0

    @property
    def wash_pump_hr(self):
        '''
        Summary: Backwash泵运行时间
        '''
        if self.name in ['wash', 'wash+backwash', 'backwash+washs']:
            return self.duration.get('hours')
        return 0


@dataclass
class OneClean():
    '''
    Summary: 完整的 单个CEB/CIP/MC 的流程，里面可包含不限量的 wash, soak ,backwash,ceb, circulate 等细粒度流程
    '''
    # 来自option
    name: str   # 针对 此 ceb 的option
    temp: float  # 温度
    chem_dosings: List[ChemDosing]  # 化学品,可以是多种
    process_list: List[CleanProcess]   # = field(default_factory=list)
    interval: UnitTime   # = field(default_factory=UnitTime)  # 间隔周期,默认1天
    duration_add: UnitTime   # = 90
    # parent
    wash_water: str
    feed_liter: float   # CIP:代表CIP tank V, CEB: 代表 ceb_m3ph
    time_detail: TimeDetail    # 来自运行时间
    ceb_m3ph: InitVar[float] = 0   # = 50  # ceb流量
    backwash_m3ph: InitVar[float] = 0   # = 100  # 其他option
    wash_m3ph: InitVar[float] = 0  # = 10  # 其他 option
    cip_m3ph: InitVar[float] = 0  # 化学清洗的流量
    # CEB 和 CIP 区别
    chem_consumer_x: float = 0
    # 计算
    process_description: List[str] = field(default_factory=list)
    one_time: Consumer = field(default_factory=Consumer)  # 不考虑组，代表整个系统
    one_day_per_group: Consumer = field(default_factory=Consumer)  # 整个系统 每天消耗
    chem_consumer: List[ChemConsumer] = field(default_factory=list)

    def __post_init__(self,
                      ceb_m3ph: float = 0,
                      backwash_m3ph: float = 0,
                      wash_m3ph: float = 0,
                      cip_m3ph: float = 0):
        # 过程的 ops
        self.ceb_m3ph = ceb_m3ph
        self.backwash_m3ph = backwash_m3ph
        self.wash_m3ph = wash_m3ph
        self.cip_m3ph = cip_m3ph
        if not self.process_list:
            return None
        self.set_name_prefix()
        self.set_unit_uc()
        self.set_process_list()
        self.set_chem_dosings()
        self.set_hours_or_times_per_day()
        self.set_consumer()
        self.set_chem_consumer()

    def set_name_prefix(self, prefix: str = ''):
        '''
        Summary: 设置独特的名称
        '''
        self.name = prefix+self.name  # 增加 prefix 以防 cip和ceb设置相同

    def set_unit_uc(self):
        self.interval = UnitTime(**self.interval)
        self.duration_add = UnitTime(**self.duration_add)

    def set_process_list(self):
        '''
        Summary: 设置 各工艺段
        '''
        ls = []
        for x in self.process_list:  # ops = List[OptionCleanProcess]
            # 名字不含在标准流程中，则跳过
            if not str(x.get('name', None)).lower() in PROCESS_MAP_ALL:
                continue
            p = CleanProcess(
                **x,
                # 增加父组件参数
                wash_water=self.wash_water,
                ceb_m3ph=self.ceb_m3ph,  # ceb 流量
                backwash_m3ph=self.backwash_m3ph,  # backwash 流量
                wash_m3ph=self.wash_m3ph  # wash 流量
            )
            ls.append(p)
        self.process_list = ls
        self.process_description = [
            x.description for x in self.process_list]  # 流程

    def set_chem_dosings(self):
        '''
        Summary: 设置 chem_dosings
        '''
        ls = []
        for x in self.chem_dosings:
            cm = ChemDosing(
                **x,
                feed_liter=self.feed_liter
            )
            ls.append(cm)
        self.chem_dosings = ls

    def set_consumer(self):
        '''
        Summary: 其他信息 便于查看
        NOTE: 不同的CEB配置 其 周期是不同的，比如HCl一天一次，NaClO 2天一次，
        因此在OneCeb层面就要计算每日平均数据
        '''
        for p in self.process_list:
            self.one_time = self.one_time + p.one_time
        self.one_day_per_group = self.one_time * self.time_detail.times_per_day

    @property
    def chem_lpms(self) -> List[tuple]:
        '''
        Summary: 所有加药泵的流量(允许重复)
        '''
        return [{'name': x.name,
                 'raw_wt': f'{x.chem.wt}%',
                 'dosing_wt': f'{x.dosing_wt}%',
                 'raw_lpm': x.chem.lpm} for x in self.chem_dosings]

    @property
    def chem_summary(self):
        '''
        Summary: 化学药剂概述
        '''
        return ' & '.join([x.name_str for x in self.chem_dosings])

    @property
    def description(self):
        '''
        Summary:  这个过程的描述
        '''
        return f'药剂采用：{self.chem_summary}。每{self.interval.val}({self.interval.unit})进行一次'

    @property
    def times_per_day(self):
        return self.time_detail.times_per_day

    @property
    def cip_pump_hr(self):
        '''
        Summary: CIP泵运行时间
        '''
        return sum([x.cip_pump_hr for x in self.process_list])

    @property
    def backwash_pump_hr(self):
        '''
        Summary: Backwash泵运行时间
        '''
        return sum([x.backwash_pump_hr for x in self.process_list])

    @property
    def wash_pump_hr(self):
        '''
        Summary: Wash泵运行时间
        '''
        return sum([x.wash_pump_hr for x in self.process_list])

    @property
    def cip_pump_hpd(self):
        '''
        Summary: CIP泵运行时间
        '''
        return self.cip_pump_hr*self.times_per_day

    @property
    def backwash_pump_hpd(self):
        '''
        Summary: Backwash泵运行时间
        '''
        return self.backwash_pump_hr*self.times_per_day

    @property
    def wash_pump_hpd(self):
        '''
        Summary: Wash泵运行时间
        '''
        return self.wash_pump_hr*self.times_per_day

    def set_hours_or_times_per_day(self):
        '''
        Summary: 此处CIP 和 CEB 计算chem消耗有区别
            - CIP: 仅需要考虑 times_per_day 
            - CEB: 需考虑 times_per_day * 每次CEB注入药剂的时间，换算为 hours
        '''
        ...

    def set_chem_consumer(self):
        '''
        Summary: 此 为 单组 单次， x = times_per_day
        '''
        self.chem_consumer = [x.get_chem_summary(
            place=self.name, chem_consumer_x=self.times_per_day) for x in self.chem_dosings]

    @property
    def chem_types(self) -> list:
        '''
        Summary: 化学药剂种类
        '''
        return list(set([x.name for x in self.chem_dosings]))
