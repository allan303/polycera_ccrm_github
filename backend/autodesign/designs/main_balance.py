#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-04-23

'''
所有设计基本信息
'''
from dataclasses import dataclass, field
import math
from pydantic import BaseModel
from typing import List, Optional
# app
from autodesign.designs.info import Consumer
from .arrange import Arrange

'''
Summary: 此模块主要计算 系统配置，不进行内部流量平衡计算
'''


class OptionMainBalance(BaseModel):
    is_use: bool = True
    lmh_design: float = 80  # 设计通量
    rec_operate: float = 0.95  # 设计运行回收率
    module_nums_per_train: int = 1  # 几芯
    serie_nums: int = 1  # 几个系列，即 几台原水泵
    group_nums_per_serie: int = 1  # 手动设定，但是group_nums可能根据情况会变动（比如设定的太高）
    serie_nums_backup: int = 0  # 备用的系列
    install: Optional[str] = '立式'
    design_pn: int = 10
    k_list: List[int] = []  # 组内 分段

    class Config:
        orm_mode = True
    # @validator('rec_operate')
    # def validate_design_rec(cls, v):
    #     if v <= 0 or v > 1:
    #         raise ValueError(f'设计回收率必须(0-1]，当前为{v}')
    #     return v

    # @validator('module_nums_per_train')
    # def validate_module_nums_per_train(cls, v):
    #     if v < 1:
    #         raise ValueError(f'module_nums_per_train必须>=1，当前为{v}')
    #     return v


'''
========================== 以下为dc ===========================
'''


@dataclass
class PerInfo:
    '''
    Summary: 数量信息
    '''
    serie: int = 0
    group: int = 0
    train: int = 0
    module: int = 0


@dataclass
class NumsInfo:
    '''
    Summary: 包含 运行/备用/合计
    '''
    operate: PerInfo = field(default_factory=PerInfo)
    backup: PerInfo = field(default_factory=PerInfo)
    total: PerInfo = field(default_factory=PerInfo)

    def set_total(self):
        self.total.serie = self.operate.serie + self.backup.serie
        self.total.group = self.operate.group + self.backup.group
        self.total.train = self.operate.train + self.backup.train
        self.total.module = self.operate.module + self.backup.module


