#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-03-03


import datetime
from typing import Optional
from pydantic import BaseModel
# app
# 各工艺段
from .main_balance import OptionMainBalance
from .backwash import OptionBackwash
from .raw_flow import OptionRaw
from .backflow import OptionBackflow
from .cir import OptionCir
from .wash import OptionWash
from .ceb import OptionCeb
from .cip import OptionCip
from .dosing import OptionDosing
from .module_for_design import ModuleForDesignPD
from .tanks import TanksOption
from .real_feed_pressure import OptionRealFeedPressure
from .pumps_pressure import OptionPumpsPressure
'''
把 各部分的Options 独立 （目前9部分）
NOTE: 采用Pydantic规范 数据接口，业务逻辑层面无需过多关注输入数据验证等

1. main_balance
2. cir
3. backflow
4. backwash
5. cip
6. ceb
7. wash
8. tank
'''


class OptionIsUse(BaseModel):
    is_use: bool = True


class OptionAll(BaseModel):
    '''
    Summary: 集合所有原始输入数据，base层面的放在1级目录
    NOTE   : 不同产品的设计（如 TMF，Polycera等 都重写这个类，主要是other中）
        -- 膜元件的选项没有包含，因为各种不同膜产品数据库不同，可以对应修改
    '''
    module: ModuleForDesignPD = ModuleForDesignPD()  # 膜组件 必备参数
    raw_flow: OptionRaw = OptionRaw()  # 原水
    is_target_perm: bool = True  # 是否是要求产水量
    dosing: OptionDosing = OptionDosing()  # 连续加药设置
    main_balance: OptionMainBalance = OptionMainBalance()  # 主要设计信息
    wash: OptionWash = OptionWash()  # 冲洗
    backwash: OptionBackwash = OptionBackwash()  # 反洗
    backflow: OptionBackflow = OptionBackflow()  # 浓水回流
    cir: OptionCir = OptionCir()  # 循环补排
    ceb: OptionCeb = OptionCeb()  # CEB
    cip: OptionCip = OptionCip()  # CIP
    tanks: TanksOption = TanksOption()
    other_info: dict = {}  # 文字类的描述,其他非通用配置等
    real_feed_pressure: OptionRealFeedPressure = OptionRealFeedPressure()
    pumps_pressure: OptionPumpsPressure = OptionPumpsPressure()

    class Config:
        orm_mode = True
