#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-11-05
'''
根据要求生成 docx
'''
import os
import io
from docxtpl import DocxTemplate
from typing import Any
from .config import DOC_TPL_DEST


def get_tpl_object(tpl_name: str = 'polycera_design_scheme_tpl', tpl_dir: str = None) -> DocxTemplate:
    '''
    Summary: 获得DocxTemplate对象
    '''
    '''生成doc tpl WORD文件'''
    tpl_dir = tpl_dir or DOC_TPL_DEST
    tpl = os.path.join(tpl_dir, tpl_name)
    if not os.path.exists(tpl) or not tpl_name:
        raise FileNotFoundError(f'没有找到{tpl}模板')
    return DocxTemplate(tpl)  # 从模板获得


def to_docx(doc: DocxTemplate = None,
            context: Any = None,
            filename: str = '',
            to_file: bool = False):
    '''
    Summary: 将self 作为 context 传入word_tpl 渲染
    '''
    # try:
    if not doc:
        raise ValueError('必须传入doc tpl 对象')
    doc.render(context)  # 渲染
    if to_file:
        filename = filename or 'unnamed'
        doc.save(f'{filename}.docx')
        return None
    path2 = io.BytesIO()  # 内存中的位置
    doc.save(path2)  # 保存到内存中
    path2.flush()
    path2.seek(0)
    # response = StreamingResponse(content=path2)
    # # 防止中文名导致问题
    # response.headers["Content-Disposition"] = "attachment; filename={}".format(
    #     filename.encode().decode("latin-1")
    # )
    # return response
    return path2
