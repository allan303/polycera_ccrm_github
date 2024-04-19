from typing import Optional, Any, List
from pydantic import BaseModel
# app
from dataclasses import field


class PolyceraMembraneBasePD(BaseModel):
    '''
    Summary: polycera平膜
    '''
    membrane_type: Optional[str]
    serie: Optional[str]
    name: Optional[str]
    pore_size: Optional[str]
    mwco: Optional[str]
    operate_ph: Optional[str]
    operate_temp: Optional[str]
    free_chlorine_ppm: Optional[float]
    cip_temp: Optional[str]
    cip_ph: Optional[str]
    hcl: Optional[str]
    citric_acid: Optional[str]
    naoh: Optional[str]
    chlorine: Optional[str]
    ozone: Optional[str]
    dye_rej: Optional[str] = 'Not compatible'
    monovalent_rej: Optional[str] = 'Not compatible'
    divalent_rej: Optional[str] = 'Not compatible'


class PolyceraSerieBasePD(BaseModel):
    '''
    Summary: 平膜+spacer
    '''
    membrane_type: Optional[str]
    membrane_name: Optional[str]
    name: Optional[str]
    attributes: Optional[str]
    spacer_mil: Optional[float]
    spacer_type: Optional[str]
    operate_pressure_max: Optional[float]
    dp_bar_max: Optional[float]
    oil_ppm_max: Optional[float]
    tss_ppm_max: Optional[float]
    btex_ppm_max: Optional[float]
    flux_min: Optional[float]
    flux_max: Optional[float]
    recommond_pre_filter_um: Optional[float]
    max_backwash_pressure: Optional[float]
    backwash_flux_min: Optional[float]
    backwash_flux_max: Optional[float]
    backwash_duration_standard: Optional[float]
    backwash_duration_max: Optional[float]
    notes: Optional[str]
    notes_cn: Optional[str]


class PolyceraSerieResponsePD(PolyceraSerieBasePD):

    membrane: PolyceraMembraneBasePD


class PolyceraModuleBasePD(BaseModel):
    '''
    Summary: Polycera 膜组件
    '''
    membrane_type: Optional[str]
    serie_name: Optional[str] = None
    model: Optional[str] = None
    description: Optional[str] = None
    description_cn: Optional[str] = None
    module_size: Optional[int] = None
    fa: Optional[float] = None
    hts_code: Optional[str] = None
    kg: Optional[float] = None
    ship_size: Optional[str] = None
    ship_size_inch: Optional[str] = None
    outer_wrap: Optional[str] = None
    outer_wrap_cn: Optional[str] = ''
    endcap: Optional[str] = None
    endcap_cn: Optional[str] = None
    cir_tph_recommend: Optional[float] = None
    test_perm_flow_tph: Optional[float] = None
    unit_price: Optional[float] = None
    lbs: Optional[float] = None
    test_perm_flux: Optional[float] = None
    brand: Optional[str] = 'PolyCera'
    d1: Optional[str] = None
    d2: Optional[str] = None
    l1: Optional[str] = 'N/A'
    l2: Optional[str] = None
    # new add
    name: Optional[str] = None
    material: Optional[str] = None
    module_type: Optional[str] = None
    is_contained_pv: bool = False
    flux_per_bar_25: float = 0
    liter_inside: float = 0


class PolyceraModuleResponsePD(PolyceraModuleBasePD):

    serie: PolyceraSerieResponsePD
