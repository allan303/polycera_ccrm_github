#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-02-28

'''
用于提取通用数据:
主要是 生成table的数据
'''
from dataclasses import dataclass, field, asdict
from pydantic import BaseModel
from typing import Optional, List, Union
import numbers
import copy
from jackutils.units import UnitLength, UnitPressure
# app
from autodesign.core.utils import get_standard_pn, get_standard_kw, get_standard_dn
from autodesign.core import const
from .product_catalog import FLAT_PRODUCT_CATALOG
from .base_class import BaseDcDbMixin
'''
Summary: 通过 JSON 配置直接获得设备清单
1. 通过catalog获取目录中的条目，得到所有默认信息
2. 用手动配置的参数 update 替换数据库中的值
3. 相关计算及赋值
4. 使用PD提取固定格式数据，用作spectable
'''


class BaseProductPd(BaseModel):
    '''
    Summary: 从 product 提取用于spectable的信息(单行产品)
    '''
    collection_name: str = ''  # 产品数据库
    class_name: str = ''
    catalog: str = ''
    product_name: str = ''
    product_name_en: str = ''
    brand: str = ''  # 品牌
    model: str = ''  # 型号
    cad_tag: str = ''  # CAD图纸上的标识
    standard: str = 'cn'
    description: str = ''
    unit: str = ''
    spec: str = ''
    # 以下非提取
    weight_net: float = 0
    weight_pack: float = 0
    module_size: str = ''
    size_pack: str = ''
    material: str = ''
    dn_related: bool = True
    kw_related: bool = True
    pn_related: bool = True
    # 以下为dataclass 动态值
    power: str = ''
    kw: float = 0
    kw_install: float = 0
    kw_k: float = 0
    use_vfd: bool = False  # 是否采用变频
    kw_avg: float = 0  # kw_install * 0.7 ，if vdf
    name: str = ''  # 用于 描述在系统中的名称 比如 进水泵
    pid_id: str = ''
    label: str = ''  # 在系统内的标签：主材,阀门..等
    place: str = ''  # 安装位置
    sort_id: float = 0
    required: bool = True
    warning: str = ''
    remark: str = ''
    nums: int = 1  # 数量
    nums_backup: int = 0  # 备用数量
    nums_total: int = 0  # 备用数量
    hpd: float = 0  # 每日运行小时（电机）
    q: float = 0  # 运行流量 m3/h
    q_min: float = 0
    q_max: float = 0
    p: float = 0  # 运行压力
    p_min: float = 0
    p_max: float = 0
    s: float = 0  # 流速
    pn: int = 0  # 公称压力
    pn_min: float = 0
    pn_max: float = 0
    dn: int = 0
    dn_inch: str = ''
    dn_max: float = 0  # DN最大值
    dn_min: float = 0  # DN最小值

    class Config:
        orm_mode = True


