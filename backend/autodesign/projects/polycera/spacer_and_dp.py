#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-05-07

'''
Summary: Polycera 格网计算
'''

from scipy.integrate import quad
import math
from dataclasses import dataclass
from typing import List
from jackutils.units import UnitLength, UnitArea, UnitFlow
from jackutils.fomulas import get_re_water, get_dp_hazen_williams_law


LEAF_FA = 1.0692307692307692  # 双面


def get_spacer_db():
    '''
    Summary: 以面积、leaf_nums为准，leaf_length计算获得
    '''
    return [
        {
            'module_size': '8040',  # 规格
            'module_fa': {'val': 23.6, 'unit': 'm2'},
            'module_length': {'val': 39, 'unit': 'inch'},
            'channel_height': {'val': 40, 'unit': 'mil'},  # feed spacer高度
            'channel_width': {'val': 118, 'unit': 'mil'},  # feed spacer宽度
            # 'leaf_length': {'val': 26, 'unit': 'inch'},  # 膜袋长度
            'cir_q': 34.1,  # 推荐的cir流量
            'leaf_nums': 20,  # 膜袋数量
            'spacer_thickness': {'val': 0.26, 'unit': 'mm'}  # 厚度
        },
        {
            'module_size': '8040',  # 规格
            'module_fa': {'val': 19.8, 'unit': 'm2'},
            'module_length': {'val': 39, 'unit': 'inch'},
            'channel_height': {'val': 65, 'unit': 'mil'},  # feed spacer高度
            'channel_width': {'val': 220.5, 'unit': 'mil'},  # feed spacer宽度
            # 'leaf_length': {'val': 26, 'unit': 'inch'},  # 膜袋长度
            'cir_q': 43.4,  # 推荐的cir流量
            'leaf_nums': 16,  # 膜袋数量
            'spacer_thickness': {'val': 0.4, 'unit': 'mm'}  # 厚度
        },
        {
            'module_size': '8040',  # 规格
            'module_fa': {'val': 13.9, 'unit': 'm2'},
            'module_length': {'val': 39, 'unit': 'inch'},
            'channel_height': {'val': 90, 'unit': 'mil'},  # feed spacer高度
            'channel_width': {'val': 255.9, 'unit': 'mil'},  # feed spacer宽度
            # 'leaf_length': {'val': 26, 'unit': 'inch'},  # 膜袋长度
            'cir_q': 45.4,  # 推荐的cir流量
            'leaf_nums': 12,  # 膜袋数量
            'spacer_thickness': {'val': 0.4, 'unit': 'mm'}  # 厚度
        },
        {
            'module_size': '8040',  # 规格
            'module_fa': {'val': 11.1, 'unit': 'm2'},
            'module_length': {'val': 39, 'unit': 'inch'},
            'channel_height': {'val': 120, 'unit': 'mil'},  # feed spacer高度
            'channel_width': {'val': 275.6, 'unit': 'mil'},
            # 'leaf_length': {'val': 26, 'unit': 'inch'},  # 膜袋长度
            'cir_q': 56.8,  # 推荐的cir流量
            'leaf_nums': 11,  # 膜袋数量
            'spacer_thickness': {'val': 0.4, 'unit': 'mm'}  # 厚度
        },
        {
            'module_size': '4040',  # 规格
            'module_fa': {'val': 5.5, 'unit': 'm2'},
            'module_length': {'val': 39, 'unit': 'inch'},
            'channel_height': {'val': 40, 'unit': 'mil'},  # feed spacer高度
            'channel_width': {'val': 118, 'unit': 'mil'},  # feed spacer宽度
            # 'leaf_length': {'val': 26, 'unit': 'inch'},  # 膜袋长度
            'cir_q': 5.7,  # 推荐的cir流量
            'leaf_nums': 6,  # 膜袋数量
            'spacer_thickness': {'val': 0.4, 'unit': 'mm'}  # 厚度
        },
        {
            'module_size': '4040',  # 规格
            'module_fa': {'val': 4.6, 'unit': 'm2'},
            'module_length': {'val': 39, 'unit': 'inch'},
            'channel_height': {'val': 65, 'unit': 'mil'},  # feed spacer高度
            'channel_width': {'val': 220.5, 'unit': 'mil'},  # feed spacer宽度
            # 'leaf_length': {'val': 26, 'unit': 'inch'},  # 膜袋长度
            'cir_q': 6.2,  # 推荐的cir流量
            'leaf_nums': 4,  # 膜袋数量
            'spacer_thickness': {'val': 0.4, 'unit': 'mm'}  # 厚度
        },
        {
            'module_size': '4040',  # 规格
            'module_fa': {'val': 3.1, 'unit': 'm2'},
            'module_length': {'val': 39, 'unit': 'inch'},
            'channel_height': {'val': 90, 'unit': 'mil'},  # feed spacer高度
            'channel_width': {'val': 255.9, 'unit': 'mil'},  # feed spacer宽度
            # 'leaf_length': {'val': 26, 'unit': 'inch'},  # 膜袋长度
            'cir_q': 6.8,  # 推荐的cir流量
            'leaf_nums': 3,  # 膜袋数量
            'spacer_thickness': {'val': 0.4, 'unit': 'mm'}  # 厚度
        },
        {
            'module_size': '4040',  # 规格
            'module_fa': {'val': 2.5, 'unit': 'm2'},
            'module_length': {'val': 39, 'unit': 'inch'},
            'channel_height': {'val': 120, 'unit': 'mil'},  # feed spacer高度
            'channel_width': {'val': 275.6, 'unit': 'mil'},
            # 'leaf_length': {'val': 26, 'unit': 'inch'},  # 膜袋长度
            'cir_q': 6.8,  # 推荐的cir流量
            'leaf_nums': 3,  # 膜袋数量
            'spacer_thickness': {'val': 0.4, 'unit': 'mm'}  # 厚度
        },
        {
            'module_size': '8080',  # 规格
            'module_fa': {'val': 19.8, 'unit': 'm2'},
            'module_length': {'val': 78, 'unit': 'inch'},
            'channel_height': {'val': 65, 'unit': 'mil'},  # feed spacer高度
            'channel_width': {'val': 220.5, 'unit': 'mil'},  # feed spacer宽度
            # 'leaf_length': {'val': 26, 'unit': 'inch'},  # 膜袋长度
            'cir_q': 43.4,  # 推荐的cir流量
            'leaf_nums': 16,  # 膜袋数量
            'spacer_thickness': {'val': 0.4, 'unit': 'mm'}  # 厚度
        },
        {
            'module_size': '8080',  # 规格
            'module_fa': {'val': 13.9, 'unit': 'm2'},
            'module_length': {'val': 78, 'unit': 'inch'},
            'channel_height': {'val': 90, 'unit': 'mil'},  # feed spacer高度
            'channel_width': {'val': 255.9, 'unit': 'mil'},  # feed spacer宽度
            # 'leaf_length': {'val': 26, 'unit': 'inch'},  # 膜袋长度
            'cir_q': 45.4,  # 推荐的cir流量
            'leaf_nums': 12,  # 膜袋数量
            'spacer_thickness': {'val': 0.4, 'unit': 'mm'}  # 厚度
        },
    ]


