#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-08-11

'''
polycera 设计 类
'''
import datetime
from dataclasses import dataclass, field
from typing import Dict
# app
from autodesign.core.docx_tool import to_docx, get_tpl_object

from autodesign.designs.base_design import MembraneSystemDesign
from autodesign.projects.polycera.spacer_and_dp import PolyceraDp
from autodesign.products.dcs.membrane import SpiralUF



'''
配置 Polycera UF 系统 默认 option
'''


def get_default_op():
    return {'backflow': {'is_use': False, 'm3ph_per_train': 10.0},
            'backwash': {'backwash_wash_m3ph_per_train': None,
                         'duration': {'unit': 'seconds', 'val': 30.0},
                         'duration_add': {'unit': 'seconds', 'val': 30.0},
                         'interval': {'unit': 'minutes', 'val': 45.0},
                         'is_drain_out': True,
                         'is_use': True,
                         'lmh': 150,
                         'pressure': {'unit': 'bar', 'val': 1.7},
                         'use_wash': False},
            'ceb': {'is_use': True,
                    'lmh': 50.0,
                    'oneclean_list': [{'chem_dosings': [{'chem_density': None,
                                                         'chem_wt': 30.0,
                                                         'dosing_wt': 0.2,
                                                         'name': 'hcl',
                                                         'solid_price_per_kg': 0.0}],
                                       'duration_add': {'unit': 'minute', 'val': 5.0},
                                       'interval': {'unit': 'day', 'val': 1.0},
                                       'name': '酸',
                                       'process_list': [{'duration': {'unit': 'second',
                                                                      'val': 30.0},
                                                         'name': 'backwash'},
                                                        {'duration': {'unit': 'second',
                                                                      'val': 60.0},
                                                         'name': 'ceb'},
                                                        {'duration': {'unit': 'minute',
                                                                      'val': 30.0},
                                                         'name': 'soak'},
                                                        {'duration': {'unit': 'second',
                                                                      'val': 30.0},
                                                         'name': 'backwash'},
                                                        {'duration': {'unit': 'second',
                                                                      'val': 30.0},
                                                         'name': 'wash+backwash'}],
                                       'temp': 25}]},
            'cip': {'cip_tank_hrt_minute': 1.5,
                    'is_use': False,
                    'm3ph_per_train': 10.0,
                    'oneclean_list': [{'chem_dosings': [{'chem_density': None,
                                                         'chem_wt': 20.0,
                                                         'dosing_wt': 0.4,
                                                         'name': 'naoh',
                                                         'solid_price_per_kg': 0.0},
                                                        {'chem_density': None,
                                                         'chem_wt': 5.0,
                                                         'dosing_wt': 0.01,
                                                         'name': 'naclo',
                                                         'solid_price_per_kg': 0.0}],
                                       'duration_add': {'unit': 'minute', 'val': 20.0},
                                       'interval': {'unit': 'day', 'val': 30.0},
                                       'name': '碱+氧化剂',
                                       'process_list': [{'duration': {'unit': 'minute',
                                                                      'val': 5.0},
                                                         'name': 'drain'},
                                                        {'duration': {'unit': 'minute',
                                                                      'val': 30.0},
                                                         'name': 'circulate'},
                                                        {'duration': {'unit': 'hours',
                                                                      'val': 2.0},
                                                         'name': 'soak'},
                                                        {'duration': {'unit': 'minute',
                                                                      'val': 30.0},
                                                         'name': 'circulate'},
                                                        {'duration': {'unit': 'minute',
                                                                      'val': 5.0},
                                                         'name': 'drain'},
                                                        {'duration': {'unit': 'minute',
                                                                      'val': 10.0},
                                                         'name': 'wash'}],
                                       'temp': 25}]},
            'cir': {'is_use': False, 'm3ph_per_train': 1.1},
            'is_target_perm': True,
            'dosing': {'chem_dosings': [{
                'name': 'pac', 'dosing_wt': 10/10000, 'chem_wt': 5
            }], 'is_use': True},
            'main_balance': {'serie_nums_backup': 0,
                             'serie_nums': 1,
                             'group_nums_per_serie': 1,
                             'lmh_design': 80,
                             'module_nums_per_train': 2,
                             'rec_operate': 0.95},
            'matter_balance': {'is_use': False},
            'module': {'description_cn': '',
                       'fa': 23.6,
                       'is_contained_pv': False,
                       'model': 'Hydro-UF-100-40-8040',
                       'rej_dt': {'tds': 0.98, 'ss': 1}},
            'raw_flow': {'concs_dt': {'cod': 0, 'ntu': 0, 'oil': 0, 'ss': 0, 'tds': 0},
                         'hpd': 24,
                         'name': '废水',
                         'ph': 17,
                         'q': 100,
                         'q_unit': 'm3/h',
                         'remark': '',
                         'temp': 25,
                         'wwtype': '河水'},
            'wash': {'duration': {'unit': 'second', 'val': 30.0},
                     'duration_add': {'unit': 'second', 'val': 15.0},
                     'interval': {'unit': 'minutes', 'val': 120.0},
                     'is_use': False,
                     'm3ph_per_train': 10}}


@dataclass
class PolyceraDesign(MembraneSystemDesign):
    '''
    Summary: 根据polycera进行定制的 膜系统设计
    '''
    dp_per_train_class: PolyceraDp = None
    module: SpiralUF = field(default_factory=SpiralUF)

    def set_option(self, default_op: dict = None):
        '''
        Summary: 可以有默认值
        '''
        dt = get_default_op()
        super().set_option(default_op=dt)

    def set_dp_per_train(self):
        try:
            self.dp_per_train_class = PolyceraDp(
                q=self.flow_info.train.q2,  # 实际进膜
                module_nums=self.main_balance.module_nums_per_train,
                module_size=str(self.module.module_size),
                spacer_mil=self.module.spacer_mil,
                temp=self.raw_flow.temp
            )
            self.dp_per_train = self.dp_per_train_class.dp
        except Exception as e:
            print(e)

    def to_docx(self,
                filename: str = None,
                to_file: bool = True,
                tpl_name: str = 'polycera_uf计算书_tpl.docx',
                my_context: Dict = None
                ):
        today = datetime.datetime.today().strftime(f"%Y-%m-%d")
        if not filename:
            filename = f'Polycera_{self.real_info.perm_m3:.0f}tpd产水_{today}'
        doc = get_tpl_object(tpl_name)
        context = {'design': self, 'my_context': my_context, 'today': today}
        rs = to_docx(doc=doc,
                     context=context,
                     to_file=to_file,
                     filename=filename)
        return rs
