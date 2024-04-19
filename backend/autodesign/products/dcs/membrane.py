#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2021-04-13

'''
Summary: membrane产品
'''
from dataclasses import dataclass, field
from pydantic import BaseModel
from typing import Optional
from autodesign.products.base_product import BaseProductMixin, BaseProductPd
from autodesign.products.base_class import BaseDcDbMixin

'''
Summary: 膜 的归类
- cls 1 : MembraneMaterial
    - 通过名称确定pk
    - 旗下包含膜材料属性，包括化学耐受性、描述等
- cls 2 : FlatSheet
    - 通过名称确定pk
    - 旗下包含 膜材料名称（以确定膜材料性状），
- cls 3 : Fiber （中空纤维丝）
- cls 4 : OperateCondition (非产品)
- cls 5 : CipCondition (非产品)
- cls 6 : BackwashCondition (非产品)
- cls 7 : FlatSheetUf
- cls 8 : FlatSheetNf
'''


@dataclass
class OperateCondition(BaseDcDbMixin):
    '''
    Summary:运行条件集合 flat_sheet
    '''

    name: str = ''  # pk
    operate_ph: str = ''  # 运行ph
    operate_temp: str = ''  # 运行温度
    operate_free_chlorine: float = 0  # 自由氯耐受


@dataclass
class CipCondition(BaseDcDbMixin):
    name: str = ''  # pk
    cip_temp: str = ''  # cip温度
    cip_ph: str = ''  # cip ph
    cip_hcl: str = ''
    cip_citric_acid: str = ''
    cip_naoh: str = ''
    cip_chlorine: str = ''
    cip_ozone: str = 'Not compatible'


@dataclass
class BackwashCondition(BaseDcDbMixin):
    name: str = ''  # pk
    backwash_p: str = ''
    backwash_lmh: str = ''


@dataclass
class FlatSheet(BaseDcDbMixin):
    '''
    平膜 base class
    '''
    catalog: str = ''
    label: str = 'membrane'
    name: str = ''
    unit: str = 'm2'
    membrane_type: str = ''
    membrane_material: str = ''
    mwco: str = ''  # str 有时候可以写范围


@dataclass
class FlatSheetUf(FlatSheet):
    '''
    UF 平膜 （卷式膜）
    '''
    membrane_type: str = 'uf'
    membrane_material: str = ''
    sub_material: str = 'Fabrics'  # 支撑层 无纺布
    mwco: str = ''
    pore_size: str = '0.1um'  # nm


@dataclass
class FlatSheetNf(FlatSheet):
    '''
    Summary: NF 平膜
    '''
    membrane_type: str = 'PA'
    sub_material: str = 'PES/Fabrics'  # 支撑层 无纺布
    mwco: str = '500Da'


@dataclass
class FlatSheetRo(FlatSheet):
    '''
    Summary: RO 平膜
    '''
    membrane_type: str = 'PA'
    sub_material: str = 'PES/Fabrics'  # 支撑层 无纺布
    mwco: str = '100Da'


@dataclass
class PolyceraUfFlatSheet(FlatSheetUf):
    '''
    Summary: PolyceraMembrane
    '''
    collection_name: str = 'polycera_uf_flat_sheet'
    serie: str = ''
    membrane_material: str = ''
    brand: str = 'polycera'


class PolyceraNfFlatSheet(FlatSheetNf):
    collection_name: str = 'polycera_nf_flat_sheet'
    name: str = 'titan-nf-500'
    dye_rej: str = 'Not compatible'
    monovalent_rej: str = 'Not compatible'
    divalent_rej: str = 'Not compatible'
    mwco: str = '500Da'
    membrane_material: str = 'Titan'


@dataclass
class SpiralSerie(BaseDcDbMixin):
    '''
    Summary: 卷式膜 
    '''
    label: str = 'membrane'
    model: str = ''
    # 以下为polycera
    flatsheet: FlatSheet = field(default_factory=FlatSheet)
    membrane_type: str = 'uf'
    name: str = 'hydro-100-32'
    attributes: str = 'HIGH FLOW'
    spacer_mil: int = 32
    spacer_size_mm: float = 0.81
    spacer_type: Optional[str] = 'new'
    operate_pressure_max: float = 8.3
    dp_bar_max: float = 1.6
    oil_ppm_max: float = 5
    tss_ppm_max: float = 100
    btex_ppm_max: float = 0
    flux_min: float = 20
    flux_max: float = 200
    recommond_pre_filter_um: float = 75
    max_backwash_pressure: float = 1.7
    backwash_flux_min: float = 40
    backwash_flux_max: float = 200
    backwash_duration_standard: float = 30  # seconds
    backwash_duration_max: float = 120  # seconds
    notes: Optional[str] = None
    notes_cn: Optional[str] = None