SPACER_DB = get_spacer_db()


def get_spacer_config(module_size: str = '8040', spacer_mil: int = 40, fa: float = None):
    '''
    Summary: 根据膜尺寸和格网高度，获得配置
    '''
    dt = {}
    for x in SPACER_DB:
        if x['module_size'] == module_size and x['channel_height']['val'] == spacer_mil:
            dt = x
            if fa:
                dt['module_fa'] = fa
    return dt


'''
Summary: 计算 feed spacer 过流截面积/水力半径/材料本身占据的空间
1) 假设为 正玄曲线
    - 计算弧长
        Y=Asin(ωx+ψ)弧长
        先求弧微分，再积分就可以了吧，如: y=10sin(0.5*x+3)
        1: 一阶导数：y'=10(cos(0.5x+3)0.5)
        2: 弧微分：ds=sqrt(1+y'^2)*dx
        3: 如x=[0,pi/2]，对ds定积分可得：s=7.57887990220783
        积分函数为 f(x) = math.sqrt((1+math.cos(x)**2))
'''


def f(x: float = 0, a: float = 1/2, b: float = math.pi):  # 高度 40mil
    # 模拟 原始格网正弦函数
    # b=1/pi 以调整： 波谷和波谷之间的距离为 2*y,即 f(0)=f(1)=f(2)=0
    return a*math.sin(b*x)


