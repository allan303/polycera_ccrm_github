#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-04-13

'''
化学品加药计算
关于浓度、密度、原液、加药浓度、加药量等转换
'''

import copy
from dataclasses import dataclass, field
from pydantic import BaseModel
from typing import Optional
import pandas as pd

# app
from jackutils.json_tool import get_from_json, save_to_json
from autodesign.core.config import JSON_DEST


def get_default_chems():
    '''
    Summary: 从json文件中获得默认chem data
    '''
    return get_from_json(filename='chem.json', dirpath=JSON_DEST)


def get_users_chems():
    '''
    Summary: 获得用户修改过的chem
    '''
    return get_from_json(filename='chem_user.json', dirpath=JSON_DEST)


def save_users_chems(data: dict = None):
    '''
    Summary: 将修改过的json内容保存到自定义的json文件
    '''
    data = data or {}
    return save_to_json(data=data, filename='chem_user.json', dirpath=JSON_DEST)


def get_chems() -> dict:
    '''
    Summary: 获得综合的chems
    '''
    dt = get_default_chems()
    dt2 = get_users_chems()
    dt.update(dt2)
    return dt


# 获得 json文件中的 chem_info data
CHEMS = get_chems()

'''
=============================以上为json文件读取与处理==================
'''
'''
=================== 以下为option====================
'''


class OptionChemDosing(BaseModel):
    '''
    Summary: 接受ceb 化学品配置
        - 父组件还需要传入 feed_m3ph
    '''
    name: Optional[str] = 'hcl'
    chem_wt: Optional[float] = 37
    dosing_wt: Optional[float] = 0.4
    feed_wt: Optional[float] = 0  # 原水 物料 浓度
    solid_price_per_kg: Optional[float] = None  # 默认数据库中的价格
    chem_density: Optional[float] = None  # 可传可不穿


@dataclass
class ChemConsumer():
    place: Optional[str]
    chem_name: Optional[str]
    name_upper: Optional[str]
    chem_name_cn: Optional[str]
    dosing_wt: float
    dosing_ppm: float
    chem_wt: float
    chem_m3ph: float
    chem_lpd: float
    chem_lpm: float
    solid_price_per_kg: float
    chem_consumer_x: float

    def __mul__(self, i: float):
        '''
        Summary: 乘法
        '''
        new = copy.copy(self)
        new.chem_consumer_x = self.chem_consumer_x * i
        return new


'''
== == == == == == == == == == 以下为 dc == == == == == == == == ==
'''


class WtDcPd(BaseModel):
    name: str
    wt: float
    liter: float
    density_kg_l: float
    m3: float
    kg: float
    solid_kg: float
    water_kg: float

    class Config:
        orm_mode = True


@dataclass
class WtDc():
    '''
    Summary: 溶液的基本信息
    '''
    name: str = 'wtdc'
    wt: float = 0  # 质量百分比
    liter: float = 0  # 体积
    density_kg_l: float = 1   # 输入的密度

    def __post_init__(self):
        self.density_kg_l = self.density_kg_l or 1

    @property
    def m3(self):
        return self.liter / 1000

    @m3.setter
    def m3(self, val: float):
        self.liter = val * 1000

    @property
    def kg(self):
        return self.liter * self.density_kg_l

    @kg.setter
    def kg(self, val: float):
        '''
        Summary: 密度不变，改liter
        '''
        self.liter = val / self.density_kg_l

    @property
    def solid_kg(self):
        '''
        Summary: 溶质 质量
        '''
        return self.wt * self.kg/100

    @property
    def water_kg(self):
        '''
        Summary: 水的质量
        '''
        return self.kg - self.solid_kg

    def __add__(self, other: 'WtDc'):
        '''
        Summary:  WtDc1 + WtDc2 = WtDc3
        2个水加起来 变成 新的水（加权平均）
        NOTE: 假设溶质为同一种物质
        '''
        if not isinstance(other, WtDc):
            return self
        new_liter = self.liter + other.liter  # 新体积
        new_kg = self.kg + other.kg  # 新质量
        new_solid_kg = self.solid_kg + other.solid_kg
        new_density = new_kg/new_liter
        new_wt = new_solid_kg / new_kg*100
        new = WtDc(
            wt=new_wt,
            liter=new_liter,
            density_kg_l=new_density
        )
        new.name = f'{self.name}|{other.name}'
        return new


