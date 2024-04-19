#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-04-20

'''
CEB 计算逻辑，整合为class
'''
from dataclasses import dataclass, field
from pydantic import BaseModel
from typing import List, Dict
# app
from autodesign.designs.chem import ChemDosing, OptionChemDosing, ChemConsumer
from jackutils.units import UnitPd
from autodesign.designs.process import (
    OptionCleanProcess,
    OptionOneClean,
    OneClean  # 替换OneCeb
)
from .time import TimeDetail
from autodesign.designs.info import Consumer


'''
OPTIONS
NOTE: 简化 针对全部系统，不考虑设备，只计算工艺
'''


class OptionCeb(BaseModel):
    '''
    Summary: 最终的ceb option
        - 配置的数量与 反洗单元关联，主要是增加加药箱和加药泵
    '''
    is_use: bool = False  # 整体是否采用
    lmh: float = 50  # ceb 通量
    oneclean_list: List[OptionOneClean] = []
    use_ceb_pump: bool = False  # 是否采用独立的CEB泵

    class Config:
        orm_mode = True


'''
==================================默认option====================
'''
ceb_acid_option = OptionOneClean(
    name='酸',
    interval=UnitPd(val=2, unit='day'),  # 间隔周期,默认1天
    # 配置药剂
    chem_dosings=[
        OptionChemDosing(
            name='hcl',
            chem_wt=37,
            dosing_wt=0.4,
            solid_price_per_kg=0,
        )
    ],
    process_list=[
        # 反洗30s
        OptionCleanProcess(name='backwash',
                           duration=UnitPd(val=30, unit='second')),
        # 加药60s
        OptionCleanProcess(name='ceb',
                           duration=UnitPd(val=60, unit='second')),
        # 浸泡 5分钟
        OptionCleanProcess(name='soak',
                           duration=UnitPd(val=5, unit='minutes')),
        # 反洗60s
        OptionCleanProcess(name='backwash',
                           duration=UnitPd(val=30, unit='second')),
        # 反洗+冲洗 30
        OptionCleanProcess(name='wash+backwash',
                           duration=UnitPd(val=30, unit='second'))
    ]
)
ceb_alka_option = OptionOneClean(
    name='碱+氧化剂',
    interval=UnitPd(val=1, unit='day'),  # 间隔周期,默认1天
    # 配置药剂
    chem_dosings=[
        OptionChemDosing(
            name='naoh',
            chem_wt=30,
            dosing_wt=0.4,
            solid_price_per_kg=0,
        ),
        OptionChemDosing(
            name='naclo',
            chem_wt=5,
            dosing_wt=0.01,
            solid_price_per_kg=0,
        )
    ],
    process_list=[
        # 反洗30s
        OptionCleanProcess(name='backwash',
                           duration=UnitPd(val=30, unit='second')),
        # 加药60s
        OptionCleanProcess(name='ceb',
                           duration=UnitPd(val=60, unit='second')),
        # 浸泡 5分钟
        OptionCleanProcess(name='soak',
                           duration=UnitPd(val=30, unit='minutes')),
        # 反洗60s
        OptionCleanProcess(name='backwash',
                           duration=UnitPd(val=30, unit='second')),
        # 反洗+冲洗 30
        OptionCleanProcess(name='wash+backwash',
                           duration=UnitPd(val=30, unit='second'))
    ]

)


default_ceb_option = OptionCeb(
    is_use=True,
    lmh=50,
    oneclean_list=[
        # CEB1 酸洗
        ceb_acid_option,
        # CEB2 NaClO + NaOH一起
        ceb_alka_option
    ]
)

'''
=====================以下为 dc ====================
'''


@dataclass
class OneCeb(OneClean):
    '''
    Summary: 完整的 ceb 的流程，里面可包含不限量的 wash, soak ,backwash,dosing等细粒度流程
    '''

    def set_name_prefix(self, prefix: str = 'CEB-'):
        '''
        Summary: 设置独特的名称
        '''
        self.name = prefix+self.name  # 增加 prefix 以防 cip和ceb设置相同

    def set_hours_or_times_per_day(self):
        '''
        Summary: 计算 ceb 注药的总时间 ，times_per_day * process[ceb][hour]
        '''
        ceb_hour_per_time = 0
        for x in self.process_list:
            if x.name == 'ceb':
                ceb_hour_per_time += x.duration.get('hours')
        self.chem_consumer_x = ceb_hour_per_time * self.times_per_day


