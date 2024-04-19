#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2019-12-11

from dataclasses import dataclass, asdict, field
import pandas as pd
from .flow_pipe import FlowPipe


@dataclass
class Flows():
    f0: FlowPipe = FlowPipe(name='原水', tab='f0')  # 原水
    f1: FlowPipe = FlowPipe(name='原水箱', tab='f1')
    f2: FlowPipe = FlowPipe(name='膜前', tab='f2')
    f3: FlowPipe = FlowPipe(name='膜后', tab='f3')
    f4: FlowPipe = FlowPipe(name='循环管路', tab='f4')
    f5: FlowPipe = FlowPipe(name='浓水排放', tab='f5')
    f6: FlowPipe = FlowPipe(name='产水', tab='f6')
    f7: FlowPipe = FlowPipe(name='浓水回流', tab='f7')
    f8: FlowPipe = FlowPipe(name='循环泵前回流', tab='f8')


@dataclass
class MatterBalance():
    '''
    Summary: 单次过滤,不考虑循环
    f0：原水
    f1：原水泵前
    f2：循环泵前，已经回流
    f3：浓水母管
    f4：循环管路
    f5：浓水排放
    f6：产水
    f7：回流管路
    '''
    # 以下都可以从 main_process中获得
    matter_name: str = ''
    rej: float = 1  # 实际截留率（单次）
    f0_c: float = 0  # 原水浓度
    q0: float = 0  # 原水
    q2: float = 0  # 膜前
    q5: float = 0  # 浓水排放
    q6: float = 0  # 产水量
    q7: float = 0  # 浓水回流
    q10: float = 0  # 反洗平均转为原水
    q11: float = 0  # 反洗时 wash
    rec: float = 0  # 表观回收率 = f5/f0
    module_nums: int = 0  # 膜数量
    module_fa: float = 0  # 单支膜面积
    use_backwash: bool = True  # 是否采用反洗
    backwash_lmh: float = 0  # 反洗通量
    backwash_interval_s: float = 0
    backwash_duration_s: float = 0
    backwash_duration_add_s: float = 0
    backwash_is_drain: bool = True  # 反洗排放 or  回流到原水箱
    # 体积
    v_per_module_liter: float = 25  # 单支膜腔体体积 L
    v_cir_pip: float = 0.15  # 循环管路体积
    v_feed_tank: float = 0  # 循环槽容积
    # 以下计算
    lmh: float = 0  # 产水通量
    v_membrane: float = 0  # 膜+浓水管路腔体内体积
    v_membrane_and_pip: float = 0  # 膜+浓水管路+循环管路体积
    one_circle_seconds: float = 0  # 单个制水周期时间： 产水+反洗
    m3_perm_one_circle: float = 0  # 单个制水周期 产水量
    m3_backwash_one_circle: float = 0  # 单次反洗耗水
    backwash_m3ph: float = 0  # 反洗流量
    # 反洗后 腔体内残留ss 比例，如果 反洗水量> 腔体体积，则=0，否则为0~100%之间
    c_remain_in_membrane_ratio: float = 0
    rec_once: float = 0
    rec_real: float = 0  # 考虑反洗水消耗 的回收率
    fa: float = 0  # 膜面积
    flows: Flows = Flows()
    data_dt: dict = field(default_factory=dict)  # 数据抓取
    flow_list: list = field(default_factory=list)

    def __post_init__(self):
        if not self.q0:
            raise Exception('FEED not valid')
        self.run()

    def run(self):
        self.cal_m3ph()
        self.cal_other()
        self.cal_matter_balance()
        self.set_flow_list()

    @property
    def q0_consider_q10(self):
        return self.q0 - self.q10

    @property
    def f0(self):
        return self.flows.f0

    @property
    def f1(self):
        return self.flows.f1

    @property
    def f2(self):
        return self.flows.f2

    @property
    def f3(self):
        return self.flows.f3

    @property
    def f4(self):
        return self.flows.f4

    @property
    def f5(self):
        return self.flows.f5

    @property
    def f6(self):
        return self.flows.f6

    @property
    def f7(self):
        return self.flows.f7

    @property
    def f8(self):
        return self.flows.f8

    def cal_m3ph(self):
        # 赋值所有水量平衡
        self.f0.c = self.f0_c
        self.f0.m3ph = self.q0
        # NOTE：回收率 需要通过 f5和f6计算，不能按照f0
        # f6/(f6+f5) = rec
        # f6 = rec*f6 + rec*f5
        # f6 = rec*f5/(1-rec)
        self.f5.m3ph = self.q5
        self.f6.m3ph = self.q6
        self.f7.m3ph = self.q7
        # 原水泵 = 原水 + 回流量
        self.f1.m3ph = self.f7.m3ph+self.f0.m3ph
        self.f2.m3ph = self.q2 or self.f1.m3ph
        self.f8.m3ph = self.f2.m3ph-self.f1.m3ph
        self.f4.m3ph = self.f7.m3ph + self.f8.m3ph
        self.f3.m3ph = self.f2.m3ph - self.f6.m3ph

    def cal_other(self):
        '''
        Summary:   
        '''
        # if self.use_backwash:
        #     # 采用反洗时，默认为UF，截留率=100%
        #     self.rej = 1
        self.one_circle_seconds = self.backwash_duration_add_s + \
            self.backwash_duration_s+self.backwash_interval_s
        self.fa = self.module_fa * self.module_nums
        # 产水量
        self.lmh = self.f6.m3ph/self.fa*1000
        self.v_membrane = self.v_per_module_liter/1000 * self.module_nums
        if not self.f8.m3ph:
            self.v_cir_pip = 0
        else:
            self.v_cir_pip = self.v_membrane/1.5
        self.v_membrane_and_pip = self.v_membrane + self.v_cir_pip
        self.m3_perm_one_circle = self.f6.m3ph * self.backwash_interval_s/3600
        # 反洗流量
        self.backwash_m3ph = self.fa * self.backwash_lmh/1000
        # 反洗耗水
        self.m3_backwash_one_circle = self.backwash_m3ph * \
            self.backwash_duration_s/3600
        delt_m3 = self.v_membrane_and_pip - self.m3_backwash_one_circle
        if delt_m3 > 0:  # 反洗不能完全置换腔体内体积
            self.c_remain_in_membrane_ratio = delt_m3 / self.v_membrane_and_pip
        # self.rec = self.f6.m3ph/self.f0.m3ph
        self.rec_once = self.f6.m3ph / (self.f2.m3ph or self.f1.m3ph)
        if not self.backwash_duration_s:  # 无反洗
            self.rec_real = self.rec
        else:
            self.rec_real = (self.f6.m3ph * self.backwash_interval_s -
                             self.m3_backwash_one_circle)/(self.f0.m3ph*self.one_circle_seconds)

    def cal_matter_balance(self):
        '''
        Summary: 计算 物料平衡（ss平衡）
        NOTE：初始默认原水箱装满了原水, 
        1）如果有反洗
            - 如果每次反洗都全部置换 腔体内 浓水，则理论上每一个产水周期开始，腔体内都是浓度=0的水
            - 如果反洗不能完全置换，则每次腔体内都会累计浓度
            - 计算多个大周期后的平衡情况
            - 如果没有浓排（f5）有回流（f7），即类似于管事膜，产水量（f6）应该 = raw + 反洗量 （换算到相同单位）
        2）如果没有反洗，则直接计算大平衡（假设运行一段时间平衡后,比如运行了100h）

        Summary: 采用反洗时，需要考虑 时间，体积，参与平衡
            - 采用微积分的思维，将一个产水周期 分解为1000 个时间段
            - 每一个时间段假设浓度相等，则 一个小周期内 输入SS ，排出SS，回流SS可以达到平衡
            - 完成一个产水周期后，计算反洗的效果和残留腔体内SS，然后再进行一个周期的迭代
        '''

        # 1) 当 (rej == 1)完全截留时 & (f0.c >0) & (f5.m3ph==0)无浓水排放时，
        # 随着时间推移系统内浓度越来越大，
        # 此时认为整个系统是一个关于时间(T)的函数，因此必须限定时间才能确定
        # UF系统可以认为 rej==1，因此100%回收率运行时 需要引入 一个产水周期的时间
        if self.use_backwash:
            # 有反洗
            split_nums = 1000
            # 时间分成1000份,再转化为hour
            delt_time = self.backwash_interval_s / split_nums/3600
            m3_into_membrane = self.f2.m3ph * delt_time  # 此段时间内进入 膜内的水量，单位m3
            # 如果分割不够小，会导致单个周期就把所有膜内水都置换了，无法计算
            while m3_into_membrane >= self.v_membrane_and_pip/50:
                # 增加分割
                split_nums += 100
                # 时间分成1000份,再转化为hour
                delt_time = self.backwash_interval_s / split_nums/3600
                m3_into_membrane = self.f2.m3ph * delt_time  # 此段时间内进入 膜内的水量，单位m3

            # 初始浓度全部为 原水浓度
            self.f1.c = self.f0.c
            self.f2.c = self.f0.c
            self.f6.c = self.f2.c * (1-self.rej)  # 根据回收率计算获得 产水浓度
            # 第一次膜内ss平衡：
            # -总体积 => total_v = vp + Q6*dt + Q5*dt
            # -产水体积 => Q6 * dt
            # 浓缩倍数 = 1-Q6 * dt /vp + Q6*dt + Q5*dt
            conc_times = 1-self.f6.c*delt_time / \
                (self.v_membrane_and_pip+self.f6.m3ph*delt_time +
                 self.f5.m3ph*delt_time+self.f7.m3ph*delt_time)
            cp = self.f0.c*conc_times
            self.f3.c = cp
            self.f4.c = cp
            self.f5.c = cp
            self.f7.c = cp
            self.f8.c = cp
            ct = self.f0.c
            # cp = self.f0.c
            ss_in_crum = 0  # 输入ss总量，单位 mg
            ss_out_crum = 0  # 输出ss总量，单位 mg
            vt = self.v_feed_tank  # 原水箱体积
            vp = self.v_membrane_and_pip  # 腔体体积
            '''
            Summary: 方程：有反洗
                说明：一段时间内(delt time,dt),
                    - 原水箱排出的水为 f1，浓度为old，输入f0+f7，流量平衡但是SS不平衡 
                    - 腔体内： 排出为 f5+f6, 输入为 f1，流量平衡单ss不平衡
                ********
                    - 原水箱ss : tank_ss = vt*[ct] 
                    - 原水箱ss_out ： tank_ss_out = C1*Q1*dt
                    - 原水箱ss_in : tank_ss_in =  C0*Q0*dt + C7*Q7*dt
                    - 原水箱更新ss： tank_ss_new = tank_ss -tank_ss_out+tank_ss_in
                    - 原水箱新浓度： [ct_new] = tank_ss_new/vt 

                    - 腔体ss: pip_ss = v_pip * [cp] 
                    - 腔体ss_out: pip_ss_out =  C6*Q6*dt + C5*Q5*dt + C7*Q7*dt
                    - 腔体ss_in: pip_ss_in =  C1*Q1*dt
                    - 腔体更新ss ： pip_ss_new = pip_ss - pip_ss_out + pip_ss_in
                    - 腔体更新浓度： [cp_new] = pip_ss_new/v_pip 

                    - c6 = [cp]*(1-rej)
                    - c5 = c3 = c4 = c8 = c7 = cp
                ********
            '''
            # 数据抓取
            ls_circle_num = []
            ls_i = []
            ls_ct = []
            ls_cp = []
            ls_c6 = []
            ls_c2 = []
            ls_c1 = []
            ls_minute = []
            circle_num = 0
            # print('delt_time:', delt_time, split_nums)
            while True:
                # 一整个产水周期
                # 直到 浓水排放浓度 和 原水输入ss浓度相等，才达到最终平衡
                i = 1
                while i <= split_nums:
                    # 循环槽 污泥平衡
                    tank_ss = vt * ct
                    tank_ss_out = self.f1.ts * delt_time
                    tank_ss_in = (self.f0.ts + self.f7.ts)*delt_time
                    tank_ss_new = tank_ss - tank_ss_out + tank_ss_in
                    # 槽内体积需要更新，如果是TMF运行，因为反洗全部回到循环槽，因此 运行时候 f0< f6+f5，这样才能达到平衡
                    vt_new = vt - self.f1.m3ph * delt_time + \
                        (self.f0.m3ph + self.f7.m3ph)*delt_time
                    ct_new = tank_ss_new/vt_new
                    # 管道内污泥平衡
                    pip_ss = vp * cp
                    pip_ss_out = (self.f6.ts+self.f5.ts+self.f7.ts)*delt_time
                    pip_ss_in = self.f1.ts * delt_time
                    pip_ss_new = pip_ss - pip_ss_out + pip_ss_in
                    cp_new = pip_ss_new/vp
                    # if i % 100 == 0:
                    #     print(i, cp_new)
                    # 系统污泥平衡
                    ss_in = self.f0.ts * delt_time
                    ss_out = (self.f6.ts+self.f5.ts)*delt_time
                    ss_in_crum += ss_in
                    ss_out_crum += ss_out
                    # 更新浓度数据
                    ct = ct_new
                    cp = cp_new
                    self.f1.c = ct  # 原水槽一致
                    self.f3.c = self.f4.c = self.f5.c = self.f8.c = self.f7.c = cp
                    self.f2.c = (self.f1.ts + self.f8.ts)/self.f2.m3ph
                    self.f6.c = self.f2.c * (1-self.rej)
                    if i % 100 == 0:
                        ls_circle_num.append(circle_num)
                        ls_c1.append(self.f1.c)
                        ls_c2.append(self.f2.c)
                        ls_i.append(i)
                        # ls_minute.append(
                        #     i*delt_time*60+circle_num*self.backwash_interval_s/60)
                        ls_minute.append(i*delt_time*60+circle_num*(self.backwash_interval_s +
                                                                    self.backwash_duration_s +
                                                                    self.backwash_duration_add_s)/60)
                        ls_c6.append(self.f6.c)
                        ls_cp.append(cp)
                        ls_ct.append(ct)
                    i += 1

                # 一个产水周期内ss变化
                ss_delt_crum = ss_in_crum - ss_out_crum
                if circle_num >= 99:  # 最后一个周期总是没有反洗
                    break
                # print(circle_num, ct, cp, ss_delt_crum, '打断')
                # 反洗对ss的影响
                pip_ss_new = self.c_remain_in_membrane_ratio * pip_ss_new  # 反洗后腔体内残留ss
                if not self.backwash_is_drain:
                    # 如果反洗不排放，全部回到水箱，水箱内平衡变化
                    tank_ss = vt * ct
                    tank_m3_add = self.m3_backwash_one_circle  # 体积增加
                    tank_ss_add = min(self.m3_backwash_one_circle,
                                      self.v_membrane_and_pip)*cp
                    vt_new = vt+tank_m3_add
                    tank_ss_new = tank_ss+tank_ss_add
                    ct_new = tank_ss_new/vt_new
                    ct, vt = ct_new, vt_new
                else:
                    # 排出系统的话要 计算 ss带出
                    backwash_ss_out = min(self.m3_backwash_one_circle,
                                          self.v_membrane_and_pip)*cp
                    ss_delt_crum -= backwash_ss_out
                # 腔体内平衡
                if self.m3_backwash_one_circle >= self.v_membrane_and_pip:
                    cp = 0  # 浓度为0，全部置换
                else:  # 不能全部置换时，残留ss，降低浓度(按比例即可)
                    cp = cp * self.m3_backwash_one_circle/self.v_membrane_and_pip
                self.f1.c = ct  # 原水槽一致
                self.f3.c = self.f4.c = self.f5.c = self.f8.c = self.f7.c = cp
                self.f2.c = (self.f1.ts + self.f8.ts)/self.f2.m3ph
                self.f6.c = self.f2.c * (1-self.rej)
                circle_num += 1
            self.data_dt = {
                'circle_num': ls_circle_num,
                'i': ls_i,
                'ct': ls_ct,
                'cp': ls_cp,
                'c6': ls_c6,
                'c2': ls_c2,
                'c1': ls_c1,
                'minute': ls_minute
            }

        '''
        Summary: 直接采用一元多次方程
                NOTE: 直接计算动态平衡时，无需考虑腔体内体积等。只要运行足够时间即会达到最终平衡
                已知： C0, REJ , 所有Q
                - [C6]*Q6 + [C5]*Q5 = C0*Q0 (assert √)
                - [C6] / [C2] = 1 -REJ = st  (==>) [C6] = st * [C2]  (assert √)
                - [C7]*Q7 + C0*Q0 = [C1]*Q1 (assert √)
                - [C1]*Q1 + [C8]*Q8 = [C2]*Q2 (assert √)
                - [C6]*Q6 + [C3]*Q3 = [C2]*Q2 (assert √)
                - [C4]*Q4 + [C5]*Q5 = [C3]*Q3 (assert √)
                - [C7]*Q7 + [C8]*Q8 = [C4]*Q4 (assert √)
                - [C3] = [C4] = [C5] = [C7] = [C8] = [CC] (assert √) 
                ---
                - st*[C2]*Q6 + [CC]*Q5 = C0*Q0 (==>) [C2] = (C0*Q0 - [CC]*Q5)/(Q6*st)
                - [CC]*Q7 + C0*Q0 = [C1]*Q1 (==>) [C1] = ([CC]*Q7 + C0*Q0)/Q1
                - [C1]*Q1 + [CC]*Q8 = [C2]*Q2 
                - st*[C2]*Q6 + [CC]*Q3 = [C2]*Q2 (==>) [C2] = [CC]*Q3 / (Q2 - Q6*st)
                ---
                - (C0*Q0 - [CC]*Q5)/(Q6*st) = [CC]*Q3 / (Q2 - Q6*st)
                => (C0*Q0 - [CC]*Q5)*(Q2 - Q6*st) = [CC]*Q3*Q6*st
                => C0*Q0*(Q2 - Q6*st) - [CC]*Q5*(Q2 - Q6*st) = [CC]*Q3*Q6*st
                => [CC]*(Q3*Q6*st+Q5*(Q2 - Q6*st)) = C0*Q0*(Q2 - Q6*st) 
                ***********
                => [CC] = C0*Q0*(Q2 - Q6*st) /(Q3*Q6*st+Q5*(Q2 - Q6*st))
                ***********
                => [C1] = ([CC]*Q7 + C0*Q0)/Q1 
                => [C2] = ([C1]*Q1 + [CC]*Q8)/Q2
                => [C6] = (1 -REJ) * [C2]
        '''
        if not self.use_backwash:
            if self.rec >= 1 and self.rej >= 1:
                # 回收率=100%，截留率=100%，此时是不合理的，
                raise ValueError('不采用反洗时，截留率和回收率都为100%是不合理的。')
            cc = (self.f0.c * self.f0.m3ph*(self.f2.m3ph - self.f6.m3ph*(1-self.rej)))/(
                self.f3.m3ph*self.f6.m3ph *
                (1-self.rej)+self.f5.m3ph *
                (self.f2.m3ph-self.f6.m3ph*(1-self.rej))
            )
            self.f3.c = self.f4.c = self.f5.c = self.f7.c = self.f8.c = cc
            self.f1.c = (cc*self.f7.m3ph + self.f0.m3ph*self.f0.c)/self.f1.m3ph
            self.f2.c = (self.f1.c*self.f1.m3ph + cc *
                         self.f8.m3ph) / self.f2.m3ph
            self.f6.c = (1-self.rej) * self.f2.c

    def set_flow_list(self):
        self.flow_list = [
            self.f0,
            self.f1,
            self.f2,
            self.f3,
            self.f4,
            self.f5,
            self.f6,
            self.f7,
            self.f8,
        ]

    @property
    def df(self):
        df = pd.DataFrame(
            [asdict(x) for x in self.flow_list]
        )
        df['ts'] = df.c * df.m3ph
        return df

    @property
    def data_record_df(self):
        return pd.DataFrame(self.data_dt)
