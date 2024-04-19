#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-02-09

'''
所有基础产品的ORM
Use mongoengine;
Use pydantic BaseModel to model the MongoDB; 
Use Pymongo to handle the DB directly 
'''


import logging
import io
import os
from datetime import datetime
from mongoengine import (StringField, FloatField,
                         ListField, DateTimeField, BooleanField,
                         queryset_manager, Document)
from bson import ObjectId
from docxtpl import DocxTemplate
from jackutils.time_tool import utc2local
# app
from autodesign.core.config import DOC_TPL_DEST


class SedDocument():
    # 数据库model 时间 mix in
    create_time = DateTimeField(default=datetime.utcnow)  # 新建时
    update_time = DateTimeField(default=datetime.utcnow)  # 新建时
    tags = ListField(StringField())  # 标签 比如 自动阀，蝶阀，气动

    # @property
    # def create_time(self):
    # 直接从ObjectID中获得时间
    #     return self.id.generation_time

    @property
    def create_time_local(self) -> datetime:
        return utc2local(self.create_time)

    @property
    def update_time_local(self) -> datetime:
        return utc2local(self.update_time)

    def save_and_reload(self):
        # save 并 重置
        self.save()
        self.reload()
        return self

    @classmethod
    def get_by_sid(cls, sid: str):
        # 根据 str objectid  找到 instance
        try:
            oid = ObjectId(sid)
        except:
            return None
        return cls.objects(id=oid).first()

    @classmethod
    def get_by_sid_or_404(cls, sid: str):
        # 根据 str objectid  找到 instance,找不到则直接raise HTTPException
        try:
            oid = ObjectId(sid)
        except:
            raise Exception(f'Not found {cls.__name__}:sid={sid}')
        obj = cls.objects(id=oid).first()
        if not obj:
            raise Exception(f'Not found {cls.__name__}:sid={sid}')
        return obj

    def clean(self):
        # 此特殊函数会在.save()之前运行
        # 也可以使用 singles进行监听 pre_save 行为（database 层面）
        self.update_time = datetime.utcnow()

    @property
    def sid(self):
        if hasattr(self, 'id'):
            return str(getattr(self, 'id'))
        return None

    @queryset_manager  # 类似于 classmethod 但是返回的是  queryset object
    def new_update_objects(doc_cls, queryset):
        # 按照 update_time 新更新的排前面
        return queryset.order_by('-update_time')

    @queryset_manager
    def old_update_objects(doc_cls, queryset):
        # 按照 update_time 老的排前面
        return queryset.order_by('+update_time')

    @queryset_manager  # 类似于 classmethod 但是返回的是  queryset object
    def new_create_objects(doc_cls, queryset):
        # 按照 create_time 新更新的排前面
        return queryset.order_by('-create_time')

    @queryset_manager
    def old_create_objects(doc_cls, queryset):
        # 按照 create_time 老的排前面
        return queryset.order_by('+create_time')

    def to_docx(self, tpl=None, context=None, user=None):
        # try:
        if not tpl:
            raise Exception('请提供TPL名称')
        tpl = os.path.join(DOC_TPL_DEST, tpl)
        # 如果没有找到TPL，则说明不提供下载功能
        if not os.path.exists(tpl):
            raise Exception('TPL NOT FOUND: {tpl}')
        # 只传入单个obj
        if not context:
            context = {
                "objs": self,
                # 可以主动传入 user  以获得用户状态
                "user": user,
                "today": datetime.utcnow().strftime("%Y-%m-%d"),
            }
        doc = DocxTemplate(tpl)  # 从模板获得
        doc.render(context)  # 渲染
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


class BaseDocumentMixin(SedDocument, Document):
    '''
    Summary: 数据库存储基本信息
    Note   : 通过 __collectionname__ 指定数据表名称
            通过 __pk__ 指定primeKey
    Example: 
    '''
    model = StringField(default='')  # 不同品牌 相同型号？
    brand = StringField(default='')  # 品牌
    standard = StringField(default='cn')
    description = StringField(default='')  # 备注
    unit = StringField(default='pcs')
    spec = StringField(default='')  # 规格，用于描述此产品
    weight_net = FloatField(default=0)   # 净重 kg
    weight_pack = FloatField(default=0)   # 包装重量 kg
    module_size = StringField(default='')  # 尺寸描述
    size_pack = StringField(default='')  # 包装尺寸
    pn = FloatField(default=10)  # 公称压力
    material = StringField(default='')  # 材料 概述
    is_outdated = BooleanField(default=False)  # 过时的，停产的
    meta = {
        'abstract': True,
    }


class BasePowerDocumentMixin(BaseDocumentMixin):
    '''
    Summary: 电动设备的基本ORM
    '''
    kw = FloatField(default=0)
    kw_k = FloatField(default=0.85)

    meta = {
        'abstract': True,
    }