def y(x: float = 0, a: float = 1/2, b: float = math.pi):
    # 一阶导数
    return a * b * math.cos(b*x)


def ds_dx(x: float = 0, a: float = 1/2, b: float = math.pi):
    '''
    Summary: # 弧微分
        接下来只要输入上下限进行积分，即可 求正玄曲线弧长
    '''
    return math.sqrt(1+(a * b * math.cos(b*x))**2)


def get_sinx_arc_length(func=ds_dx, start: float = -0.5, end: float = 1.5):
    '''
    Summary: f(x) = sin(x) 求弧长 （正好是一个类似三角形的区域）
    '''
    return quad(func=func, a=start, b=end)[0]


@dataclass
class PolyceraSpacer():
    '''
    Summary:
        - 假设为正玄曲线
        - 曲线高度为 格网高度
        - 假设半个周期为2倍的高度(即单个桥洞的宽度为 H*2)
        - 格网数量 = 膜袋数量(观察所得)
    '''
    module_size: str = ''
    module_fa: UnitArea = None
    module_length: UnitLength = None
    channel_height: UnitLength = None  # 流道
    channel_width: UnitLength = None
    leaf_nums: int = 1
    spacer_thickness: UnitLength = None
    cir_q: float = 0
    # 计算
    leaf_length: UnitLength = None
    leaf_fa: float = 1  # 双面
    spacer_nums_per_module: int = 0
    spacer_arc_length: UnitLength = UnitLength(unit='mil')  # 单个格网 弧长
    channel_arc_length: UnitLength = UnitLength(unit='mil')  # 单个流道的弧长
    segment_nums_per_spacer: int = 0  # 按照桥洞宽度 分割 的数量
    channel_nums_per_spacer: int = 0  # 单个spacer对应的流道数量
    channel_nums_per_module: int = 0  # 组件流道数量
    channel_perimeter: UnitLength = UnitLength(unit='mil')
    channel_hydro_d_m: float = 0  # 计算Re数用到的 水利半径
    # ca = cross area
    ca_between_two_leaf_m2: float = 0  # 膜袋之间的空间 面积
    ca_per_spacer_m2: float = 0  # 单个格网占据的截面积
    ca_between_two_leaf_net_m2: float = 0  # 每一层之间有效的截面积
    ca_per_module_m2: float = 0  # 组件有效截面积
    ca_per_channel_m2: float = 0  # 单个流道有效截面积

    def __post_init__(self):
        self.set_ucs()
        # self.set_by_logic()
        self.cal_nums()
        self.cal_ca()

    def set_ucs(self):
        # 转换单位
        self.module_fa = UnitArea(**self.module_fa)
        self.module_length = UnitLength(**self.module_length)
        self.channel_height = UnitLength(**self.channel_height)
        # 正玄曲线，波峰波谷之间为2，一个封闭图形为 pi,一个桥洞为2个封闭图形宽度
        self.channel_width = UnitLength(
            **self.channel_width)  # 40mil 一个桥洞为80mil宽度
        self.leaf_length = UnitLength(val=0, unit='m')
        self.spacer_thickness = UnitLength(**self.spacer_thickness)

    def cal_nums(self):
        # leaf_length计算 *1.2为放大系数
        self.leaf_length.val = self.module_fa.get('m2') / self.leaf_nums/2*1.2
        # 格网数 = 膜袋数量
        self.spacer_nums_per_module = self.leaf_nums+1  #
        # 根据（一个桥洞）的宽度进行分割，总共分割为几段
        self.segment_nums_per_spacer = math.floor(self.leaf_length.get(
            'm') / self.channel_width.get('m'))
        # 计算一个格网上，流道数量 (注意一个width中有2个流道,上下各一个)
        self.channel_nums_per_spacer = self.segment_nums_per_spacer*2
        # 组件 桥洞数量
        self.channel_nums_per_module = self.channel_nums_per_spacer * \
            self.spacer_nums_per_module
        # 单个膜袋 fa
        self.leaf_fa = self.module_fa/self.leaf_nums

    def cal_ca(self):
        '''
        Summary: 计算截面积相关
        '''
        # 单个格网 流道截面积+格网截面积
        self.ca_between_two_leaf_m2 = self.leaf_length.get(
            'm') * self.channel_height.get('m')
        # 微积分计算弧长: 一个桥洞弧长
        # 先根据获得的 height和width 生成 微分函数

        def ds_dx(x: float = 0, a: float = 1/2, b: float = math.pi):
            '''
            Summary: # 弧微分
                接下来只要输入上下限进行积分，即可 求正玄曲线弧长
            '''
            a = self.channel_height.get('mil')
            b = 2*math.pi / self.channel_width.get('mil')
            return math.sqrt(1+(a * b * math.cos(b*x))**2)
        # 获取 0 - width  之间的弧长
        self.channel_arc_length.val = get_sinx_arc_length(
            func=ds_dx, start=0, end=self.channel_width.get('mil'))
        # 单个桥洞 的弧长
        self.spacer_arc_length = self.channel_arc_length * self.segment_nums_per_spacer
        # 单个spacer占据的截面积
        self.ca_per_spacer_m2 = self.spacer_arc_length.get('m') * \
            self.spacer_thickness.get('m')
        # 每一层的有效截面积
        self.ca_between_two_leaf_net_m2 = self.ca_between_two_leaf_m2 - self.ca_per_spacer_m2
        # 全部截面积
        self.ca_per_module_m2 = self.ca_between_two_leaf_net_m2 * \
            self.spacer_nums_per_module
        # 每一个 channel 有效面积
        self.ca_per_channel_m2 = self.ca_between_two_leaf_net_m2 / \
            self.channel_nums_per_spacer
        # 计算周长
        self.channel_perimeter = self.channel_arc_length + self.channel_width  # 实际周长
        # 水利半径 4*截面积/实际周长
        # NOTE: *2之后和实际现场结果接近，不清楚原因
        self.channel_hydro_d_m = 4*self.ca_per_channel_m2 / \
            self.channel_perimeter.get('m') * 2.2


