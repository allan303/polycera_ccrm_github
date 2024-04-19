#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2021-04-11
'''
Summary: 商业化产品
'''

from dataclasses import dataclass
from autodesign.products.base_product import BaseProductMixin


@dataclass
class CartridgeFilter(BaseProductMixin):
    '''
    保安过滤器
    '''
    catalog: str = '9.1'
    material: str = 'SS304'
    q: float = 0  # 流量
    precision: float = 5    # 过滤精度

    def set_spec(self):
        self.spec = f'Q≥{self.q:.1f}m3/h,过滤精度{self.precision}um'


@dataclass
class PipelineMixer(BaseProductMixin):
    '''
    Summary: 管道混合器（加药时候需要）
    '''
    catalog: str = '9.4'

    def set_spec(self):
        self.spec = f'DN{self.dn}'
