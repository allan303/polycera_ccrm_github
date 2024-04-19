from mongoengine import (
    StringField, BooleanField, FloatField, IntField)
from jackutils.units import UnitArea, UnitLength
from typing import Dict, List
# app
from app.models.base_model import BaseDocument, BaseDesignModuleOrm
from app.models.user.models import UserOrm


# Flat sheet


class PolyceraMembraneOrm(BaseDocument):
    '''
    Summary: polycera平膜
    '''
    membrane_type = StringField(required=True)
    serie = StringField(required=True)
    name = StringField(required=True, unique=True)
    pore_size = StringField(default='20nm')
    mwco = StringField(default='100KDa')
    operate_ph = StringField(required=False)
    operate_temp = StringField(required=False)
    free_chlorine_ppm = FloatField(default=0)
    cip_temp = StringField(default='')
    cip_ph = StringField(default='')
    hcl = StringField(default='')
    citric_acid = StringField(default='')
    naoh = StringField(default='')
    chlorine = StringField(default='')
    ozone = StringField(default='')
    membrane_str = StringField(default='Ultrafiltration')
    dye_rej = StringField(default='Not compatible')
    monovalent_rej = StringField(default='Not compatible')
    divalent_rej = StringField(default='Not compatible')

    def get_series(self):
        return PolyceraSerieOrm.objects(membrane_name=self.name).order_by('name').all()

    @property
    def precision_and_mwco(self):
        if self.pore_size:
            return f'{self.pore_size} nm/{self.mwco}'
        return self.mwco


class PolyceraSerieOrm(BaseDocument):
    '''
    Summary: 平膜+spacer
    '''
    membrane_name = StringField(required=True)
    membrane_type = StringField()
    name = StringField(required=True, unique=True)
    attributes = StringField(default='')
    spacer_mil = IntField(required=False)
    spacer_type = StringField(default='')
    operate_pressure_max = FloatField(required=True)
    dp_bar_max = FloatField(required=True)
    oil_ppm_max = FloatField(required=True)
    tss_ppm_max = FloatField(required=True)
    btex_ppm_max = FloatField(required=False)
    flux_min = FloatField(required=True)
    flux_max = FloatField(required=True)
    recommond_pre_filter_um = FloatField(required=True)
    max_backwash_pressure = FloatField(required=True)
    backwash_flux_min = FloatField(required=True)
    backwash_flux_max = FloatField(required=True)
    backwash_duration_standard = FloatField(required=True)
    backwash_duration_max = FloatField(required=True)
    notes = StringField(default='')
    notes_cn = StringField(default='')

    @property
    def membrane(self):
        return PolyceraMembraneOrm.objects(name=self.membrane_name).first()

    def get_modules(self):
        # 获取 modules(所有)
        return PolyceraModuleOrm.objects(serie_name=self.name).order_by('fa').all()

    def get_modules_large(self):
        # 获取 modules(所有)
        return PolyceraModuleOrm.objects(serie_name=self.name, module_size__gte=4040).order_by('fa').all()

    def get_modules_small(self):
        # 获取 modules(所有)
        return PolyceraModuleOrm.objects(serie_name=self.name, module_size__lt=4040).order_by('fa').all()

    @property
    def operate_flux_range(self):
        return f'{int(self.flux_min)} - {int(self.flux_max)}LMH'

    @property
    def backwash_flux_range(self):
        return f'{int(self.backwash_flux_min)} - {int(self.backwash_flux_max)}LMH'

    @property
    def spacer_mm(self):
        return UnitLength(val=self.spacer_mil, unit='mil').get('mm')


class PolyceraModuleOrm(BaseDesignModuleOrm):
    '''
    Summary: Polycera 膜组件
    '''
    name = StringField(default='超滤')
    material = StringField(default='polycera')  # 材质
    module_type = StringField(default='卷式')
    is_contained_pv = BooleanField(default=False)
    flux_per_bar_25 = FloatField(default=80)
    liter_inside = FloatField(default=22)

    fs_serie = StringField(required=False, default='hydro')
    membrane_type = StringField(required=True, default='uf')
    serie_name = StringField(required=False)
    brand = StringField(default='PolyCera')
    model = StringField(required=True)
    description = StringField(default='')
    description_cn = StringField(default='')
    module_size = IntField(required=True)
    fa = FloatField(required=True)
    hts_code = StringField(default='')
    kg = FloatField(default=0)
    lbs = FloatField(default=0)
    ship_size = StringField(default='')
    ship_size_inch = StringField(default='')
    outer_wrap = StringField(default='')
    outer_wrap_cn = StringField(default='')
    endcap = StringField(default='')
    endcap_cn = StringField(default='')
    cir_tph_recommend = FloatField(required=True)
    test_perm_flow_tph = FloatField(required=True)
    unit_price = FloatField(default=0)
    test_perm_flux = FloatField(default=0)
    spacer_mil = IntField(required=False)  # 用于order
    membrane_name = StringField()
    d1 = StringField()
    d2 = StringField()
    l1 = StringField(default='N/A')
    l2 = StringField()
    is_contained_pv = BooleanField(default=False)

    @property
    def fa_ft2(self):
        return UnitArea(val=self.fa, unit='m2').get('ft2')

    def set_test_perm_flux(self):
        try:
            self.test_perm_flux = self.test_perm_flow_tph / self.fa * 1000
            self.save()
        except:
            pass

    @property
    def serie(self):
        return PolyceraSerieOrm.objects(name=self.serie_name).first()

    @property
    def membrane(self):
        return self.serie.membrane

    @classmethod
    def get_cache(cls) -> List[Dict]:
        '''
        Summary: [{sid:name}] 用于 前台 select
        NOTE： 手动缓存 改善性能
        '''
        return super().get_cache(keys=['sid',
                                       'model',
                                       "is_deleted",
                                       "fa",
                                       "module_size",
                                       "spacer_mil"])

    @classmethod
    def set_ctufs(cls):
        '''
        Summary: 加入 碟滤 CTUF
        '''
        for x in cls.objects.all():
            if str(x.model).startswith('CTUF'):
                x.is_contained_pv = True
                x.save()
