#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2021-08-16

'''
Summary: 用于format
'''


def to_price(n: float) -> str:
    return f'{n:,.2f}'


def to_00(n: float) -> str:
    return f'{n:0=2d}'
