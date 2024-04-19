#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-03-03

'''
设计大类
1: SpecTable 管理多个dc
2: SpecTable 衍生出来的DesignBase，多了水量
3: FlowDc
'''

import datetime
from docxtpl import DocxTemplate, InlineImage
import io
from matplotlib import pyplot as plt
import copy
from dataclasses import dataclass, field, asdict
from typing import Dict, Tuple, List
from anytree.search import find_by_attr
from anytree import PreOrderIter, RenderTree
from anytree.importer import DictImporter
import pandas as pd
# from anytree.exporter import DictExporter
# app
from autodesign.designs.flowdc import FlowDc
from autodesign.products.spectable import SpecTable
from jackutils.units import UnitTime
from jackutils.dict_tool import deep_update_dict
from autodesign.designs.info import Consumer, RealInfo, PowerChemConsumer
from .base_options import OptionAll  # 包含了所有options
from .main_balance import MainBalance
from .backwash import Backwash
from .ceb import Ceb
from .wash import Wash
from .cip import Cip
from .dosing import Dosing
from .time import TimeDetail, TimeInfo
from .tanks import SystemTanks
from .module_for_design import ModuleForDesign
from .chem import ChemConsumer
from autodesign.core.docx_tool import to_docx, get_tpl_object
from autodesign.designs.matter_balance import MatterBalance
from autodesign.designs.flow_balance import FlowInfo
from autodesign.products.dcs.pipe import Pipe
from jackutils.json_tool import get_from_json
from autodesign.core.config import JSON_DEST_DESIGN_OPTION
from autodesign.products.spectable import SpecNode, print_specnode_tree
from autodesign.products.get_product import get_product_dc_by_dict
from autodesign.designs.real_feed_pressure import RealFeedPressure


