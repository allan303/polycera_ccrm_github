#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2021-05-28

'''
Summary: 排列  如 (14:5)等
'''
from dataclasses import dataclass, field
from typing import List
import copy
from jackutils.list_tool import gcd_many

'''
Summary: 排序
'''


def assign_2_k(k_list: List[int], n: int) -> List[int]:
    '''
    Summary: 采用递归方式，仅考虑2个数值的比例分配问题

        按照k_list提供的比例，如[2,1]，将正整数n尽量接近分割成 正整数 [n0,n1,n2...]
        如， n=19,k_list=[2,1], ==> [13,6]
    '''
    if len(k_list) <= 1:
        return [n]
    if len(k_list) == 2:
        # 主要计算逻辑
        unit_num = n/sum(k_list)  # 单位值
        int_list = [int(x*unit_num) for x in k_list]
        remain = n - sum(int_list)  # 只有0|1
        if remain == 0:
            return int_list
        else:
            # 1:1情况，加前面
            if k_list[0] == k_list[1]:
                return ([int_list[0]+1, int_list[1]])
            portion = k_list[0]/k_list[1]  # 目标比例
            # 判定哪一种更加接近
            d1 = abs((int_list[0]+1)/int_list[1]-portion)
            d2 = abs(int_list[0]/(int_list[1]+1)-portion)
            if d1 > d2:  # d2是正确的
                return ([int_list[0], int_list[1]+1])
            else:
                return ([int_list[0]+1, int_list[1]])
    else:
        raise ValueError('k_list 长度>2')


@dataclass
class Arrange():
    '''
    Summary: 总计数量int, 按照提供的比例，如2:1:1 尽量按比例分配
        --> nums= 19 , k_list = [2:1] --> result = [13:6]
    '''
    k_list: List[int] = field(default_factory=list)
    # parent
    nums: int = 1
    # 结果/计算
    result: List[int] = field(default_factory=list)

    def __post_init__(self):
        self.cal()

    def cal(self):
        ks = copy.copy(self.k_list)  # 复制[2,1,1]
        gcd = gcd_many(ks)
        if gcd > 1:
            ks = [x/gcd for x in ks]
        while sum(ks) > self.nums:
            ks.pop()
        if len(ks) <= 2:
            self.result = assign_2_k(k_list=ks, n=self.nums)
            return None
        ls = []
        n = self.nums
        while len(ks):
            k1 = ks.pop(0)
            k2 = sum(ks)
            n1 = assign_2_k(k_list=[k1, k2], n=n)[0]
            ls.append(n1)
            n -= n1
        self.result = ls

    @property
    def summary(self) -> str:
        '''
        Summary:  [6,5,2] --> '6:5:2'
        '''
        return ':'.join([str(x) for x in self.result])
