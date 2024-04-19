#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2022-03-17

'''
Summary: 细粒度 操作process,除了正常运行的
1) 每一个操作单独原子化,包含冲洗/反洗/药剂循环/停机或浸泡/加药反洗/排空/阀门切换
2) 单个Process获得属性应该是单位时间的WaterConsumer和chemConsumer
3) duration 和 interval 通过一个时间管理的class 完成
'''

from ctypes import Union
import ssl
from enum import Enum
from enum import unique

from prompt_toolkit import PromptSession
from autodesign.designs.chem import ChemConsumer
from autodesign.designs.info import WaterConsumer
from pydantic import BaseModel
from typing import List, Dict
from dataclasses import dataclass, field, InitVar
# app
from jackutils.units import UnitPd, UnitPd, UnitTime


# class OptionBaseProcess(BaseModel):
#     '''
#     Summary: BaseProcess属性,至少有时间配置
#     '''
#     name: str = ''
#     duration: UnitPd = UnitPd(val=30, unit='s')  # 时间,option传入
#     interval: UnitPd = UnitPd(val=1, unit='h')

#     class Config:
#         orm_mode = True
@unique
class WaterType(Enum):
    '''
    Summary: 系统内水类型
    '''
    perm = 'perm'
    feed = 'feed'
    conc = 'conc'
    outside = 'outside'
    chem = 'chem'  # 药剂
    chem_water = 'chem_water'  # 含药剂废水，比如冲洗


@unique
class ProcessName(Enum):
    backwash = 'backwash'
    cir = 'cir'
    wash = 'wash'
    soak = 'soak'
    valve_switch = 'valve_switch'
    ceb = 'ceb'
    drain='drain'


@dataclass
class ProcessMixin():
    '''
    Summary: ProcessMixin属性,与时间无关
    - 最终为了获取water_consumer_per_hour 和 chem_consumer_per_hour
    - 对于单个OneProcess 和 ProcessGroup 都一样的接口
    '''
    name: str = ''
    description: str = ''
    duration_s: float = 30  # 是否共享 看 参数
    m3ph: float = 0  # 反洗流量
    is_drain_out: bool = True  # 是否排空
    water_type: str = WaterType.perm.value
    # 统一
    internal_v: float = 0  # 内部体积
    cip_v: float = 0  # 清洗药剂体积

    @property
    def m3(self):
        return self.m3ph*self.duration_s/3600

    @property
    def water_consumer(self):
        return WaterConsumer()

    @property
    def summary(self):
        return f'{self.name},持续{self.duration_s}s'


@dataclass()
class ProcessBackwash(ProcessMixin):
    name: str = 'backwash'
    description: str = '反洗'
    water_type: str = WaterType.perm.value

    @property
    def water_consumer(self):
        wc = WaterConsumer()
        # 1) 产水使用
        if self.water_type == WaterType.perm.value:
            wc.perm_m3_use = self.m3
        elif self.water_type == WaterType.outside.value:
            # 如采用外来干净水源
            wc.other_feed_not_operate = self.m3
            # 排空与否
        if self.is_drain_out:
            wc.drain_m3_not_operate = self.m3
        else:  # 不排空，则去原水池
            wc.raw_m3_add = self.m3
        return wc


@dataclass()
class ProcessWash(ProcessMixin):
    name: str = 'wash'
    description: str = '冲洗'
    water_type: str = WaterType.feed.value

    @property
    def water_consumer(self):
        wc = WaterConsumer()
        # 1) 产水使用
        if self.water_type == WaterType.perm.value:
            wc.perm_m3_use = self.m3
        elif self.water_type == WaterType.feed.value:
            wc.raw_m3_use_not_operate = self.m3
        elif self.water_type == WaterType.outside.value:
            # 外部水源冲洗
            wc.other_feed_not_operate = self.m3
        # 排空与否
        if self.is_drain_out:
            wc.drain_m3_not_operate = self.m3
        else:  # 不排空，则去原水池
            wc.raw_m3_add = self.m3
        return wc


@dataclass()
class ProcessSoak(ProcessMixin):
    name: str = 'soak'
    description: str = '浸泡'


@dataclass()
class ProcessCir(ProcessMixin):
    name: str = 'cir'
    description: str = '循环'


@dataclass()
class ProcessValveSwitch(ProcessMixin):
    name: str = 'valve_switch'
    description: str = '阀门切换'


@dataclass()
class ProcessDrain(ProcessMixin):
    '''
    Summary: 原水或含药剂废水
    '''
    name: str = 'drain'
    description: str = '排空'
    water_type: str = WaterType.feed.value

    @property
    def water_consumer(self):
        wc = WaterConsumer()
        if self.water_type == WaterType.chem.value:
            wc.drain_m3_not_operate_chem = self.internal_v
        else:
            wc.drain_m3_not_operate = self.internal_v
        return wc


@dataclass()
class ProcessCebInject(ProcessMixin):
    name: str = 'ceb_inject'
    description: str = 'CEB注药'
    water_type: str = WaterType.perm.value  # perm or outside

    @property
    def water_consumer(self):
        wc = WaterConsumer()
        if self.water_type == WaterType.perm.value:
            wc.perm_m3_use = self.m3
        elif self.water_type == WaterType.outside.value:
            wc.other_feed_m3 = self.m3
        # 排放
        if self.m3 > self.internal_v:
            # 如果超过内部容积了，则有排水
            wc.drain_m3_not_operate_chem = self.m3 - self.internal_v
        return wc


@dataclass
class ProcessGroup(ProcessMixin):
    '''
    Summary: 操作组合
    '''
    name: str = ''
    duration_s: float = 30  # 是否共享 看 参数
    is_meanwhile: bool = False  # 如果是同时，则共享duration，如果否，则
    process_list: List[ProcessMixin] = field(default_factory=list)

    def __post_init__(self):
        self.cal()

    def cal(self):
        self.set_duration()

    def set_duration(self):
        '''
        Summary: 要么从上到下同步，要么从下到上sum
        '''
        if self.is_meanwhile:
            for x in self.process_list:
                x.duration_s = self.duration_s
        else:
            self.duration_s = sum([x.duration_s for x in self.process_list])

    def add(self, *args):
        '''
        Summary: 增加一个工序
        '''
        for process in args:
            if isinstance(process, ProcessMixin):
                self.process_list.append(process)
            elif isinstance(process, self.__class__):
                self.process_list + process
        self.cal()

    @property
    def summary_list(self):
        return [x.summary for x in self.process_list]

    @property
    def summary(self):
        return '; '.join(self.summary_list)

    @property
    def water_consumer(self):
        wc = WaterConsumer()
        for x in self.process_list:
            wc += x.water_consumer
