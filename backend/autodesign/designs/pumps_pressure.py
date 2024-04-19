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


class OptionPumpsPressure(BaseModel):
    feed_pump: float = 4
    cir_pump: float = 2
    backwash_pump: float = 2
    cip_pump: float = 2.5
    feed_vfd: bool = True
    backwash_vfd: bool = True
    cir_vfd: bool = True
    cip_vfd: bool = False
    ceb_pump: float = 2  # 独立的ceb泵