@dataclass
class ChemInfo():
    '''
    Summary: 化学品 固有性质
    '''
    name: str = ''
    solid_price_per_kg: Optional[float] = None  # 数据库中默认价格
    solid_density: Optional[float] = None  # 固体的密度
    # 计算
    name_cn: Optional[str] = ''
    name_upper: Optional[str] = ''
    # wt_list: List[dict] = None

    def __post_init__(self):
        self.set_chem_info()

    def set_chem_info(self):
        '''
        Summary: 设置基本的chem信息
        '''
        self.name = str(self.name).strip().lower()
        db = CHEMS.get(self.name, None)
        if not db:
            # raise KeyError(f'{self.name} not in CHEMS DB')
            self.name_upper = self.name.upper()
            self.name_cn = self.name_cn or str(self.name).upper()
            self.solid_density = self.solid_density or 1
            self.solid_price_per_kg = self.solid_price_per_kg or 0
            self.wt_list = []
            return None
        else:
            self.name_cn = db['name_cn']
            self.name_upper = db['name_upper']
            self.solid_density = self.solid_density or db['solid_density']
            self.wt_list = db['wt_list']
            # 可以手动传入 价格，其他固定
            self.solid_price_per_kg = self.solid_price_per_kg or db['solid_price_per_kg']

    def cal_density(self, wt: float, k: float = 0.693):
        '''
        Summary: 估算不同 wt % 下的水溶液密度
        - k: 溶质到水里以后体积缩水比例
        '''
        if wt < 0 or wt > 100:
            raise ValueError(f'WT 必须在0-100之间')
        if wt == 0:
            return 1
        elif wt == 100:
            return self.solid_density
        # 从 现有的 wt_list 数据中查找
        for x in self.wt_list:
            if x['wt'] == wt:
                return x['density_kg_l']
        # 如果都没有，则进行估算
        h2o_kg = 100 - wt  # 水重量
        chem_kg = wt  # 化学品重量
        h2o_v = h2o_kg
        chem_v = chem_kg/self.solid_density  # 化学品v
        solution_density = 100/(h2o_v+chem_v*k)
        return solution_density