@dataclass
class PolyceraDp():
    q: float = 0
    module_nums: int = 1
    module_size: str = '8040'
    spacer_mil: int = 40
    temp: float = 25
    # 计算
    spacer: PolyceraSpacer = None
    flow: UnitFlow = None
    v_m_s: float = 0  # 流速
    re: float = 0
    dp: float = 0

    def __post_init__(self):
        self.set_ucs()
        self.cal()

    def set_ucs(self):
        dt = get_spacer_config(
            module_size=self.module_size, spacer_mil=self.spacer_mil)
        if not dt:
            raise ValueError(
                f'module_size={self.module_size},spacer_mil={self.spacer_mil}找不到对应的格网配置')
        self.spacer = PolyceraSpacer(**dt)
        self.flow = UnitFlow(val=self.q, unit='m3/h')

    def cal(self):
        self.v_m_s = self.flow.get(
            'm3/s') / self.spacer.ca_per_module_m2
        d = self.spacer.channel_hydro_d_m
        # 计算雷诺数
        self.re = get_re_water(d=d, v=self.v_m_s, temp=self.temp)
        # 压损
        self.dp = get_dp_hazen_williams_law(re=self.re,
                                            v_m_s=self.v_m_s,
                                            d_m=self.spacer.channel_hydro_d_m,
                                            length_m=self.spacer.module_length.get('m')*self.module_nums)
