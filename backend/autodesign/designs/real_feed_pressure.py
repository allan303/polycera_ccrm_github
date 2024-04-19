#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2021-07-21
'''
Summary: 原水泵 压力计算
'''
from dataclasses import dataclass
from pydantic import BaseModel
from jackutils.fomulas import get_temp_correction_factor


class OptionRealFeedPressure(BaseModel):
    perm_bar: float = 0.1  # 产水压力
    years: int = 3
    fouling_k: float = 0.9


@dataclass
class RealFeedPressure:
    '''
    Summary: 实际进水压力估算，即Q2
    '''
    # parent
    m3ph_per_train: float   # 产水量
    temp: float = 25  # 温度
    fa_per_module: float = 19.8
    flux_per_bar_25: float = 80  # 基准
    module_nums_per_train: int = 1
    dp_per_train: float = 0.1  # 可传可继承
    # option
    perm_bar: float = 0  # 产水测压力
    years: int = 3
    fouling_k: float = 0.9
    # AUTO
    feed_bar: float = 0  # 目标计算值
    conc_bar: float = 0
    fa_per_train: float = 0  # 列面积
    flux_per_bar_25_years: float = 0  # 污染后的 标准透水性
    flux_lmh: float = 0
    temp_correction_factor: float = 0  # 温度补偿系数
    tmp_bar_25: float = 0
    tmp_bar: float = 0

    def __post_init__(self):
        self.cal()

    def cal(self):
        self.fa_per_train = self.fa_per_module * self.module_nums_per_train
        self.flux_lmh = self.m3ph_per_train / self.fa_per_train * 1000  # 运行通量
        self.flux_per_bar_25_years = self.flux_per_bar_25 * self.fouling_k**self.years
        self.temp_correction_factor = get_temp_correction_factor(self.temp)
        self.tmp_bar_25 = self.flux_lmh / self.flux_per_bar_25_years  # 标准状态下 需要的TMP
        self.tmp_bar = self.tmp_bar_25 / self.temp_correction_factor  # 实际需要tmp
        if not self.perm_bar:
            self.perm_bar = 0.5
        # (f+c)/2 - p = t
        # (f+f-dp)/2 - p = t
        # 2f-dp = (t+p)*2
        # f = ((t+p)*2+dp)/2
        self.feed_bar = ((self.tmp_bar+self.perm_bar)*2 + self.dp_per_train)/2
        self.conc_bar = self.feed_bar - self.dp_per_train