@dataclass
class MainBalance():
    '''
    Summary: 只考虑运行operate情况下的平衡，不考虑其他，如反洗等
    （2-迭代算法）
        - 只考虑 提供的水量为进水量 
        - 之后暴力计算得到最终结果
        - 如果不符合要求（偏差>1%) 则 提高原水量 再次计算
    '''

    # 以下来自option
    is_use: bool   # 固定
    lmh_design: float  # = 80  # 设计通量,这个通量和 operate 通量 不太一样
    rec_operate: float  # = 0.95  # 设计运行回收率
    module_nums_per_train: int  # = 1  # 几芯
    serie_nums: int  # 几个系列，即 几台原水泵
    group_nums_per_serie: int   # 手动设定，但是group_nums可能根据情况会变动（比如设定的太高）
    serie_nums_backup: int  # 备用的系列
    install: str
    design_pn: int
    k_list: List[int]
    # 来自其他区域的 option
    liter_inside_per_module: float  # 膜组件 内部体积
    fa_per_module: float  # = 0  # 单支膜面积(module.fa)
    is_contained_pv: bool  # 是否包含膜壳
    operate_hour: float  # 运行时间
    # NOTE: 通过迭代train_nums_per_group，进行近似求解，当满足 perm_m3pd 或者 feed_m3pd 时候 达到要求
    train_nums_per_group: int = 1  # 每组列数量
    # 计算
    # NOTE: 仅考虑输入输出，不考虑内部流量平衡
    perm_m3ph: float = 0
    conc_m3ph: float = 0
    feed_m3ph: float = 0
    perm_m3pd: float = 0  # 如果是产水，用这个值来标定
    conc_m3pd: float = 0
    feed_m3pd: float = 0  # 如果是原水，用这个值来标定
    lmh_operate: float = 0  # 运行工况时候的lmh
    module_nums: int = 0
    module_nums_per_group: int = 0  # 几芯
    module_nums_per_serie: int = 0
    train_nums_per_serie: int = 0
    train_nums: int = 1
    group_nums: int = 1
    fa_per_train: float = 0
    fa_per_group: float = 0
    fa: float = 0  # 系统面积
    fa_total: float = 0  # 运行的面积
    liter_inside_per_group: float = 0  # 腔体内部体积
    nums_info: NumsInfo = field(default_factory=NumsInfo)
    one_day_per_group: Consumer = field(default_factory=Consumer)
    one_day_total: Consumer = field(default_factory=Consumer)
    arrange: Arrange = field(default_factory=Arrange)

    def __post_init__(self):
        self.is_use = True
        self.cal_init()

    def cal_init(self):
        self.set_nums_info_first()  # 系统排列确定,运行通量确定
        self.cal_flow()  # 计算水量

    def cal_all(self):
        '''
        Summary: 外部loop结束后，进行细节计算
        通过 lmh_operate 输入确定的运行通量
        '''
        # self.cal_flow()
        self.set_nums_info_final()
        self.set_arrange()
        self.set_consumer()

    def set_nums_info_first(self):
        '''
        Summary: 通过 serie_nums 起头计算
        '''
        if not self.serie_nums:
            self.serie_nums = 1
        if not self.group_nums_per_serie:
            self.group_nums_per_serie = 1
        # 组数量
        self.group_nums = self.serie_nums * self.group_nums_per_serie
        # train nums
        self.train_nums = self.group_nums * self.train_nums_per_group
        # 膜组件数量
        self.module_nums = self.train_nums * self.module_nums_per_train
        self.module_nums_per_group = self.train_nums_per_group * self.module_nums_per_train
        self.module_nums_per_serie = self.module_nums_per_group * self.group_nums_per_serie
        self.train_nums_per_serie = self.train_nums_per_group * self.group_nums_per_serie
        self.fa = self.fa_per_module * self.module_nums
        self.fa_per_train = self.fa_per_module*self.module_nums_per_train
        self.fa_per_group = self.fa_per_module*self.module_nums_per_group

    def set_nums_info_final(self):
        '''
        Summary: 不进入循环，减少消耗
        '''
        # 设置 nums_info
        a, b = self.nums_info.operate, self.nums_info.backup
        a.serie = self.serie_nums
        a.group = self.group_nums
        a.train = self.train_nums
        a.module = self.module_nums
        b.serie = self.serie_nums_backup
        b.group = self.serie_nums_backup*self.group_nums_per_serie
        b.train = b.group * self.train_nums_per_group
        b.module = b.train*self.module_nums_per_train
        self.nums_info.set_total()
        self.fa_total = self.nums_info.total.module * self.fa_per_module
        self.liter_inside_per_group = self.module_nums_per_group * \
            self.liter_inside_per_module*1.5

    def cal_flow(self):
        '''
        Summary: 计算当前配置下，按照lmh_design, rec_operate 获得的主要水量平衡
        '''
        lmh = self.lmh_design
        if self.lmh_operate:
            lmh = self.lmh_operate
        # 计算m3ph
        self.perm_m3ph = self.fa * lmh / 1000
        self.feed_m3ph = self.perm_m3ph / self.rec_operate
        self.conc_m3ph = self.feed_m3ph - self.perm_m3ph
        # 计算 m3pd
        self.perm_m3pd = self.perm_m3ph * self.operate_hour
        self.conc_m3pd = self.conc_m3ph * self.operate_hour
        self.feed_m3pd = self.feed_m3ph * self.operate_hour

    def set_arrange(self):
        '''
        Summary: 排列计算
        '''
        self.arrange = Arrange(
            k_list=self.k_list, nums=self.train_nums_per_group)

    def set_consumer(self):
        '''
        Summary: 设置消耗
        '''
        self.one_day_total.perm_m3_produced = self.perm_m3pd
        self.one_day_total.drain_m3_operate = self.conc_m3pd
        self.one_day_total.raw_m3_use_operate = self.feed_m3pd
        self.one_day_per_group = self.one_day_total / self.group_nums

    @property
    def summary(self) -> str:
        '''
        Summary: 配置描述
        '''
        mb = self
        s1 = f'{mb.serie_nums}用{mb.serie_nums_backup}备'
        if not self.is_contained_pv:
            return f'{s1}, {mb.group_nums_per_serie}膜组/套, 单膜组{mb.group_config}, {self.install}安装'
        else:
            return f'{s1}, 单套{mb.group_config}, {self.install}安装'

    @property
    def group_config(self) -> str:
        '''
        Summary: 排列信息
        '''
        if not self.is_contained_pv:
            if len(self.arrange.result) > 1:
                return f'({self.arrange.summary})*{self.module_nums_per_train}芯'
            else:
                return f'{self.arrange.summary}*{self.module_nums_per_train}芯'
        else:
            return f'{self.arrange.summary}支膜组件'

    def set_lmh_operate(self, is_target_perm: bool, target_m3pd: float):
        '''
        Summary: 根据 目标水量，设置精确的 lmh_operate
        '''
        if is_target_perm:
            # 以产水量为准
            self.perm_m3pd = target_m3pd
            self.feed_m3pd = self.perm_m3pd / self.rec_operate

        else:
            self.feed_m3pd = target_m3pd
            self.perm_m3pd = self.feed_m3pd*self.rec_operate
        self.conc_m3pd = self.feed_m3pd - self.perm_m3pd
        # m3ph
        self.perm_m3ph = self.perm_m3pd/self.operate_hour
        self.feed_m3ph = self.feed_m3pd/self.operate_hour
        self.conc_m3ph = self.conc_m3pd/self.operate_hour
        self.lmh_operate = self.perm_m3ph / self.fa * 1000

    @property
    def train_nums_per_group_s1(self):
        '''
        Summary: 一段的 列 数量 （如果没有分段排列，则 = train_nums_per_group）
        '''
        return self.arrange.result[0]