@dataclass
class BaseProductMixin(BaseDcDbMixin):
    '''
    Summary: 
    不针对外部，因此为了方便不编写pydantic接口，直接采用dataclass
    '''
    collection_name: str = ''  # 产品数据库
    class_name: str = ''
    catalog: str = ''
    product_name: str = ''
    product_name_en: str = ''
    brand: str = ''  # 品牌
    model: str = ''  # 型号
    cad_tag: str = ''  # CAD图纸上的标识
    standard: str = 'cn'
    description: str = ''
    unit: str = ''
    spec: str = ''
    # 以下非提取
    weight_net: float = 0
    weight_pack: float = 0
    module_size: str = ''
    size_pack: str = ''
    material: str = ''
    dn_related: bool = True
    kw_related: bool = True
    pn_related: bool = True
    # 以下为dataclass 动态值
    power: str = ''
    kw: float = 0
    kw_install: float = 0
    use_vfd: bool = False  # 是否采用变频
    kw_avg: float = 0  # kw_install * 0.7 ，if vdf
    kw_k: float = 0
    name: str = ''  # 用于 描述在系统中的名称 比如 进水泵
    pid_id: str = ''
    label: str = ''  # 在系统内的标签：主材,阀门..等
    place: str = ''  # 安装位置
    sort_id: float = 0
    required: bool = True
    warning: str = ''
    remark: str = ''
    nums: int = 1  # 数量
    nums_backup: int = 0  # 备用数量
    nums_total: int = 0  # 备用数量
    hpd: float = 0  # 每日运行小时（电机）
    q: float = 0  # 运行流量 m3/h
    q_min: float = 0
    q_max: float = 0
    p: float = 0  # 运行压力
    p_min: float = 0
    p_max: float = 0
    s: float = 0  # 流速
    pn: int = 0  # 公称压力
    pn_min: float = 0
    pn_max: float = 0
    dn: int = 0
    dn_inch: str = ''
    dn_max: float = 0  # DN最大值
    dn_min: float = 0  # DN最小值
    # 方便引入pipe

    def __post_init__(self, **kwargs):
        self.run()

    def run(self):
        # 初始化时候即进行相关计算
        self.p_max = self.p_max or self.p
        self.q_max = self.q_max or self.q
        self.set_dn()
        self.set_inch()
        self.set_pn()
        if not self.kw:
            self.set_kw()
        if not self.kw_install:
            self.set_kw_install()
        if not self.kw_avg:
            self.set_kw_avg()
        if not self.spec:
            self.set_spec()
        if not self.remark:
            self.set_remark()
        if not self.catalog:
            self.set_catalog()
        self.set_sort_id()

    def set_catalog(self):
        '''
        Summary: 设置产品catalog
        '''
        for v in FLAT_PRODUCT_CATALOG.values():
            if self.__class__.__name__ == v['class_name']:
                self.catalog = v['catalog']

    @property
    def kwh_per_day(self):
        '''
        Summary: 每天耗电
        '''
        return self.kw_avg * self.nums * self.hpd

    def __mul__(self, i: numbers.Number):
        # define 乘法 *
        if isinstance(i, numbers.Number) and i >= 0:
            new = copy.deepcopy(self)
            new.nums = int(new.nums * i)
            new.nums_backup = int(new.nums_backup*i)
            return new
        raise TypeError(
            f'{i} is Not a Validate Number, not allowed to use __mul__ with BaseProductMixin')

    def __rmul__(self, i: numbers.Number = 1):
        # i * self
        return self * i

    # @property
    # def spec_pd(self) -> BaseModel:
    #     # 提取的基本信息(pydantic)
    #     return BaseSpecTablePD.from_orm(self)

    @property
    def spec_dt(self) -> dict:
        # 提取的基本信息(dict)
        return asdict(self)

    def set_kw(self):
        # 不覆盖0值
        if not self.kw_related:
            return None
        if not self.power == 'electric':
            return None

    def set_kw_install(self):
        # 主动设置
        self.kw_install = get_standard_kw(self.kw)

    def set_kw_avg(self):
        # 平均功耗, 用于计算电费
        if self.use_vfd:
            self.kw_avg = self.kw_install * 0.7
        else:
            self.kw_avg = self.kw_install

    def set_pn(self):
        if not self.pn_related:
            return None
        if self.pn and not self.pn in const.GB9119:
            self.pn = get_standard_pn(self.p,
                                      max_val=self.pn_max,
                                      min_val=self.pn_min
                                      )
            return None
        if not self.pn and self.p:
            # 未提供PN 但是提供了p
            self.pn = get_standard_pn(self.p,
                                      max_val=self.pn_max,
                                      min_val=self.pn_min
                                      )

    @property
    def pn_uc(self):
        return UnitPressure(self.pn, 'bar')

    @property
    def dn_uc(self):
        return UnitLength(self.dn, 'mm')

    def set_dn(self):
        if not self.dn_related:
            return None
        if self.dn and not self.dn in const.GB9119:
            self.dn = get_standard_dn(self.dn,
                                      max_val=self.dn_max,
                                      min_val=self.dn_min
                                      )
            return None

    def set_inch(self):
        if not self.dn_related:
            return None
        if not self.dn_inch:
            self.dn_inch = const.GB9119.get(self.dn, '')

    def set_spec(self): ...
    def set_remark(self): ...

    def set_sort_id(self, sep: str = '.', times: int = 1000, max_bit: int = 5):
        '''
        Summary: 将 pid_id转换为 sort_id 
        example:
            - pid_id = 1.1 => sort_id = times**5*1 + times*4*1 
            - pid_id = 1.1.1 => sort_id = times**5*1 + times*4*1 + times**3*1
        Param:
            max_bit: 最多支持几位  如 '1.25.32.41.54' 五位
            times: 几进制
        '''
        if not self.pid_id:
            self.sort_id = 0
            return None
        s = self.pid_id
        spl = s.split(sep)  # List[str]
        sort_id = 0
        bit = 5
        for x in spl:
            try:
                v = int(x) * times**bit
                sort_id += v
            except Exception:
                raise('PID_ID中只允许数字')
            bit -= 1
        self.sort_id = sort_id

    @property
    def remark_required(self):
        '''
        Summary: 把是否可选加入remark
        '''
        if self.required:
            return self.remark
        if self.remark:
            return self.remark+',可选'
        else:
            return '可选'
