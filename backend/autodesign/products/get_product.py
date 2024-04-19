#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2021-04-13
'''
Summary: 通过 catalog 获得对应的 class 以及 对应数据库中的默认数据
'''
from .base_product import BaseProductMixin
from .product_catalog import FLAT_PRODUCT_CATALOG
from .dcs.pipe import (
    Pipe,
    SoftpiplineDtro,
    BackWashPillar,
    PiplineRelated,
    ReducerPipe
)
from .dcs.valve import Valve
from .dcs.instrument import (
    Instrument,
    FlowGauge,
    FlowGaugeMagnetic,
    PressureGauge,
    ImpulseLine,
    TempGauge,
    ConductivityGauge
)
from .dcs.power_equipments import (
    Agitator,
    HeatExchanger,
    AirCompressor
)
from .dcs.equipment import (
    CartridgeFilter,
    PipelineMixer
)
from .dcs.pump import (
    Pump,
    CentrifugalPump,
    PistonPump,
    ScrewPump,
    DiaphragmPump,
    BoostPump,
    BarrelPump,
    DiaphragmMeteringPump
)
from .dcs.membrane import SpiralUF, RoVessel
from .dcs.tank import (
    Tank,
    TankRound,
    TankSquare
)

PRODUCT_CLASS_LIST = [
    BaseProductMixin,
    Pipe,
    SoftpiplineDtro,
    ReducerPipe,
    BackWashPillar,
    PiplineRelated,
    Valve,
    Instrument,
    FlowGauge,
    FlowGaugeMagnetic,
    PressureGauge,
    ImpulseLine,
    TempGauge,
    ConductivityGauge,
    Agitator,
    HeatExchanger,
    AirCompressor,
    CartridgeFilter,
    PipelineMixer,
    Pump,
    CentrifugalPump,
    PistonPump,
    ScrewPump,
    DiaphragmPump,
    DiaphragmMeteringPump,
    BoostPump,
    BarrelPump,
    SpiralUF,
    RoVessel,
    Tank,
    TankRound,
    TankSquare
]
PRODUCT_CLASS_DICT = {x.__name__: x for x in PRODUCT_CLASS_LIST}


def get_product_dc_by_dict(dt: dict) -> BaseProductMixin:
    '''
    Summary: 通过dict中的catalog 获得 默认类 和 默认产品参数，返回dc
    '''
    catalog = dt.get('catalog')
    # 没有指定正确的catalog，则使用默认类
    if not catalog or not catalog in FLAT_PRODUCT_CATALOG:
        dt['catalog'] = '0'
    # 数据库参数
    default_product_dt = FLAT_PRODUCT_CATALOG[dt['catalog']].copy()
    # 对应dataclass
    cs = PRODUCT_CLASS_DICT[default_product_dt['class_name']]
    # print(cs.__dataclass_fields__)
    # 用户输入数据进行 更新
    default_product_dt.update(dt)
    new_dt = {}
    # 清洗 dt 的key
    for k in default_product_dt.keys():
        if k in cs.__dataclass_fields__:
            new_dt[k] = default_product_dt[k]
        # else:
        #     print('不包含', k)
    return cs(**new_dt)


'''
Summary: 通过配置好的 option_json 直接获取spectable
{
    [{'catalog':''}]
}
'''
