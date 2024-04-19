#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-04-23

'''
spectable
'''

from dataclasses import dataclass, field, InitVar
from typing import Any, List, Optional, Dict
import numbers
import pandas as pd
from anytree import Node, AnyNode, RenderTree, PreOrderIter
from anytree.importer import DictImporter
import os
# app
from autodesign.core.config import JSON_DEST_DESIGN_OPTION
from jackutils.json_tool import get_from_json
from autodesign.products.base_product import BaseProductMixin


@dataclass
class SpecTable:
    '''
    管理一个 List[dc] :: 可通过pid_id直接获得此设备的所有信息，便于查询
    '''
    name: str = 'Equipment List'
    table: List[BaseProductMixin] = field(default_factory=list)

    @property
    def table_dt(self):
        # List[dict]
        return [x.spec_dt for x in self.table]

    def __df_add_kw_info(self, df: pd.DataFrame) -> pd.DataFrame:
        '''
        Summary: 为df 增加kw数据
        '''
        df['kwh_per_day'] = df['kw_avg']*df['nums']*df['hpd']
        return df

    @property
    def df(self) -> pd.DataFrame:
        '''
        Summary: pandas.DataFrame
        '''
        df = pd.DataFrame(self.table_dt)
        df.sort_values('sort_id')
        return self.__df_add_kw_info(df)

    @property
    def df_useful_cols(self, cols: list = ['pid_id', 'name', 'spec', 'nums', 'nums_backup', 'nums_total']):
        return self.df[cols]

    @property
    def df_only_kw(self) -> pd.DataFrame:
        '''
        Summary: 返回 电动设备（有运行时间的）
        '''
        df = pd.DataFrame(self.sorted_dc_list_only_kw)
        return self.__df_add_kw_info(df)

    @property
    def df_groupby(self) -> pd.DataFrame:
        # 合并同类项
        df = pd.DataFrame(self.table_dt)
        cols = df.columns  # 全部col
        dcols = ['name',
                 'catalog',
                 'model',
                 'brand',
                 'spec',
                 'material',
                 'kw',
                 'kw_k',
                 'required']  # groupby判断依据 cols

        def f_join(x):
            return ','.join(x)  # 新的一列用于生成查重str

        def f_first(x):  # 取第一行
            return x.iloc[0]
        # agg_dict 定义了合并同类项时，其他不同列的行为
        agg_dict = {
            'place': f_join,  # 安装位置 合并
            'nums': 'sum',  # sum
        }
        # 剩下的cols
        other_cols = set(cols) - set(dcols) - set(agg_dict.keys())
        # 剩下的cols都取第一行
        for x in other_cols:
            agg_dict[x] = f_first
        df1 = df.groupby(by=dcols, as_index=False).agg(agg_dict)
        return __df_add_kw_info(df1)

    def add_one(self, data):
        '''
        Summary: add one Equipment (inplace)
        Note : 直接管理dc
        '''
        if data is None:
            return None
        if isinstance(data, BaseProductMixin):  # dc
            if data.nums > 0:
                self.table.append(data)
        elif isinstance(data, self.__class__):  # 自身类 另一个spectable
            self.table += data.table
        else:
            tp = str(type(data))
            raise TypeError(
                f'{tp} is Not allowed to use [SpecTable.add_one] function')

    def add(self, *args):
        '''
        Summary:  # 根据type进行连续添加
        Example:  spectable.add(valve1,valve2,...)
        '''
        for x in args:
            self.add_one(x)

    def __mul__(self, i: numbers.Number):
        # define 乘法 *
        try:
            i = float(i)
        except:
            raise TypeError(
                f'[{i}] is not a valid Number, Can not * with SpecTable')
        if i <= 0:
            raise ValueError(
                f'[{i}] is not a valid Number, Can not * with SpecTable')
        new = self.__class__()
        new.name = self.name
        new.table = [x*i for x in self.table]  # 全部乘以i,返回新的SpecTable
        return new

    def get_by_pid(self, pid: str = None):
        '''
        Summary:通过pid找到DC
        '''
        if not pid:
            return None
        ls = list(filter(lambda x: x.pid_id == pid, self.table))
        if len(ls) == 0:
            return None
        elif len(ls) == 1:
            return ls[0]
        else:
            raise Exception(f'PID ID = {pid} is duplicated {len(ls)} times')

    @property
    def sorted_dc_list(self):
        '''
        Summary: 用于doc渲染
        '''
        return sorted(self.table, key=lambda x: x.sort_id)

    @property
    def sorted_dc_list_only_kw(self):
        '''
        Summary: 用于doc渲染,仅显示有kw的类，且进行排列
        '''
        ls = []
        for x in self.table:
            if x.kw and x.hpd:
                ls.append(x)
        return sorted(ls, key=lambda x: x.sort_id)

    @property
    def kwh_per_day(self):
        '''
        Summary: 电耗
        '''
        return sum([x.kw_avg*x.hpd*x.nums for x in self.sorted_dc_list_only_kw])


# class MySpecNode:
#     '''
#     Summary: 简单的 Tree 数据结构
#     '''

#     def __init__(self,
#                  name: str = 'Node',
#                  parent: Optional['SpecNode'] = None,
#                  payload: Optional[Dict] = None
#                  ):
#         self.name = name
#         self.__parent = parent
#         self.__children = []
#         self.payload = payload or {}
#         self.set_parent_children()

#     @property
#     def children(self):
#         return self.__children

#     @children.setter
#     def children(self, children):
#         print('不能直接设置children')
#         return None

#     @property
#     def parent(self):
#         return self.__parent

