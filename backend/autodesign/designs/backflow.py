#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-04-24

'''
Backflow 
'''

from pydantic import BaseModel


class OptionBackflow(BaseModel):
    '''
    Summary: Backflow
    '''
    is_use: bool = False
    m3ph_per_train: float = 0  # 单列 回流量

    class Config:
        orm_mode = True


default_backflow_option = OptionBackflow(
    is_use=False,
    m3ph_per_train=10
)
