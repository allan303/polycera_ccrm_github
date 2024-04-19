
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# File    :   Dtros.py
# Time    :   2019/02/27 16:45:32
# Author  :   Jack Li
# Contact :   allanth3@163.com


from dataclasses import dataclass
from autodesign.products.base_product import BaseProductMixin
from jackutils.list_tool import find_x
from autodesign.core import const

'''
DTRO 单支膜
'''


@dataclass
class DtroDc(BaseProductMixin):
    brand: str = 'DFMTEC/杭州碟滤'
    cad_tag: str = 'dtro'
    model: str = 'DTGE-9405'  # 型号名称
    min_p: int = 30  # 最小运行压力
    max_p: int = 75  # 压力等级
    membrane: str = 'bw'  # 膜包类型
    max_temp: int = 40  # 最高运行温度
    length_mm: int = 1400  # 长度 mm
    size_d: int = 214  # mm  外部尺寸 直径
    nums_dlb: int = 210  # 导流板数量
    nums_membrane: int = 209  # 膜片数量
    fa: float = 9.405  # 过滤面积
    min_liter: float = 500  # 运行流量 min L
    max_liter: float = 1200
    operation_kg: int = 74  # 运行重量
    rej: float = 0.985   # 脱盐率  25℃ # 非平膜，是单只膜的rej
    material_vessel: str = 'FRP'  # 膜壳材质
    material_perm_flange: str = 'POM'  # 配水法兰材质
    material_conc_flange: str = 'Stainless Steel'  # 压力法兰
    material_dlb: str = 'ABS'  # 导流板材质
    label: str = 'membrane'

    def __post_init__(self, *args, **kwargs):
        if not self.pn:
            self.pn = find_x(
                x=self.max_p+20, y_list=const.PRESSURE_LEVEL, use_larger=True)
        if not self.spec:
            self.spec = '{}bar,{}m2'.format(
                self.max_p, self.fa)

    @property
    def operation_p(self):
        return '{}至{}bar'.format(self.min_p, self.max_p)
