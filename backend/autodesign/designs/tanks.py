#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2021-05-08
'''
Summary: 组织 系统内主要tank
'''
from dataclasses import dataclass, field
from pydantic import BaseModel
from autodesign.products.dcs.tank import Tank


class TankOption(BaseModel):
    '''
    Summary: 水箱设置
    '''
    name: str = ''
    nums: int = 1  # 数量
    hrt_minutes: float = 60
    material: str = "碳钢防腐/PP"
    drain_minutes: float = 60  # 排空用时
    # 如果直接指定v 则不进行计算
    v: float = 0


class TanksOption(BaseModel):
    perm: TankOption = TankOption(name='产水箱', hrt_minutes=60)
    feed: TankOption = TankOption(name='原水箱', hrt_minutes=60)
    cip: TankOption = TankOption(
        name='清洗水箱', hrt_minutes=1.5, drain_minutes=15)


@dataclass
class SystemTanks():
    feed: Tank = field(default_factory=Tank)
    perm: Tank = field(default_factory=Tank)
    cip: Tank = field(default_factory=Tank)