@dataclass
class MembraneSystemDesign():
    '''
    Summary: 基本的设计 mixin
        - 设定Flow:
            产水量还是处理量
        - 计算各工序时间分配：
            工作时间，以及其他耗时
        - 计算dosing
            加药量计算，这部分会增加到原水量中
        - 计算所有水量平衡
            区分 处理量情况 和 产水量情况
        - 计算feedpump
        - 计算wash
        - 计算backflow
        - 计算cir
        - 计算backwash
        - 计算ceb
        - 计算cip
        - 计算train
        - 计算group
    '''

    options: dict = field(default_factory=dict)
    # 产品：单只膜组件，用于确定一系列其他参数
    module: ModuleForDesign = field(default_factory=ModuleForDesign)
    # 计算
    # 原始输入水质水量情况
    raw_flow: FlowDc = field(default_factory=FlowDc)
    temp_perm_m3pd: float = 0  # 用于递归 保存
    # 主要信息保存
    main_balance: MainBalance = field(default_factory=dict)
    wash: Wash = field(default_factory=dict)
    ceb: Ceb = field(default_factory=dict)
    backwash: Backwash = field(default_factory=dict)
    cip: Cip = field(default_factory=dict)
    dosing: Dosing = field(default_factory=dict)
    # 基本信息计算
    flow_info: FlowInfo = field(default_factory=FlowInfo)
    # 主要组件
    time_info: TimeInfo = field(default_factory=TimeInfo)
    one_day_per_group: Consumer = field(default_factory=Consumer)  # 单组
    one_day_total: Consumer = field(default_factory=Consumer)  # 整个系统
    real_info: RealInfo = field(default_factory=RealInfo)  # 保存系统最终结果
    # tanks 信息
    tanks: SystemTanks = field(default_factory=SystemTanks)
    # tree_dict: dict = field(default_factory=dict)
    power_chem_consumer: PowerChemConsumer = field(
        default_factory=PowerChemConsumer)
    other_info: dict = field(default_factory=dict)
    dp_per_train: float = 0.1  # 压差每一列
    real_feed_pressure: RealFeedPressure = None
    chem_consumer: List[ChemConsumer] = field(default_factory=list)

    def __post_init__(self):
        self.set_option()
        self.set_raw()
        self.set_module()
        self.set_time_info()
        # 此处进行迭代计算
        self.cal_all_loop()
        self.set_flow_info()
        self.set_dosing()
        self.set_cip()
        self.set_consumer()
        self.set_real_info()  # 重置信息
        self.set_tanks()
        self.set_dp_per_train()
        self.set_feed_pressure()
        self.set_tree()
        self.set_spectable()
        self.set_power_chem_consumer()
        self.set_other_info()
        self.set_chem_consumer()

    def set_other_info(self):
        import copy
        self.other_info = copy.copy(self.op.other_info)
        self.other_info['create_time_local_str'] = datetime.datetime.today().strftime(
            f"%Y-%m-%d")

    def set_option(self, default_op: dict = None, must_op: dict = None):
        '''
        Summary: 可以有默认值
        '''
        if not isinstance(self.options, dict):
            self.options = {}
        options = deep_update_dict(self.options, must_op)  # dict
        default_op = deep_update_dict(default_op, options)  # dict
        self.options = default_op  # dict
        self.op = OptionAll(**default_op)  # 转换为 pd

    def set_raw(self):
        '''
        Summary: 从option中设置原水
            1）为原水量:
                目标为尽量高的回收率，进水量确定，但是产水量不确定
            2）为要求的产水量：
                为目标产水量，产水量确定，进水量不确定
        '''
        op = self.op.raw_flow  # 包含其他信息
        self.raw_flow = FlowDc(**op.dict())  # 原水

    def set_module(self):
        self.module = self.module.__class__.init_from(self.op.module.dict())
        if self.module.fa <= 0:
            raise ValueError('膜面积必须>0')

    def set_time_info(self):
        '''
        Summary: 设置time_info,全部单位 seconds
        '''
        self.time_info.seconds.total = self.raw_flow.hpd * 3600  # 总运行时间
        op = self.op
        # cip
        hrd = self.raw_flow.hpd  # 初始总时间/每天
        if not self.op.cip.is_use:
            ...
        else:
            hrd_temp = hrd
            for onecip in op.cip.oneclean_list:
                td = TimeDetail(
                    name=f'{onecip.name}',
                    interval=UnitTime(**onecip.interval.dict()),
                    duration=UnitTime(val=onecip.duration_s, unit='second'),
                    duration_add=UnitTime(
                        val=onecip.duration_add_s, unit='second'),
                    remark=onecip.chem_names,
                    label='cip'
                )
                td.cal(hpd=hrd)
                hrd_temp -= (td.waste_seconds_per_day)/3600  # 减少 有效时间/每天
                self.time_info.time_detail_list.append(td)
            hrd = hrd_temp
        # CEB
        if not self.op.ceb.is_use:
            ...
        else:
            hrd_temp = hrd
            for oneceb in op.ceb.oneclean_list:
                td = TimeDetail(
                    name=f'{oneceb.name}',
                    interval=UnitTime(**oneceb.interval.dict()),
                    duration=UnitTime(val=oneceb.duration_s, unit='second'),
                    duration_add=UnitTime(
                        val=oneceb.duration_add_s, unit='second'),
                    remark=oneceb.chem_names,
                    label='ceb'
                )
                td.cal(hpd=hrd)
                hrd_temp -= (td.waste_seconds_per_day)/3600  # 减少 有效时间/每天
                self.time_info.time_detail_list.append(td)
            hrd = hrd_temp
        # backwash
        if not op.backwash.is_use:
            ...
        else:
            td = TimeDetail(
                name=f'backwash',
                interval=UnitTime(
                    val=self.op.backwash.interval_s, unit='second'),
                duration=UnitTime(val=op.backwash.duration_s, unit='second'),
                duration_add=UnitTime(
                    val=op.backwash.duration_add_s, unit='second'),
                remark='',
                label='backwash'
            )
            td.cal(hpd=hrd)
            hrd -= (td.waste_seconds_per_day)/3600  # 减少 有效时间/每天
            self.time_info.time_detail_list.append(td)
        # wash
        if not op.wash.is_use:
            ...
        else:
            td = TimeDetail(
                name=f'wash',
                interval=UnitTime(**op.wash.interval.dict()),
                duration=UnitTime(val=op.wash.duration_s, unit='second'),
                duration_add=UnitTime(
                    val=op.wash.duration_add_s, unit='second'),
                remark='',
                label='wash'
            )
            td.cal(hpd=hrd)
            hrd -= (td.waste_seconds_per_day)/3600  # 减少 有效时间/每天
            self.time_info.time_detail_list.append(td)
        self.time_info.cal_waste_time()

    def set_main_balance(self, train_nums_per_group: int):
        '''
        Summary: 所有mainprocess
        '''
        op = self.op.main_balance
        self.main_balance = MainBalance(
            liter_inside_per_module=self.module.liter_inside,
            fa_per_module=self.module.fa,
            is_contained_pv=self.module.is_contained_pv,  # 此型号是否需要膜壳（但是不代表不能串联，比如TMF）
            operate_hour=self.time_info.hours.operate,
            train_nums_per_group=train_nums_per_group,
            ** op.dict()
        )

    def cal_single_loop(self, train_nums_per_group: int = 1):
        '''
        Summary: 单个loop
            - set_main_balance 中已经采用 临时数据 temp_perm_m3pd
        '''
        self.set_main_balance(train_nums_per_group=train_nums_per_group)
        # 重新根据 main_balance 计算得到的原水量 进行加药计算
        self.set_wash()
        self.set_backwash()
        self.set_ceb()
        # self.set_cip()
        self.set_consumer_no_main_balance()

    def cal_all_loop(self):
        '''
        Summary: 不同的递归模式：
            1-目标为产水量：最终净产水量
            2-目标为处理量：最终的原水量 raw_m3pd_raw = temp_perm_m3pd
        '''
        train_nums_per_group = 1
        target_m3pd = 0
        if self.op.is_target_perm:
            # 为目标产水量时
            while True:
                # 根据目前的配置，计算 backwash/ceb 等的消耗，以及 main_balance的产出
                self.cal_single_loop(train_nums_per_group=train_nums_per_group)
                consumer = self.one_day_total  # 未考虑 main 情况下的消耗
                target_m3pd = self.raw_flow.m3pd - consumer.perm_m3  # consumer.perm_m3 是负数
                if self.main_balance.perm_m3pd >= target_m3pd:
                    # 达到了 产水量要求
                    break
                else:
                    # 增加配置
                    train_nums_per_group += 1
        else:
            # 提供的是处理量
            while True:
                # 根据目前的配置，计算 backwash/ceb 等的消耗，以及 main_balance的产出
                self.cal_single_loop(train_nums_per_group=train_nums_per_group)
                consumer = self.one_day_total  # 未考虑 main 情况下的消耗
                target_m3pd = self.raw_flow.m3pd - consumer.raw_m3  # consumer.perm_m3 是负数
                if self.main_balance.feed_m3pd >= target_m3pd:
                    # 达到了 产水量要求
                    break
                else:
                    # 增加配置
                    train_nums_per_group += 1
        # 目标水量 输入，调整main_balance的lmh_operate
        self.main_balance.set_lmh_operate(
            is_target_perm=self.op.is_target_perm, target_m3pd=target_m3pd)
        # 此处已经找到了合适 的 train_nums_per_group
        self.main_balance.cal_all()

    def set_wash(self):
        '''
        Summary: wash
        '''
        op = self.op.wash
        times_per_day = 0
        if not op.is_use or not op.m3ph_per_train:
            op.is_use = False
            return None
        times_per_day = [
            x for x in self.time_info.time_detail_list if x.name == 'wash'][0].times_per_day
        self.wash = Wash(
            train_nums_per_group_s1=self.main_balance.train_nums_per_group_s1,  # = 1
            group_nums=self.main_balance.group_nums,
            times_per_day=times_per_day,
            **op.dict()
        )

    def set_backwash(self):
        '''
        Summary: 反洗 [单组]
        '''
        op = self.op.backwash
        if not op.is_use:
            self.op.ceb.is_use = False
            return None
        time_detail = [
            x for x in self.time_info.time_detail_list if x.label == 'backwash'][0]
        self.backwash = Backwash(
            **op.dict(),
            times_per_day=time_detail.times_per_day,  # 前期计算好的时间相关信息
            wash_m3ph_per_train=self.op.wash.m3ph_per_train,  # = 0
            fa=self.main_balance.fa_per_group,  # = 0  # 来自 main_balance
            train_nums_per_group_s1=self.main_balance.train_nums_per_group_s1,  # 需要运行的列
            group_nums=self.main_balance.group_nums
        )

    def set_ceb(self):
        '''
        Summary: 对ceb进行计算 [单组]
        '''
        if not self.op.ceb.is_use:
            return None
        op = self.op.ceb  # pydantic
        if not op.oneclean_list:
            op.is_use = False
            return None
        mb = self.main_balance
        # 因为可能包含多个不同配置的CEB，因此需要传入 time_detail_list
        ls = [x for x in self.time_info.time_detail_list if x.label == 'ceb']
        self.ceb = Ceb(
            wash_water=self.op.wash.wash_water,
            backwash_m3ph=self.backwash.backwash_m3ph,  # 系统
            # 来自系统（operate)
            train_nums_per_group_s1=mb.train_nums_per_group_s1,  # 1段膜壳数量
            wash_m3ph_per_train=self.op.wash.m3ph_per_train,
            fa=mb.fa_per_group,  # Group
            time_detail_list=ls,
            group_nums=mb.group_nums,
            backwash_vfd=self.op.pumps_pressure.backwash_vfd,  # 反洗泵是否有变频
            backwash_lmh=self.op.backwash.lmh,  # 反洗通量，ceb通量<=反洗通量
            **op.dict()
        )

    def set_cip(self):
        '''
        Summary: CIP计算 [单组]
        '''
        if not self.op.cip.is_use:
            return None
        op = self.op.cip
        if not op.oneclean_list:
            op.is_use = False
            return None
        mb = self.main_balance
        # 因为可能包含多个不同配置的CIP，因此需要传入 time_detail_list
        ls = [x for x in self.time_info.time_detail_list if x.label == 'cip']
        self.cip = Cip(
            wash_water=self.op.wash.wash_water,
            liter_inside_per_group=mb.liter_inside_per_group,
            # 来自系统（operate)
            train_nums_per_group_s1=mb.train_nums_per_group_s1,  # 1段膜壳数量
            wash_m3ph_per_train=self.op.wash.m3ph_per_train,
            time_detail_list=ls,  # 包含多个CIP的综合信息
            group_nums=mb.group_nums,
            **op.dict()
        )

    def set_dosing(self):
        '''
        Summary: 设置dosing
        '''
        op = self.op.dosing
        if not op.is_use or not self.op.dosing.chem_dosings:
            op.is_use = False
            return None
        self.dosing = Dosing(
            **op.dict(),
            serie_q0=self.flow_info.serie.q0,
            hr_per_day=self.time_info.hours.operate,
            serie_nums=self.main_balance.nums_info.operate.serie  # 运行的 系列数量
        )

    def set_consumer_no_main_balance(self):
        '''
        Summary: 计算水量消耗
        '''
        self.one_day_total = Consumer()
        # 药剂费用 换一个方式
        ls = [self.backwash, self.ceb, self.wash]
        for x in ls:
            if x:
                if x.is_use:
                    self.one_day_total = self.one_day_total + x.one_day_total

    def set_consumer(self):
        '''
        Summary: 计算水量消耗
        '''
        self.one_day_per_group = Consumer()
        self.one_day_total = Consumer()
        # 药剂费用 换一个方式
        ls = [self.main_balance, self.backwash, self.ceb, self.wash]
        for x in ls:
            if x:
                if x.is_use:
                    self.one_day_total = self.one_day_total + x.one_day_total
        self.one_day_per_group = self.one_day_total / self.main_balance.group_nums

    def set_flow_info(self):
        '''
        Summary: 已经配置好 main_balance
        '''
        op = self.op
        mb = self.main_balance
        tt = self.flow_info.group  # 单组作为基准
        tt.q6 = mb.perm_m3ph / mb.group_nums
        tt.rec = mb.rec_operate
        if op.backflow.is_use and op.backflow.m3ph_per_train:
            tt.q7 = op.backflow.m3ph_per_train * mb.train_nums_per_group_s1
        else:
            op.backflow.is_use = False
        if op.cir.is_use and op.cir.m3ph_per_train:
            tt.q2 = op.cir.m3ph_per_train * mb.train_nums_per_group_s1
        if op.backwash.is_use:
            tt.q9 = self.backwash.backwash_m3ph
            if not self.backwash.is_drain_out:
                # 将 反洗耗水平均到 运行周期内
                operate_hour = self.backwash.interval.get('hours')
                tt.q10 = self.backwash.backwash_m3 / operate_hour
        tt.set_balance()
        if not tt.q8:
            op.cir.is_use = False
        # 扩展
        self.flow_info.serie = tt * mb.group_nums_per_serie
        self.flow_info.total = tt * mb.group_nums
        self.flow_info.train = tt / mb.train_nums_per_group_s1

    def set_real_info(self):
        '''
        Summary: 根据各个模块 最终的消耗，计算实际系统的情况
            perm_m3_produced: float = 0  # 总制产水
            perm_m3_use: float = 0  # 总消耗产水
            rec_operate: float = 1  # 运行 回收率
            lmh_operate: float = 0  # 运行回收率
            raw_m3: float = 0  # 总原水排放
            hpd_total: float = 0
            hpd_operate: float = 0
        '''
        info = self.real_info
        info.serie_nums = self.main_balance.serie_nums
        info.group_nums = self.main_balance.group_nums
        info.hpd = self.raw_flow.hpd
        info.lmh_design = self.main_balance.lmh_design
        info.lmh_operate = self.main_balance.lmh_operate
        info.rec_operate = self.main_balance.rec_operate
        info.rec_net = self.one_day_total.perm_m3 / self.one_day_total.raw_m3
        info.rec_once = self.flow_info.total.rec_once
        info.lmh_nominal = self.one_day_total.perm_m3 / \
            self.time_info.hours.total/self.main_balance.fa*1000
        info.perm_m3 = self.one_day_total.perm_m3
        info.drain_m3 = self.one_day_total.drain_m3
        info.raw_m3 = self.one_day_total.raw_m3
        info.chem_rmb_per_m3_water = 0   # 药剂费用
        if self.op.backwash.is_use:
            info.drain_m3_backwash = self.backwash.one_day_total.drain_m3
        if self.op.ceb.is_use:
            info.drain_m3_ceb = self.ceb.one_day_total.drain_m3
        if self.op.cip.is_use:
            info.drain_m3_cip = self.cip.one_day_total.drain_m3
        info.drain_m3_operate = self.main_balance.conc_m3pd

    @property
    def operate_mode(self):
        '''
        Summary: 运行模式：根据配置自动生成
        '''
        if self.op.cir.is_use:
            if self.op.backflow.is_use:
                return '循环补排+浓水回流'
            else:
                return '循环补排'
        else:
            if self.op.backflow.is_use:
                return '浓水回流'
            else:
                if self.main_balance.rec_operate < 100:
                    return '错流单通'
                else:
                    return '死端过滤'

    def get_plot_time_info(self, unit='小时/天', w=6, l=5, left=0.18, right=0.98, wspace=0.4, hspace=0.15,
                           bottom=0.15, top=0.92) -> plt:
        '''
        Summary: matplot制成的 1*1 图像, 时间分布
        '''
        plt.rcParams['font.sans-serif'] = ['Microsoft Yahei']
        plt.rcParams['axes.unicode_minus'] = False
        plt.style.use('ggplot')
        l = 5*0.4
        fig = plt.figure(figsize=(w, l))
        title = '工序时间平衡(小时/天)'
        # 1
        ti = self.time_info.hours
        xs = ['总设计时间', '制水/运行', '反洗', 'CEB', 'CIP']
        ys = [ti.total, ti.operate, ti.backwash, ti.ceb, ti.cip]
        ax1 = plt.subplot(1, 1, 1)
        ax1.barh(xs, ys, color='g')
        # ax1.set_xlabel(unit, fontsize=9)
        # # 2
        # ax2 = plt.subplot(1, 2, 2)
        # ax2.barh(mls.name_upper, mls[unit], color='blue')
        # ax2.set_xlabel(unit, fontsize=9)
        plt.suptitle(title, fontsize=10)
        plt.subplots_adjust(left=left, right=right, wspace=wspace, hspace=hspace,
                            bottom=bottom, top=top,)
        return plt

    def get_plot_perm_balance(self, unit='m3/d', w=6, l=5, left=0.18, right=0.98, wspace=0.4, hspace=0.15,
                              bottom=0.15, top=0.92) -> plt:
        '''
        Summary: matplot制成的 1*1 图像, 时间分布
        '''
        plt.rcParams['font.sans-serif'] = ['Microsoft Yahei']
        plt.rcParams['axes.unicode_minus'] = False
        plt.style.use('ggplot')
        l = 4*0.4
        fig = plt.figure(figsize=(w, l))
        title = '产水量平衡(m3/d)'
        # 1
        ri = self.real_info
        xs = ['总产水量', '自用水量', '净产水量', '原水量']
        ys = [ri.perm_m3_produced, -ri.perm_m3_use,
              ri.perm_m3pd_net, ri.raw_m3pd_raw]
        ax1 = plt.subplot(1, 1, 1)
        ax1.barh(xs, ys, color='g')
        # ax1.set_xlabel(unit, fontsize=9)
        # # 2
        # ax2 = plt.subplot(1, 2, 2)
        # ax2.barh(mls.name_upper, mls[unit], color='blue')
        # ax2.set_xlabel(unit, fontsize=9)
        plt.suptitle(title, fontsize=10)
        plt.subplots_adjust(left=left, right=right, wspace=wspace, hspace=hspace,
                            bottom=bottom, top=top,)
        return plt

    def get_plot_operate_flow_balance(self, unit='m3/d', w=6, l=5, left=0.18, right=0.98, wspace=0.4, hspace=0.15,
                                      bottom=0.15, top=0.92) -> plt:
        '''
        Summary: matplot制成的 1*1 图像, 时间分布
        '''
        plt.rcParams['font.sans-serif'] = ['Microsoft Yahei']
        plt.rcParams['axes.unicode_minus'] = False
        plt.style.use('ggplot')
        l = 4*0.4
        fig = plt.figure(figsize=(w, l))
        title = '单组制水时水量平衡(m3/h)'
        # 1
        fi = self.flow_info.group
        xs = ['原水', '进水泵', '浓水排放', '产水']
        ys = [fi.q0, fi.q1, fi.q5, fi.q6]
        if self.op.cir.is_use:
            xs.append('循环泵')
            ys.append(fi.cir)
        if fi.q7:
            xs.append('浓水回流')
            ys.append(fi.q7)

        ax1 = plt.subplot(1, 1, 1)
        ax1.barh(xs, ys, color='g')
        # ax1.set_xlabel(unit, fontsize=9)
        # # 2
        # ax2 = plt.subplot(1, 2, 2)
        # ax2.barh(mls.name_upper, mls[unit], color='blue')
        # ax2.set_xlabel(unit, fontsize=9)
        plt.suptitle(title, fontsize=10)
        plt.subplots_adjust(left=left, right=right, wspace=wspace, hspace=hspace,
                            bottom=bottom, top=top,)
        return plt

    def get_InlineImage(self, doc: DocxTemplate, pic: plt = None) -> InlineImage:
        '''
        Summary: 生成用于渲染doc的InlineImage
        '''
        p = io.BytesIO()  # 内存地址
        pic.savefig(p, dpi=200)  # 储存到内存
        p.flush()
        p.seek(0)
        return InlineImage(doc, p)

    def get_InlineImage_time_info(self, doc: DocxTemplate):
        return self.get_InlineImage(doc=doc, pic=self.get_plot_time_info())

    def get_InlineImage_perm_balance(self, doc: DocxTemplate):
        return self.get_InlineImage(doc=doc, pic=self.get_plot_perm_balance())

    def get_InlineImage_operate_flow_balance(self, doc: DocxTemplate):
        return self.get_InlineImage(doc=doc, pic=self.get_plot_operate_flow_balance())

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

    def get_matter_balance(self, matter_name: str = 'ss'):
        '''
        Summary: 物料平衡计算,默认为ss, 采用 TOTAL计算，因为 Tank是按照系统来的
        '''
        fi = self.flow_info.total
        mb = MatterBalance(
            matter_name=matter_name,
            rej=float(self.module.rej_dt.get(matter_name, 1)),
            f0_c=self.raw_flow.concs_dt.get(matter_name, 0),
            q0=fi.q0,
            q2=fi.q2,
            q5=fi.q5,
            q6=fi.q6,
            q7=fi.q7,
            q10=fi.q10,
            q11=fi.q11,
            rec=self.main_balance.rec_operate,
            use_backwash=self.op.backwash.is_use,
            backwash_lmh=self.op.backwash.lmh,
            module_fa=self.main_balance.fa_per_module,
            module_nums=self.main_balance.module_nums_per_group,
            backwash_duration_add_s=self.op.backwash.duration_add_s,
            backwash_duration_s=self.op.backwash.duration_s,
            backwash_interval_s=self.op.backwash.interval_s,
            v_per_module_liter=self.op.module.liter_inside,
            v_cir_pip=0.15 if self.op.cir.is_use else 0,
            v_feed_tank=self.raw_flow.m3ph * 0.5,  # 按照半小时停留时间
        )
        return mb

    def set_tanks(self):
        '''
        Summary: 设置所有tank
        '''
        # 原水箱
        op = self.op.tanks
        self.tank_dict = {}
        self.tanks.feed = get_product_dc_by_dict(dict(name='原水箱',
                                                      q=self.flow_info.total.q0,
                                                      hrt=op.feed.hrt_minutes/60,
                                                      material=op.feed.material,
                                                      catalog='5.2',
                                                      pid_id='0.1'))
        self.tanks.perm = get_product_dc_by_dict(dict(name='产水箱',
                                                      q=self.flow_info.total.q6,
                                                      hrt=op.perm.hrt_minutes/60,
                                                      catalog='5.2',
                                                      pid_id='6.0'))
        self.tank_dict['feed'] = {'v': self.tanks.feed.v}
        self.tank_dict['perm'] = {'v': self.tanks.perm.v}
        if self.op.cip.is_use:
            self.tanks.cip = get_product_dc_by_dict(dict(name='CIP水箱',
                                                         q=self.cip.cip_m3ph,
                                                         hrt=op.cip.hrt_minutes/60,
                                                         catalog='5.2',
                                                         pid_id='4.0'))
            self.tank_dict['cip'] = {'v': self.tanks.cip.v}
            # 化学清洗箱容积 必须大于 腔体内容积
            self.tanks.cip.v = max(self.tanks.cip.v,
                                   self.cip.liter_inside_per_group/1000)

    def set_feed_pressure(self):
        '''
        Summary: 估算进水压力要求
        '''
        op = self.op
        self.real_feed_pressure = RealFeedPressure(
            **op.real_feed_pressure.dict(),
            dp_per_train=self.dp_per_train,
            m3ph_per_train=self.flow_info.train.q6,   # 产水量
            module_nums_per_train=op.main_balance.module_nums_per_train,
            flux_per_bar_25=op.module.flux_per_bar_25 or 80,  # 基准透水性
            fa_per_module=op.module.fa,
            temp=op.raw_flow.temp  # 温度

        )

    def set_spectable(self):
        self.spectable = SpecTable(name='设备清单')
        for x in PreOrderIter(self.tree):
            if x.payload.get('pid_id'):
                p = get_product_dc_by_dict(x.payload)
                # 数量 要以 SpecTable property 为准，payload中的要替换
                p.nums = x.nums
                p.nums_backup = x.nums_backup
                p.nums_total = x.nums_total
                if not p.name:
                    p.name = p.product_name
                self.spectable.table.append(p)

    def set_power_chem_consumer(self) -> None:
        '''
        Summary: 设置消耗信息，电耗，药剂耗
        '''
        pcc = self.power_chem_consumer
        pcc.kwh_per_day = self.spectable.kwh_per_day
        pcc.kwh_per_m3 = pcc.kwh_per_day / self.real_info.perm_m3

    @property
    def design_flow_summray(self) -> str:
        '''
        Summary: 描述水量,产水量或者处理量
        '''
        s = '处理量'
        if self.op.is_target_perm:
            s = '产水量'
        rf = self.op.raw_flow
        return f'{rf.q:.1f} {rf.q_unit} ({s})'

   

    @staticmethod
    def set_places_and_pipe_tank_info(root: SpecNode):
        '''
        Summary: 所有place填充
        '''
        for node in PreOrderIter(root):
            if node.is_leaf:
                p = node.parent
                if p:
                    if not node.payload.get('place'):
                        node.payload['place'] = p.name
                    if p.is_pipe:
                        for attr in ['dn', 'pn', 'q']:
                            if not node.payload.get(attr):
                                node.payload[attr] = p.payload.get(attr, 0)
                    if p.is_tank:
                        for attr in ['v']:
                            if not node.payload.get(attr):
                                node.payload[attr] = p.payload.get(attr, 0)

    def set_tree(self, filename: str = 'polycera_design_1.json') -> SpecNode:
        '''
        Summary: 获得设备清单 结构
        '''
        # 直接获取tree Node Root
        tree_dict = get_from_json(
            filename=filename, dirpath=JSON_DEST_DESIGN_OPTION)
        # 动态修改 tree_dict
        importer = DictImporter(nodecls=SpecNode)
        root = importer.import_(tree_dict)  # 重设各种数量
        self.set_tree_dynamic(root=root)
        # find_by_attr 根据 key 和 value 找到第一个匹配的Node
        # NOTE 以下 Tree Node ID 均编制在json文件中
        self.tree = root
        self.tree.set_all_id()
        # 设置所有dn
        # self.tree_dict = DictExporter().export(self.tree)

    def print_tree(self, to_file: bool = False, no_leaf: bool = False):
        print_specnode_tree(self.tree, to_file=to_file, no_leaf=no_leaf)

    @property
    def tree_iter(self):
        '''
        Summary: 用于 doctpl中
        '''
        return RenderTree(self.tree)

    def set_tree_pipes(self, root: SpecNode):
        '''
        Summary: 设置 tree 中管道的信息
        '''
        ds = self
        group_q = ds.flow_info.group
        # train_q = ds.flow_info.train
        serie_q = ds.flow_info.serie
        total_q = ds.flow_info.total
        cip_q = 0
        if ds.cip:
            cip_q = ds.cip.cip_m3ph
        pump_in_s = 1.5
        high_s = 2
        low_s = 1

        def set_pipe_info(value: str = 'value', pipe: Pipe = None, pn: int = 10):
            '''
            Summary: 找到为pipe的子节点 payload 注入 pipe信息
            '''
            n = find_by_attr(root, name='name', value=value)
            if not n:  # 如果没有就不操作
                return None
            for attr in ['dn', 's', 'real_s', 'q']:
                if not n.payload.get(attr):
                    n.payload[attr] = getattr(pipe, attr, 0)
                if not n.payload.get('pn'):
                    n.payload['pn'] = pn
        # 原水箱排空管路
        set_pipe_info(value='原水箱排空管路',
                      pipe=ds.tanks.feed.get_drain_pipe(minutes=ds.op.tanks.feed.drain_minutes))
        # 原水箱出口管路(接原水泵)
        set_pipe_info(value='原水箱出口管路(接原水泵)',
                      pipe=Pipe(s=pump_in_s, q=total_q.q1))
        # 原水泵入口管路
        set_pipe_info(value='原水泵入口管路', pipe=Pipe(s=pump_in_s, q=serie_q.q1))
        # 原水泵出口管路
        set_pipe_info(value='原水泵出口管路', pipe=Pipe(s=high_s, q=serie_q.q1))
        # 过滤器旁通管路
        set_pipe_info(value='过滤器旁通管路', pipe=Pipe(s=high_s, q=serie_q.q1))
        # 膜组进水管路
        set_pipe_info(value='膜组进水管路', pipe=Pipe(s=high_s, q=group_q.q1))
        # 膜组循环泵前后管路
        set_pipe_info(value='膜组循环泵前后管路', pipe=Pipe(s=high_s, q=group_q.q2))
        # 膜组浓水总管(循环+回流+浓排)
        set_pipe_info(value='膜组浓水总管(循环+回流+浓排)',
                      pipe=Pipe(s=high_s, q=group_q.q3))
        # 膜组循环管路(循环+回流)
        set_pipe_info(value='膜组循环管路(循环+回流)', pipe=Pipe(s=high_s, q=group_q.q4))
        # 膜组浓水排放管路
        set_pipe_info(value='膜组浓水排放管路', pipe=Pipe(
            s=high_s, q=max(group_q.q5, group_q.q0*0.1)))
        # 膜组产水管路
        set_pipe_info(value='膜组产水管路', pipe=Pipe(s=low_s, q=group_q.q6))
        # 膜组浓水回流管路(至原水箱)
        set_pipe_info(value='膜组浓水回流管路', pipe=Pipe(s=high_s, q=group_q.q7))
        # 膜组循环回流管路
        set_pipe_info(value='膜组循环回流管路', pipe=Pipe(s=high_s, q=group_q.q8))
        # 膜组反洗入口管道
        set_pipe_info(value='膜组反洗入口管道', pipe=Pipe(s=high_s, q=group_q.q9))
        # 膜组反洗排放管道
        set_pipe_info(value='膜组反洗排放管道', pipe=Pipe(s=high_s, q=group_q.q9))
        # 膜组CIP入口管道
        set_pipe_info(value='膜组CIP入口管道', pipe=Pipe(s=high_s, q=cip_q))
        # 膜组CIP浓水回流管道
        set_pipe_info(value='膜组CIP浓水回流管道', pipe=Pipe(s=high_s, q=cip_q))
        # 膜组CIP产水回流管道
        set_pipe_info(value='膜组CIP产水回流管道', pipe=Pipe(s=low_s, q=cip_q/2))
        # 反洗泵入口管道
        set_pipe_info(value='反洗泵入口管道', pipe=Pipe(
            s=pump_in_s, q=group_q.q9))
        # 反洗泵出口管道
        set_pipe_info(value='反洗泵出口管道', pipe=Pipe(s=high_s, q=group_q.q9))
        # CIP泵入口管道
        set_pipe_info(value='CIP泵入口管道', pipe=Pipe(s=pump_in_s, q=cip_q))
        # CIP泵出口管道
        set_pipe_info(value='CIP泵出口管道', pipe=Pipe(s=high_s, q=cip_q))
        # CIP水箱排空管道
        set_pipe_info(value='CIP水箱排空管道',
                      pipe=ds.tanks.cip.get_drain_pipe(minutes=ds.op.tanks.cip.drain_minutes))
        # 压缩空气入口管道
        set_pipe_info(value='压缩空气入口管道', pipe=Pipe(dn=25))
        # 产水箱排空管道
        set_pipe_info(value='产水箱排空管道',
                      pipe=ds.tanks.perm.get_drain_pipe(minutes=ds.op.tanks.perm.drain_minutes))
        # 产水箱出口管道(接反洗泵)
        set_pipe_info(value='产水箱出口管道(接反洗泵)', pipe=Pipe(
            s=pump_in_s, q=group_q.q9))
        # 独立的CEB泵和管道
        if self.op.ceb.is_use and self.op.ceb.use_ceb_pump:
            set_pipe_info(value='CEB泵入口管道', pipe=Pipe(
                s=pump_in_s, q=self.ceb.ceb_m3ph))
            set_pipe_info(value='CEB泵出口管道', pipe=Pipe(
                s=pump_in_s, q=self.ceb.ceb_m3ph))

    def get_tree_dc(self, value: str, name: str = 'name'):
        '''
        Summary: 通过关键词找到设备
        '''
        node = find_by_attr(self.tree, name=name, value=value)
        if node:
            return get_product_dc_by_dict(node.payload)
        return None

    def set_tree_dynamic(self, root: SpecNode):
        '''
        Summary: 根据系统配置，动态增减root的节点
        1) 编制json的基础框架（基本上包含 design各主要组件）
        2) json --> SpecNode (root)
        3) 动态为 root 增减 children
        如： CEB药剂种类不同，增减计量泵/加药箱等设备
        '''
        def set_payload(name: str = 'name', value: str = 'value', payload: dict = None):
            '''
            Summary: 找到Node，并更新payload
            '''
            n = find_by_attr(root, name=name, value=value)
            if n:
                n.payload.update(payload)
                n.update_payload_nums_total()
        ds = self
        root.name = f'{root.name}({ds.operate_mode})'
        op = ds.op
        chem_pump_x = 10  # 计量泵放大倍数
        # 数量设置
        # serie
        set_payload(value='单套',
                    payload={'nums': ds.main_balance.serie_nums,
                             'nums_backup': ds.main_balance.serie_nums_backup})
        # group
        set_payload(value='膜组模块',
                    payload={'nums': ds.main_balance.group_nums_per_serie})
        # train
        set_payload(value='膜列模块',
                    payload={'nums': ds.main_balance.train_nums_per_group})
        # module
        set_payload(value='膜壳',
                    payload={'module_nums': ds.main_balance.module_nums_per_train, 'spec': f'标准{ds.main_balance.module_nums_per_train}芯RO膜壳'})
        # 膜壳 *芯
        set_payload(value='膜元件',
                    payload={'nums': ds.main_balance.module_nums_per_train,
                             'model': ds.module.model,
                             'spec': f'{ds.module.brand}, {ds.module.model}'})
        # 水箱
        # 原水箱
        set_payload(value='原水箱',
                    payload=asdict(ds.tanks.feed))
        # 产水箱
        set_payload(value='产水箱',
                    payload=asdict(ds.tanks.perm))
        # 原水泵设置
        pumps_op = self.op.pumps_pressure
        # 运行压力：最小1.5
        feed_p = min(pumps_op.feed_pump,
                     round(self.real_feed_pressure.feed_bar))
        feed_p = max(feed_p, 1.5)
        set_payload(value='原水泵', payload={
            'hpd': ds.time_info.hours.operate, 'p': feed_p, 'p_max': pumps_op.feed_pump, 'use_vfd': ds.op.pumps_pressure.feed_vfd})
        # 原水泵 运行时间
        if op.cir.is_use:
            # 循环泵 运行时间,运行压力,增压部分 需要考虑减去原水压力
            cir_p = min(pumps_op.cir_pump,
                        round(self.dp_per_train*1.2))
            cir_p = max(cir_p, 1)
            set_payload(value='循环泵', payload={
                        'hpd': ds.time_info.hours.operate, 'p': cir_p, 'p_max': pumps_op.cir_pump, 'use_vfd': ds.op.pumps_pressure.cir_vfd})
        else:
            # CIR相关管路移除
            find_by_attr(root, name='name', value='膜组循环泵前后管路').parent = None
            find_by_attr(root, name='name',
                         value='膜组浓水总管(循环+回流+浓排)').parent = None
            find_by_attr(root, name='name',
                         value='膜组循环管路(循环+回流)').parent = None
            find_by_attr(root, name='name', value='膜组循环回流管路').parent = None
        # CIP水箱
        if op.cip.is_use:
            set_payload(value='CIP水箱',
                        payload=asdict(ds.tanks.cip))
        # 反洗
        if op.backwash.is_use:
            set_payload(value='反洗模块', payload={
                        'nums': ds.backwash.backwash_nums})
            node_backwash = find_by_attr(root, name='name', value='反洗模块')
            # 添加反洗泵 运行时间
            set_payload(value='反洗泵', payload={
                        'hpd': ds.backwash.hpd_backwash_pump, "p": pumps_op.backwash_pump, 'use_vfd': ds.op.pumps_pressure.backwash_vfd})
            # CEB 动态增加
            node_ceb = find_by_attr(
                root, name='name', value='CEB模块')
            if not op.ceb.is_use:
                node_ceb.parent = None
                # 移除反洗管路上的管道混合器
                find_by_attr(root, name='name',
                             value='管道混合器(用于CEB加药)').parent = None
            else:
                if not op.ceb.use_ceb_pump:
                    # 不使用单独的ceb泵，则删除CEB泵管道
                    find_by_attr(root, name='name',
                                 value='CEB泵入口管道').parent = None
                    find_by_attr(root, name='name',
                                 value='CEB泵出口管道').parent = None
                else:
                    # 移除反洗管路上的管道混合器
                    find_by_attr(root, name='name',
                                 value='管道混合器(用于CEB加药)').parent = None
                    # 设置ceb泵参数
                    set_payload(value='CEB泵', payload={
                        'hpd': ds.time_info.hours.ceb, 'p': pumps_op.ceb_pump})
                # node_ceb = SpecNode(id='3', name='CEB模块', parent=root)

                i = 1
                id_add = len(node_ceb.children)
                for x in ds.ceb.chem_dosings:  # dosing pip
                    pipe = Pipe(name=x.name, dn_min=20,
                                q=x.chem_m3ph*chem_pump_x, s=2)
                    chem_name = x.chem_info.name_cn or x.chem_info.name_upper or x.name
                    node_ceb_x = SpecNode(id=f'{i+id_add}',
                                          name=f'CEB-{chem_name}',
                                          parent=node_ceb)
                    SpecNode(
                        # id='1',
                        name=f'CEB{i}-加药箱',
                        parent=node_ceb_x,
                        payload={
                            "nums": 1,
                            "pid_id": "3.2",
                            "catalog": "5.3",
                            "name": f"CEB-{chem_name}-加药箱",
                            "v": 1,
                            "material": "塑料"
                        },
                    )
                    SpecNode(
                        # id='2',
                        name=f'CEB{i}-计量泵',
                        parent=node_ceb_x,
                        payload={
                            "nums": 1,
                            "pid_id": "3.3",
                            "catalog": "4.4.1",
                            "name": f"CEB-{chem_name}-计量泵",
                            "p": 8,
                            "q": x.chem_m3ph*chem_pump_x,
                            "material": "PVC泵头"
                        }
                    )
                    SpecNode(
                        # id='3',
                        name=f'CEB{i}-背压阀',
                        parent=node_ceb_x,
                        payload={
                            "nums": 1,
                            "pid_id": "3.9",
                            "catalog": "2.5",
                            "name": f"CEB-{chem_name}-背压阀",
                            "dn": pipe.dn,
                            "material": "PVC"
                        }
                    )
                    SpecNode(id='4',
                             name=f'CEB{i}-放空阀',
                             parent=node_ceb_x,
                             payload={
                                "nums": 1,
                                "pid_id": "3.11",
                                "catalog": "2.1",
                                "name": f"CEB-{chem_name}-放空阀",
                                "place": f'{chem_name} CEB加药箱',
                                "dn": 40,
                                "material": "PVC"
                             }
                             )
                    i += 1
        else:
            # 反洗整体移除
            find_by_attr(root, name='name', value='反洗模块').parent = None
            # 膜组反洗相关
            find_by_attr(root, name='name', value='膜组反洗相关').parent = None
        # CIP
        if op.cip.is_use:
            set_payload(value='化学清洗模块', payload={'nums': ds.cip.cip_nums})
            # 加热器
            set_payload(value='CIP加热器', payload={
                        'hpd': ds.time_info.hours.cip})
            # CIP泵
            set_payload(value='CIP泵', payload={
                        'hpd': ds.time_info.hours.cip, "p": pumps_op.cip_pump, 'use_vfd': ds.op.pumps_pressure.cip_vfd})
        else:
            # CIP模块整体移除
            find_by_attr(root, name='name', value='化学清洗模块').parent = None
            # 膜组CIP相关
            find_by_attr(root, name='name', value='膜组CIP相关').parent = None
        # 运行连续加药
        if op.dosing.is_use:
            node_feed_pump = find_by_attr(root, name='name', value='原水泵模块')
            node_dosing = SpecNode(name='连续加药模块', id='4',
                                   parent=node_feed_pump)
            i = 1
            for x in ds.dosing.chem_dosings:  # dosing pip
                # NOTE:计量泵 放大5倍
                pipe = Pipe(name=x.name, dn_min=20,
                            q=x.chem_m3ph*chem_pump_x, s=2)
                chem_name = x.chem_info.name_cn or x.chem_info.name_upper or x.name
                node_x = SpecNode(id=f'{i}',
                                  name=f'连续加药-{chem_name}',
                                  parent=node_dosing)
                SpecNode(id='1',
                         name=f'加药箱',
                         parent=node_x,
                         payload={
                            "nums": 1,
                            "pid_id": "1.10",
                            "catalog": "5.3",
                            "name": "加药箱",
                            "v": 1,
                            "material": "塑料"
                         })
                SpecNode(id='2',
                         name=f'计量泵',
                         parent=node_x,
                         payload={
                            "nums": 1,
                            "pid_id": "1.11",
                            "catalog": "4.4.1",
                            "name": "计量泵",
                            "p": 8,
                            "q": x.chem_m3ph*chem_pump_x,
                            "material": "PVC泵头"})
                SpecNode(id='3',
                         name=f'背压阀',
                         parent=node_x,
                         payload={
                            "nums": 1,
                            "pid_id": "1.12",
                            "catalog": "2.5",
                            "name": "背压阀",
                            "dn": pipe.dn,
                            "material": "PVC"
                         })
                i += 1
        else:
            # dosing管道混合器
            find_by_attr(root, name='name', value='管道混合器(运行加药)').parent = None
        # backflow
        if not op.backflow.is_use:
            find_by_attr(root, name='name',
                         value='膜组浓水回流管路').parent = None

        self.set_tree_pipes(root=root)
        self.set_places_and_pipe_tank_info(root=root)
        if self.op.module.is_contained_pv:
            # 移除膜壳
            find_by_attr(root, name='name', value='膜壳').parent = None
        return root

    def set_dp_per_train(self):
        '''
        Summary: 设置 Train DP
        '''
        ...

    def set_chem_consumer(self):
        '''
        Summary: 总的药剂消耗 dosing + ceb + cip
        '''
        if self.op.dosing.is_use:
            self.chem_consumer += self.dosing.chem_consumer
        if self.op.ceb.is_use:
            self.chem_consumer += self.ceb.chem_consumer
        if self.op.cip.is_use:
            self.chem_consumer += self.cip.chem_consumer

    def get_chem_consumer_df(self):
        '''
        Summary: df ,化学品消耗细则
        '''
        ls = [asdict(x) for x in self.chem_consumer]
        if not ls:
            return None
        df = pd.DataFrame(ls)
        df['dosing_ppm'] = df['dosing_wt'] * 10000
        df['chem_m3pd'] = df['chem_m3ph'] * df['chem_consumer_x']
        df['perm_m3pd'] = self.real_info.perm_m3
        df['rmb_per_kg_solution'] = df['solid_price_per_kg']*df['chem_wt']/100
        df['price_per_day'] = df['rmb_per_kg_solution'] * df['chem_m3pd'] * 1000
        df['price_per_m3'] = df['price_per_day']/df['perm_m3pd']
        return df

    def get_chem_consumer_list(self):
        '''
        Summary: List[Dict] ,化学品消耗细则
        '''
        df = self.get_chem_consumer_df()
        if not isinstance(df, pd.DataFrame):
            return None
        return list(df.T.to_dict().values())

    def get_chem_consumer_price_per_day(self):
        df = self.get_chem_consumer_df()
        if not isinstance(df, pd.DataFrame):
            return 0
        return df.price_per_m3.sum()

    '''
    Summary: 以下为关键设备
    '''
    @property
    def feed_pump(self):
        return self.get_tree_dc('原水泵')

    @property
    def backwash_pump(self):
        return self.get_tree_dc("反洗泵")

    @property
    def cir_pump(self):
        return self.get_tree_dc("循环泵")

    @property
    def cip_pump(self):
        return self.get_tree_dc("CIP泵")

    @property
    def feed_tank(self):
        return self.get_tree_dc('原水箱')

    @property
    def perm_tank(self):
        return self.get_tree_dc('产水箱')

    @property
    def cip_tank(self):
        return self.get_tree_dc('CIP水箱')

    @property
    def pre_filter(self):
        '''
        Summary: 预过滤器
        '''
        return self.get_tree_dc("预过滤器")

    def get_ceb_tank(self, i: int):
        return self.get_tree_dc(f'CEB{i}-加药箱')

    def get_ceb_pump(self, i: int):
        return self.get_tree_dc(f'CEB{i}-计量泵')
