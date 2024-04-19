#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-05-19
'''
Summary: 运行过程中持续加药
'''

from dataclasses import dataclass, field
from pydantic import BaseModel
from typing import List, Dict
# app
from autodesign.designs.chem import ChemDosing, OptionChemDosing, ChemConsumer
from autodesign.designs.info import Consumer


class OptionDosing(BaseModel):
    '''
    Summary: Dosing 系统运行时候连续加药
    '''
    is_use: bool = False
    chem_dosings: List[OptionChemDosing] = []  # 各种不同药剂配置

    class Config:
        orm_mode = True


default_dosing_option = OptionDosing(
    is_use=False,
    chem_dosings=[
        # OptionChemDosing(
        #     name='hcl',
        #     chem_wt=50,
        #     dosing_wt=50e-4,
        #     solid_price_per_kg=None,

        # ),
        # OptionChemDosing(
        #     name='阻垢剂',
        #     chem_wt=10,
        #     dosing_wt=5e-4,
        #     solid_price_per_kg=300,
        # ),
        # OptionChemDosing(
        #     name='杀菌剂',
        #     chem_wt=10,
        #     dosing_wt=10e-4,
        #     solid_price_per_kg=200,
        # ),
        OptionChemDosing(
            name='pac_fe',
            chem_wt=5,
            dosing_wt=10/10000
        )
    ]
)

'''
==========================以上为 option=========================
==========================以下为 dc ============================
'''


@dataclass
class Dosing():
    '''
    Summary: 连续加药
        - 按照tph来计算，获得Raw 的 实际（需要加入药剂带入的水）
        - 然后带入 main_balance 计算水平衡
        - 然后计算完成 ceb / cip / wash 等消耗的时间后，得到实际运行时间，采用reset_hr_per_day 进行反算
        - 得到每天的各种参数
    '''
    # 来自option
    is_use: bool  # = False
    # = field(default_factory=list)  # 来的时候dict
    chem_dosings: List[ChemDosing]
    # parent
    serie_q0: float   # 单个系列，即单个原水泵q
    hr_per_day: float  # hours_per_day
    serie_nums: int
    # 计算
    # 首先计算全部，之后通过 nums 计算每个单元的用量 和 配置 药剂泵、药剂箱等
    dosing_m3_per_m3_water: float = 0  # 每吨水增加的水量
    one_day_per_serie: Consumer = field(default_factory=Consumer)  # 整个系统 每天消耗
    one_day_total: Consumer = field(default_factory=Consumer)  # 整个系统
    chem_consumer: List[ChemConsumer] = field(default_factory=list)

    def __post_init__(self):
        self.set_chem_dosings()
        self.cal()
        self.set_consumer()
        self.set_chem_consumer()

    def set_chem_dosings(self):
        '''
        Summary: 单个加药系统的计算，最后要考虑nums
        '''
        if not self.chem_dosings:
            return None
        ls = []
        for x in self.chem_dosings:
            # 根据实际运行的组数量进行水量计算，但是计算设备装机时候需要考虑 备用
            cd = ChemDosing(
                **x,
                feed_liter=self.serie_q0*1000  # 只算吨水
            )
            ls.append(cd)
        self.chem_dosings = ls

    def cal(self):
        '''
        Summary: 计算消耗
        '''
        self.dosing_m3_per_m3_water = sum(
            [x.dosing_m3_per_m3_water for x in self.chem_dosings])  # 吨水带入的水

    def set_consumer(self):
        if not self.is_use:
            return None
        self.one_day_per_serie.raw_m3_add = self.serie_q0 * self.dosing_m3_per_m3_water
        self.one_day_total.raw_m3_add = self.one_day_per_serie.raw_m3_add*self.serie_nums

    def set_chem_consumer(self):
        '''
        Summary: x = 运行时间 * 系列数量
        '''
        if not self.is_use:
            return None
        self.chem_consumer = [x.get_chem_summary(
            place='连续加药', chem_consumer_x=self.hr_per_day*self.serie_nums) for x in self.chem_dosings]