@dataclass
class SpiralMembrane(BaseProductMixin, BaseDcDbMixin):
    '''
    Summary: 卷式膜组件
    '''
    label: str = 'membrane'
    brand: str = ''
    membrane_type: str = 'uf'
    serie: SpiralSerie = field(default_factory=SpiralSerie)
    model: str = ''
    description: str = ''
    module_size: int = 8040
    fa: float = 0
    fa_ft2:  Optional[float] = 0
    hts_code: str = ''
    kg: float = 13
    lbs: float = None
    ship_size: str = '273mm2 x 1,207mm'
    ship_size_inch: str = ''
    outer_wrap: str = 'FRP'
    outer_wrap_cn: str = '玻璃钢'
    endcap: str = 'Female'
    endcap_cn: Optional[str] = None
    cir_m3ph_recommend: float = 17
    test_perm_flow_m3ph: float = 4.6
    test_perm_flux: float = None
    d1: Optional[str] = None
    d2: Optional[str] = None
    l1: Optional[str] = 'N/A'
    l2: Optional[str] = None

    @property
    def test_perm_flow_m3pd(self):
        '''
        Summary: 测试水量 m3/d,用于NF
        '''
        return self.test_perm_flow_m3ph * 24

    @test_perm_flow_m3pd.setter
    def test_perm_flow_m3pd(self, val: float):
        '''
        Summary: 设置
        '''
        self.test_perm_flow_m3ph = val / 24


@dataclass
class ModuleMixin(BaseProductMixin):
    '''
    Summary: 通用膜组件
    '''
    catalog: str = '6'
    fa: float = 0  # m2
    rej_dt: dict = field(default_factory=dict)
    model: str = ''
    is_contained_pv: bool = False  # 是否带膜壳
    install: str = '立式'
    flux_per_bar_25: float = 100  # 25°标准状态下的透水性
    liter_inside: float = 20  # 内部储水量

    def set_spec(self):
        self.spec = f'{self.model}'


@dataclass
class GeneralUF(ModuleMixin):
    '''
    Summary: 超滤通用特性
    '''
    catalog: str = '6.3'
    mwco: str = '100KDa'
    pore_size: str = '0.02um'
    length: float = 1000
    interface_size: str = '进水1.5”，产水1”'

    def set_spec(self):
        self.spec = f'{self.pore_size},{self.module_size}'


class FiberUF(GeneralUF):
    '''
    Summary: 通用 中空纤维
    '''
    catalog: str = '6.3.1'
    p_max: float = 3
    liter_inside: float = 40  # 单支内部容积
    install: str = '立式'
    module_size: str = '8080'
    flux_per_bar_25: float = 80  # 25°标准状态下的透水性


@dataclass
class SpiralUF(GeneralUF):
    '''
    Summary: 卷式膜
    '''
    catalog: str = '6.3.2'
    p_max: float = 8.3
    liter_inside: float = 20  # 单支内部容积
    install: str = '立式'
    spacer_mil: int = 40
    module_size: str = '8040'
    flux_per_bar_25: float = 100  # 25°标准状态下的透水性

    def set_spec(self):
        self.spec = f'{self.spacer_mil}mil,{self.mwco},{self.pore_size},{self.module_size}'


class PolyceraUF(SpiralUF):
    brand: str = 'Polycera'
    collection_name: str = 'polycera_module'
    spacer_mil: int = 40  # 有格网
    module_size: str = '8040'


'''
PD
'''


class SpiralUFPd(BaseProductPd):
    '''
    Summary: 用于 design计算需要的属性，其他过滤掉
    '''
    fa: float = 0  # m2
    model: str = ''
    is_contained_pv: bool = False  # 是否带膜壳
    liter_inside: float = 20  # 单支膜元件内部的 容积
    rej_dt: dict = {'tds': 0.98, 'ss': 1}
    spacer_mil: int = 40
    module_size: str = '8040'
    flux_per_bar_25: float = 80  # 25°标准状态下的透水性

    class Config:
        orm_mode = True


class FiberUFPd(BaseProductPd):
    '''
    Summary: 针对中空纤维
    '''
    fa: float = 0  # m2
    model: str = ''  # 型号
    is_contained_pv: bool = True  # 是否带膜壳
    liter_inside: float = 20  # 单支膜元件内部的 容积
    rej_dt: dict = {'tds': 0.98, 'ss': 1}
    spacer_mil: int = 40
    module_size: str = '8040'
    flux_per_bar_25: float = 80  # 25°标准状态下的透水性

    class Config:
        orm_mode = True


# vessel
@dataclass
class RoVessel(BaseProductMixin):
    '''
    Summary: RO膜壳
    '''
    catalog: str = '6.3.2'
    module_nums: int = 0  # 默认无

    def set_spec(self):
        if self.module_nums:
            self.spec = f'标准{self.module_nums}芯RO膜壳'
        else:
            self.spec = '标准RO膜壳'
        print(self.spec)
