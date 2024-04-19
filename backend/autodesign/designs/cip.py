#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-04-27

'''
CIP
    - CIP和CEB类似但不同
    - 可能需要一定的冲刷流量，因此确定泵流量可以采用tph_per_train
    - CIP药箱数量手动设置
    - CIP药箱大小可以通过流量和循环时间确定（比如2min）
    - 不同药剂进行不同CIP配置(OneCip)
    - 配药可以考虑人工或者管道自动配药（确定CIP）
'''

from dataclasses import dataclass, field
from pydantic import BaseModel
from typing import List, Dict
# app
from autodesign.designs.chem import OptionChemDosing, ChemConsumer, ChemDosing
from jackutils.units import UnitPd, UnitPd
from .time import TimeDetail
from autodesign.designs.info import Consumer
from .process import OptionCleanProcess, OptionOneClean, OneClean

'''
Summary: CIP水箱尺寸计算 = Max(管道腔体内体积，按照CIP m3/h * HRT)
    - 8'膜 ： 20L/支
    - 4'膜 :  7L/支
'''


class OptionCip(BaseModel):
    '''
    Summary:  cip (需要明确 CIP泵取值逻辑)
    NOTE:
    CIP水箱的大小有2个思路逻辑：
        -1）根据需要充满整个管道系统的体积，在进行放大
        -2）根据需要的流速/流量，再设定循环时间来确定

        方法1）比较准确，但是难以准确计算
        方法2）比较粗糙，但是易于理解，此处采用方法1）
    '''
    is_use: bool = False
    cip_nums: int = 1
    oneclean_list: List[OptionOneClean] = []
    m3ph_per_train: float = 0  # 每列cip流量

    class Config:
        orm_mode = True


default_onecip_option1 = OptionOneClean(
    # 流程
    name='柠檬酸',
    process_list=[
        OptionCleanProcess(  # 冲洗30秒
            name='drain',
            duration=UnitPd(val=5, unit='minutes')
        ),
        OptionCleanProcess(  # 循环30分钟
            name='circulate',
            duration=UnitPd(val=30, unit='minutes')
        ),
        OptionCleanProcess(  # 浸泡2小时
            name='soak',
            duration=UnitPd(val=2, unit='hours')
        ),
        OptionCleanProcess(  # 循环30分钟
            name='circulate',
            duration=UnitPd(val=30, unit='minutes')
        ),
        OptionCleanProcess(  # 排空5分钟
            name='drain',
            duration=UnitPd(val=5, unit='minutes')
        ),
        OptionCleanProcess(  # 冲洗120s
            name='wash',
            duration=UnitPd(val=10, unit='minutes')
        ),
    ],
    interval=UnitPd(val=30, unit='day'),  # 默认30天一次
    duration_add=UnitPd(val=10, unit='minutes'),  # 多20分钟
    chem_dosings=[
        OptionChemDosing(
            name='citric',
            chem_wt=100,
            dosing_wt=1.5,
            solid_price_per_kg=0  # 默认数据库中的价格
        )
    ]  # 化学品配置
)

default_onecip_option2 = OptionOneClean(
    # 流程
    name='碱+氧化剂',
    process_list=[
        OptionCleanProcess(  # 冲洗30秒
            name='drain',
            duration=UnitPd(val=5, unit='minutes')
        ),
        OptionCleanProcess(  # 循环30分钟
            name='circulate',
            duration=UnitPd(val=30, unit='minutes')
        ),
        OptionCleanProcess(  # 浸泡2小时
            name='soak',
            duration=UnitPd(val=2, unit='hours')
        ),
        OptionCleanProcess(  # 循环30分钟
            name='circulate',
            duration=UnitPd(val=30, unit='minutes')
        ),
        OptionCleanProcess(  # 排空5分钟
            name='drain',
            duration=UnitPd(val=5, unit='minutes')
        ),
        OptionCleanProcess(  # 冲洗120s
            name='wash',
            duration=UnitPd(val=10, unit='minutes')
        ),
    ],
    interval=UnitPd(val=30, unit='day'),  # 默认30天一次
    duration_add=UnitPd(val=20, unit='minutes'),  # 多20分钟
    chem_dosings=[
        OptionChemDosing(
            name='naoh',
            chem_wt=20,
            dosing_wt=0.4,
            solid_price_per_kg=0  # 默认数据库中的价格
        ),
        OptionChemDosing(
            name='naclo',
            chem_wt=5,
            dosing_wt=0.01,  # 100ppm
            solid_price_per_kg=0  # 默认数据库中的价格
        )
    ]  # 化学品配置
)