@dataclass
class Ceb():
    '''
    Summary: 用于项目的 dc 
        - 包含1个或多个ceb配置
        - 包含ceb系统的总体配置
            - is_use / group_num_max 等
        - 多个独立的ceb的配置 [
            {'name':'CEB1','process_list':{...}},
            {'name':'CEB2','process_list':{...}},
            ]
    '''
    # 来自option
    is_use: bool  # = False  # 来自Option
    use_ceb_pump: bool  # = False  # 来自Option
    oneclean_list: List[dict]  # = field(default_factory=list),会直接转换为dc
    lmh: float  # = 50  # 来自main_process
    # parent
    wash_water: str
    backwash_m3ph: float  # 反洗通量
    train_nums_per_group_s1: int  # 1段膜壳数量
    wash_m3ph_per_train: float
    fa: float  # 系统面积
    time_detail_list: List[TimeDetail]  # 包含多个CEB的综合信息
    group_nums: int
    backwash_vfd: bool  # 反洗泵是否有变频
    backwash_lmh: bool  # 反洗通量，ceb通量<=反洗通量
    # 以下为计算
    wash_m3ph: float = 0
    ceb_m3ph: float = 0
    one_day_per_group: Consumer = field(default_factory=Consumer)  # 整个系统 每天消耗
    one_day_total: Consumer = field(default_factory=Consumer)  # 整个系统
    chem_consumer: List[ChemConsumer] = field(default_factory=list)

    def __post_init__(self):
        if not self.is_use:
            return None
        if not self.oneclean_list:  # 没有option
            self.is_use = False
            return None
        if not self.backwash_vfd and not self.use_ceb_pump:
            # 反洗泵无变频 + 不采用独立CEB泵
            self.lmh = self.backwash_lmh
        else:
            self.lmh = min(self.lmh, self.backwash_lmh)
        # self.check_name_duplicate()  # ceb名称查重
        self.ceb_m3ph = self.lmh * self.fa / 1000  # ceb流量
        self.wash_m3ph = self.train_nums_per_group_s1 * self.wash_m3ph_per_train
        self.set_oneclean_list()
        self.set_consumer()
        self.set_chem_consumer()

    def set_oneclean_list(self):
        '''
        Summary: 设置ceb s
        '''
        ls = []
        for op in self.oneclean_list:
            td = [x for x in self.time_detail_list
                  if x.name == op.get('name') and x.label == 'ceb']
            if not td:
                raise Exception(f'CEB {op.get("name")} 无time_detail')
            oneceb = OneCeb(
                wash_water=self.wash_water,
                ceb_m3ph=self.ceb_m3ph,  # = 50  # ceb流量
                backwash_m3ph=self.backwash_m3ph,  # = 100  # 其他option
                wash_m3ph=self.wash_m3ph,  # = 10  # 其他 option
                feed_liter=self.ceb_m3ph*1000,
                time_detail=td[0],  # 来自运行时间
                **op
            )
            ls.append(oneceb)
        self.oneclean_list = ls

    @property
    def chem_dosings(self) -> List[ChemDosing]:
        if not self.is_use:
            return []
        ls = []
        for x in self.oneclean_list:
            ls += x.chem_dosings
        return ls

    @property
    def chem_dosings_info(self):
        # 几种不同加药的 集合
        if not self.is_use:
            return []
        return [{'name': x.chem.name_cn,
                 'wt': x.chem.wt,
                 'lmp': x.chem.lpm,
                 } for x in self.chem_dosings]

    @property
    def chem_lpms(self) -> List[tuple]:
        # 药剂名称:药剂lpm
        return [x.chem_lpms for x in self.oneclean_list]

    def set_consumer(self):
        '''
        Summary: 根据已经得到的数据，把常用的参数 设置到 instance上
        NOTE: 因为不同ceb周期可能不同，因此计算 两个ceb单次合计是没有意义的
        '''
        for x in self.oneclean_list:
            self.one_day_per_group = self.one_day_per_group + x.one_day_per_group
        self.one_day_total = self.one_day_per_group * self.group_nums

    @property
    def cip_pump_hpd(self):
        '''
        Summary: CIP泵运行时间
        '''
        return sum([x.cip_pump_hpd for x in self.oneclean_list])

    @property
    def backwash_pump_hpd(self):
        '''
        Summary: Backwash泵运行时间
        '''
        return sum([x.backwash_pump_hpd for x in self.oneclean_list])

    @property
    def wash_pump_hpd(self):
        '''
        Summary: Wash泵运行时间
        '''
        return sum([x.wash_pump_hpd for x in self.oneclean_list])

    def set_chem_consumer(self):
        '''
        Summary:  从单组单次 转换为 单组*group_nums*times_per_day
        '''
        for x in self.oneclean_list:
            ls = [cc*self.group_nums for cc in x.chem_consumer]
            self.chem_consumer += ls

    @property
    def ceb_pump_summary(self):
        '''
        Summary: CEB泵的说明
        '''
        if not self.use_ceb_pump:
            return '复用反洗泵'
        else:
            return '设置独立CEB泵'

    @property
    def chem_types(self) -> list:
        '''
        Summary: 化学药剂种类
        '''
        return list(set([x.name for x in self.chem_dosings]))

    @property
    def chem_dosings_nums(self):
        return len(self.chem_dosings)
