#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-04-24

'''
cir 
'''

from pydantic import BaseModel


class OptionCir(BaseModel):
    '''
    Summary: cir 循环增压泵
    Note   : 需要考虑是与 group 一一对应还是 1对多
    '''
    # 以下来自 option
    is_use: bool = False
    m3ph_per_train: float = 0  # 控制总循环量

    class Config:
        orm_mode = True


default_cir_option = OptionCir(
    is_use=False,
    m3ph_per_train=30,
)