@dataclass
class ChemDosing():
    '''
    Summary: 
        - 化学品类, 按照数据库中的json格式, 这是单一化学品
        - 两种不同浓度溶液（通常为药剂原液+wt=0的原水）， 混合成为目标浓度
    '''
    name: str  # = '' # 化学品名称
    chem_wt: float  # = 30 原液浓度
    dosing_wt: float  # = 0.4 目标浓度
    feed_wt: Optional[float]  # = 0
    solid_price_per_kg: Optional[float]   # 原始价格全部换算为纯固体价格 rmb/kg
    chem_density: Optional[float]   # =1
    # parent
    feed_liter: float  # 必须提供
    # 以下为计算
    # wt_list: List[dict] = None
    dosing_m3_per_m3_water: float = 0  # 药剂和原水水量比例
    chem_info: ChemInfo = ChemInfo()
    chem: WtDc = field(default_factory=WtDc)  # 药剂原液
    feed: WtDc = field(default_factory=WtDc)  # 原水
    dosing: WtDc = field(default_factory=WtDc)  # 合并后的溶液（目标浓度）

    def __post_init__(self):
        self.set_chem_info()
        self.set_chem()
        self.set_feed()
        self.set_dosing()
        self.cal()

    def set_chem_info(self):
        '''
        Summary: 设置基本的chem信息
        '''
        self.chem_info = ChemInfo(
            name=self.name, solid_price_per_kg=self.solid_price_per_kg)

    def set_chem(self):
        if not self.chem_density:
            self.chem_density = self.chem_info.cal_density(wt=self.chem_wt)
        self.chem = WtDc(
            name=f'{self.chem_info.name_upper}原液',
            density_kg_l=self.chem_density,  # 化学品密度
            wt=self.chem_wt,  # 质量百分比
            liter=0  # 此时还没有计算值
        )

    def set_feed(self):
        '''
        Summary: 注意，此流量为 反洗泵(CEB泵)流量
        '''
        self.feed = WtDc(
            name='原水',
            density_kg_l=1,  # 输入的密度
            wt=self.feed_wt,  # 药剂质量百分比
            liter=self.feed_liter
        )

    def set_dosing(self):
        '''
        Summary: 此为 原液+原水 合并
        NOTE: 假设合并后 体积不变，从raw+feed 可以计算 dosing 的 密度
        '''
        self.dosing = WtDc(
            name='配置药剂',
            density_kg_l=1,  # 次密度 应该通过 计算得到liter 和 kg 之后算，不用 cal_density,误差太大
            wt=self.dosing_wt,
            liter=0  # 此时还没有计算
        )

    def cal(self):
        '''
        Summary: 主要计算逻辑
        NOTE: 以下Q 都指  tph（而非m3ph）
        Note:【1】dosing_liter(Q3)=feed_liter(Q1) + chem_liter(Q2)
            - Q3 = Q1 (已知) + Q2 
            - kg3 = kg1(水浓度=0) + kg2  = kg2
            - kg3 = Q3 * wt3 (已知)
            - kg2 = Q2 * wt2 (已知)
            - Q3 = Q2 * wt2 / wt3
            - Q3 = Q1+ Q2 
            - Q2 = Q1/(wt2/wt3-1)
        '''
        if not self.feed_liter:
            raise ValueError('ChemDosing feed_liter 不能为0')
        if self.chem_wt <= self.dosing_wt:  # 浓度直接相等
            raise ValueError(f'chem wt 必须大于 dosing Wt')
        if self.dosing_wt <= self.feed_wt:
            raise ValueError(f'dosing wt 必须大于 feed Wt')
        # 采用考虑密度的计算
        self.chem.kg = self.feed.kg / (self.chem.wt/self.dosing_wt-1)
        self.dosing = self.chem+self.feed
        self.dosing.name = '配置药剂'
        self.dosing_m3_per_m3_water = self.chem.liter / self.feed.liter

    @property
    def name_str(self):
        '''
        Summary: 10%氢氧化钠
        '''
        return f'{self.dosing_wt}% {self.chem_info.name_cn}({self.chem_info.name_upper})'

    @property
    def description(self):
        return f'{self.chem_info.name_cn},原液{self.chem.wt}%,加药{self.dosing.wt}%'

    @property
    def df(self) -> pd.DataFrame:
        return pd.DataFrame([
            WtDcPd.from_orm(self.chem).dict(),
            WtDcPd.from_orm(self.feed).dict(),
            WtDcPd.from_orm(self.dosing).dict(),
        ])

    @property
    def summary(self) -> dict:
        '''
        Summary: 描述 加压的信息
        NOTE: 因为传入的serie_q0 单位为 m3/h ,基于此可以得到chem的流量数据
        '''
        return {
            'chem_name': self.name,  # 化学品名称
            'chem_name_cn': self.chem_info.name_cn,  # 化学品名称
            'chem_m3ph': self.chem_m3ph,
            'chem_lpm': self.chem_lpm
        }

    def get_chem_summary(self, place: str, chem_consumer_x: float):
        '''
        Summary: 单个点 化学品加药的 summary
        '''
        dt = {
            'place': place,
            'chem_name': self.name,  # 化学品名称
            'name_upper': self.chem_info.name_upper,  # 化学品名称
            'chem_name_cn': self.chem_info.name_cn,  # 化学品名称
            'chem_wt': self.chem.wt,
            'chem_m3ph': self.chem_m3ph,  # 此参数代表 加药泵瞬时流量
            'chem_lpd': self.chem_m3ph * 1000,  # 升每日
            'dosing_wt': self.dosing.wt,
            'dosing_ppm': self.dosing.wt * 10000,
            'chem_lpm': self.chem_lpm,  # 此参数代表 加药泵瞬时流量
            'solid_price_per_kg': self.chem_info.solid_price_per_kg,
            'chem_consumer_x': chem_consumer_x
        }
        return ChemConsumer(**dt)

    @property
    def chem_m3ph(self):
        '''
        Summary: 化学品原液 加药量
        '''
        return self.chem.liter/1000

    @property
    def chem_lpm(self):
        return self.chem.liter/60