#     @parent.setter
#     def parent(self, parent_node: "SpecNode"):
#         # 设置时候 进行操作
#         # 原有parent删除此节点
#         if self.__parent:
#             if self.__parent.__children:
#                 self.__parent.__children.remove(self)
#         # 新的parent 增加此节点
#         parent_node.append_child(self)
#         # 赋值
#         self.__parent = parent_node

#     def set_parent_children(self):
#         # 把自己添加到 parent.__children list 中
#         if self.parent:
#             self.parent.__children.append(self)

#     @property
#     def is_root(self):
#         if not self.parent:
#             return True
#         return False

#     @property
#     def is_leaf(self):
#         # 最终点
#         if not self.__children:
#             return True
#         return False

#     def append_child(self, node: 'SpecNode'):
#         '''
#         Summary: 增加一个节点
#         '''
#         self.__children.append(node)
#         node.__parent = self

#     # def set_parent(self, parent_node: "SpecNode"):
#     #     # 设置时候 进行操作
#     #     # 原有parent删除此节点
#     #     self.parent.__children.remove(self)
#     #     # 新的parent 增加此节点
#     #     parent_node.append_child(self)
#     #     # 赋值
#     #     self.parent = parent_node

#     @property
#     def root_node(self):
#         return get_root(self)

#     def __repr__(self):
#         parent_name = "根节点"
#         if self.__parent:
#             parent_name = self.__parent.name
#         return f'{self.name},{parent_name},{[x.__repr__() for x in self.__children]}'

#     @property
#     def parent_chain(self):
#         # 从小到大的 chain
#         ls = []
#         p = self.__parent
#         while p:
#             ls.append(p)
#             p = p.__parent
#         return ls


class SpecNode(AnyNode):  # Add Node feature
    def __init__(self,
                 payload=None,
                 is_pipe: bool = False,
                 is_tank: bool = False,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.payload = payload or {}
        self.is_pipe = is_pipe
        self.is_tank = is_tank
        # 初始化直接指定
        self.update_payload_nums_total()

    def update_payload_nums_total(self):
        '''
        Summary: 初始此node时
        '''
        if not self.payload.get('nums') or not isinstance(self.payload.get('nums'), numbers.Number):
            self.payload['nums'] = 1
        if not self.payload.get('nums_backup') or not isinstance(self.payload.get('nums_backup'), numbers.Number):
            self.payload['nums_backup'] = 0
        self.payload['nums_total'] = self.payload['nums_backup'] + \
            self.payload['nums']

    @property
    def parent_chain(self):
        # 从小到大的 chain
        ls = []
        p = self.parent
        while p:
            ls.append(p)
            p = p.parent
        return ls

    def get_mul_nums(self, key: str, default_nums=1):
        # 出现了就代表有1个，除非指定为0
        if self.payload.get(key) == 0:  # 显性指定0时候 清空
            return 0
        nums = self.payload.get(key, default_nums)
        p = self.parent
        if p:  # 返回parent nums * 自身 nums
            return p.get_mul_nums(key, default_nums) * nums
        else:  # 根节点 返回本身的值
            return nums

    @property
    def nums_total(self):
        # 总数
        return self.get_mul_nums('nums_total', 1)

    @property
    def nums(self):
        # 运行数量
        return self.get_mul_nums('nums', 1)

    @property
    def nums_backup(self):
        # 备用数量
        return self.nums_total - self.nums

    def set_all_id(self):
        '''
        Summary: 对所有Children中的id进行自动设置，按照index来
        '''
        for node in PreOrderIter(self):
            if node.children:
                i = 1
                for c in node.children:
                    c.id = str(i)
                    i += 1

    @property
    def id_full(self):
        if not self.parent:
            # root 无id
            return ''
        if self.parent.id_full:
            return f'{self.parent.id_full}.{self.id}'
        return self.id


def get_json_file_to_specnode(filename: str, dirpath: str = JSON_DEST_DESIGN_OPTION):
    '''
    Summary: 从json文件中 获取,转换为Tree
    '''
    uf_op_dt = get_from_json(filename=filename, dirpath=dirpath)
    importer = DictImporter(nodecls=SpecNode)
    root = importer.import_(uf_op_dt)
    return root


def print_or_to_file(*args, file=None):
    if not file:
        print(*args)
    else:
        print(*args, file=file)


def is_pipe_or_not(node: SpecNode, prefix: str, py: dict, data: Any):
    if node.is_pipe:
        real_s = py.get("real_s", 0)
        dn = py.get("dn", 0)
        q = py.get('q', 0)
        print_or_to_file(
            f'{prefix}  (DN{dn},{real_s:.1f}m/s,{q:.1f}m3/h)', file=data)
    else:
        print_or_to_file(
            f'{prefix}  ({py.get("nums",1)})', file=data)


def print_node(pre: str, node: SpecNode, to_file: bool = False, filename: str = None, no_leaf: bool = False):
    data = False
    if to_file:
        data = open(filename, 'a', encoding="utf-8")
    py = node.payload
    prefix = f'{pre}{node.id_full}-{node.name}'
    if node.is_root:
        print_or_to_file(node.name, file=data)
    else:
        if no_leaf:  # 不打印子节点
            if not node.is_leaf:
                is_pipe_or_not(node, prefix, py, data)
        else:
            pid = py.get("pid_id")
            if not pid:
                is_pipe_or_not(node, prefix, py, data)
            else:
                print_or_to_file(
                    f'{prefix} ({py.get("nums",1)}) pid={pid}', file=data)


def print_specnode_tree(root: SpecNode,  filename: str = 'uf_bom.txt', to_file: bool = False, no_leaf: bool = False):
    if os.path.exists(filename):
        # 已存在，则删除
        os.remove(filename)
    for pre, _, node in RenderTree(root):
        print_node(pre=pre,
                   node=node,
                   to_file=to_file,
                   filename=filename,
                   no_leaf=no_leaf)
