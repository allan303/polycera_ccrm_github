import io
import os
from docxtpl import DocxTemplate
from typing import Any
# app
from .errors import MyExceptions
from app.core.config import DOC_TPL_DEST


def get_tpl_object(tpl_name: str = 'polycera_design_scheme_tpl.docx', tpl_dir: str = None) -> DocxTemplate:
    '''
    Summary: 获得DocxTemplate对象
    '''
    '''生成doc tpl WORD文件'''
    tpl_dir = tpl_dir or DOC_TPL_DEST
    tpl = tpl_name
    tpl = os.path.join(tpl_dir, tpl)
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
    # filename = "download" if not filename else filename
    # filename = filename + '.docx'
    # word文件名称不能包含以下字符
    ls = ["?", "、", os.sep, "/", "*", "“", "”", "<", ">", "|"]
    for x in ls:
        filename = filename.replace(x, "_")
    doc.render(context)  # 渲染
    if to_file:
        filename = filename or 'unnamed'
        if not filename.endswith('.docx'):
            doc.save(f'{filename}.docx')
        else:
            doc.save(f'{filename}')
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


def to_docx_file(tpl_name: str = None,
                 tpl_dir: str = None,
                 context: Any = None,
                 filename: str = '',
                 to_file: bool = False):
    '''
    Summary: 将self 作为 context 传入word_tpl 渲染
    '''
    tpl_dir = tpl_dir or DOC_TPL_DEST
    doc = get_tpl_object(tpl_name=tpl_name, tpl_dir=tpl_dir)
    # 默认传入doc
    if isinstance(context, dict):
        context['doc'] = doc
    return to_docx(doc=doc, context=context, filename=filename, to_file=to_file)
