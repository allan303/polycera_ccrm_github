#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2021-06-08

'''
Summary: excel file
'''
import os
import pandas as pd


def get_from_excel(filename: str, dirpath: str) -> pd.DataFrame:
    '''
    Summary: 从json文件中获得默认chem data
    NOTE : open 的 'r' 只读模式必须判断是否存在文件
    '''
    file = f'{filename}'
    file_path = os.path.join(dirpath, file)
    if not os.path.exists(file_path):
        print(f'{file} 不存在')
        return None
    return pd.read_excel(file_path)