default_cip_option = OptionCip(
    is_use=True,
    cip_nums=1,
    oneclean_list=[
        default_onecip_option1,
        default_onecip_option2
    ],
    m3ph_per_train=10,  # 每列流量
)

'''
=========================== 以下 dc ============================
'''


@dataclass
class OneCip(OneClean):
    '''
    Summary: CIP和ceb不同，只需要确定单次cip的raw chem需求量，但是对于duration没有要求
        - 根据cip m3ph 和 循环时间，计算cip tank 的V
        - 根据v 得到dosing_m3
        - 将dosing_m3 和dosing_wt ,chem_wt 传入 ChemDosing 计算获得 raw_m3
        - 可以配置混合药剂
        - 实际cip时间通过process_list 获得
    '''

    def set_name_prefix(self, prefix: str = 'CIP-'):
        '''
        Summary: 设置独特的名称
        '''
        self.name = prefix+self.name  # 增加 prefix 以防 cip和ceb设置相同

    def set_hours_or_times_per_day(self):
        '''
        Summary: 计算 CIP 药剂消耗，仅仅需要考虑times_per_day
        '''
        self.chem_consumer_x = self.times_per_day


@dataclass
class Cip():
    '''
    Summary: 总体cip计算
    NOTE: CIP默认采用外来水源进行操作，不考虑原水和产水损耗，只考虑药剂费用
    '''
    # 来自option
    is_use: bool  # = True
    oneclean_list: List[OptionOneClean]  # = field(default_factory=list)
    m3ph_per_train: float  # = 0
    # 来自系统
    wash_water: str
    train_nums_per_group_s1: int   # 来自系统（operate)
    group_nums: int
    cip_nums: int  # 设置几套 CIP系统
    wash_m3ph_per_train: float   # 每次 cip 对应多组（通常为1组）的冲洗流量
    time_detail_list: List[TimeDetail]  # 包含多个CIP的综合信息
    liter_inside_per_group: float  # 膜和腔体内的体积，如8040按照 20L每只*1.5（管道富余）
    # 计算
    wash_m3ph: float = 0
    cip_m3ph: float = 0  # 循环泵流量
    one_day_per_group: Consumer = field(default_factory=Consumer)  # 整个系统 每天消耗
    one_day_total: Consumer = field(default_factory=Consumer)  # 整个系统
    chem_consumer: List[ChemConsumer] = field(default_factory=list)

    def __post_init__(self):
        if not self.is_use:
            return None
        self.set_m3phs()
        self.set_oneclean_list()
        self.set_consumer()
        self.set_chem_consumer()

    def set_m3phs(self):
        '''
        Summary: 计算cip流量和wash m3ph
        '''
        if not self.m3ph_per_train:
            self.m3ph_per_train = 10
        self.wash_m3ph = self.wash_m3ph_per_train * self.train_nums_per_group_s1
        self.cip_m3ph = self.m3ph_per_train * self.train_nums_per_group_s1

    def set_oneclean_list(self):
        ls = []
        for op in self.oneclean_list:
            td = [x for x in self.time_detail_list
                  if x.name == op.get('name') and x.label == 'cip']
            if not td:
                raise Exception(f'CIP {op.get("name")} 无time_detail')
            dc = OneCip(
                **op,
                wash_water=self.wash_water,
                feed_liter=self.liter_inside_per_group,  # 不是每次都会装满药剂
                wash_m3ph=self.wash_m3ph,   # 来自父组件
                cip_m3ph=self.cip_m3ph,   # 来自父组件，流速
                time_detail=td[0],  # 主要是需要 每天几次
            )
            ls.append(dc)
        self.oneclean_list = ls

    def set_consumer(self):
        '''
        Summary: 总体消耗
        NOTE:CIP 不考虑水消耗，原则上为外来水源
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
        for x in self.oneclean_list:
            ls = [cc*self.group_nums for cc in x.chem_consumer]
            self.chem_consumer += ls

    @property
    def chem_dosings(self) -> List[ChemDosing]:
        if not self.is_use:
            return []
        ls = []
        for x in self.oneclean_list:
            ls += x.chem_dosings
        return ls

    @property
    def chem_types(self) -> list:
        '''
        Summary: 化学药剂种类
        '''
        return list(set([x.name for x in self.chem_dosings]))

    @property
    def chem_dosings_nums(self):
        return len(self.chem_dosings)
