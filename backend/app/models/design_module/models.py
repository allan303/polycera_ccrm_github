from mongoengine import (
    StringField, FloatField, BooleanField, IntField, DictField
)
import os
from typing import List, Dict

from jackutils.json_tool import  save_to_json
# app
from app.core.config import STATIC_DEST
from autodesign.designs.module_for_design import ModuleForDesignPD
from app.models.base_model import BaseDesignModuleOrm


class DesignModuleOrm(BaseDesignModuleOrm):
    '''
    Summary: 用于 Design 的 基本产品信息（统一维护）？
    NOTE： 默认包含所有膜元件产品，还可以添加其他品牌产品
    '''
    _classname = 'design_module'
    _children = ''  # 将会关联到此class的类
    _father = ''  # 此类关联的class

    name = StringField(default='超滤')
    material = StringField(default='pvdf')  # 材质
    membrane_type = StringField(default='uf')
    module_type = StringField(default='卷式')
    brand = StringField(default='')
    model = StringField(required=True)
    fa = FloatField(required=True)
    is_contained_pv = BooleanField(default=False)
    flux_per_bar_25 = FloatField(default=80)
    liter_inside = FloatField(default=40)
    spacer_mil = IntField(default=40)  # 有格网
    module_size = StringField(default='8040')
    rej_dt = DictField(default=dict)
    description = StringField(default='')

    @classmethod
    def insert_modules(cls, orm_cls_list: List, delete_all: bool = False, filter_dt_and: dict = None):
        '''
        Summary: 添加 标准膜元件产品
                不同的 Module数据库 拿来直接添加
        '''
        if delete_all:
            cls.objects().delete()
        if not filter_dt_and:
            filter_dt_and = {'is_deleted': False, 'module_size__gte': 4040}
        for orm in orm_cls_list:
            objs = orm.get_qs(filter_dt_and=filter_dt_and)
            for obj in objs:
                pd = ModuleForDesignPD.from_orm(obj)
                # 不添加重复： brand&model一致
                curr = cls.objects(brand=pd.brand, model=pd.model).first()
                if not curr:
                    new = cls(**pd.dict())
                    new.description = obj.description_cn
                    new.save()

    @classmethod
    def save_to_json(cls, filename: str = 'design_module'):
        '''
        Summary: 目前的product 保存到Json
        '''
        dt = [ModuleForDesignPD.from_orm(x).dict() for x in cls.objects.all()]
        path = os.path.join(STATIC_DEST, 'products')
        save_to_json(data=dt, filename=filename, dirpath=path)

    @classmethod
    def get_cache(cls) -> List[Dict]:
        '''
        Summary: [{sid:name}] 用于 前台 select
        NOTE： 手动缓存 改善性能
        '''
        return super().get_cache(keys=['sid', 'name', 'model', 'module_type', 'brand', "description", 'fa', 'is_contained_pv'])

    @classmethod
    def get_qs(cls, **kwargs):
        return super().get_qs(fuzzy_keys='name,model,description,module_type,brand', **kwargs)

    @classmethod
    def order_keywords_dict(cls):
        dt = super().order_keywords_dict()
        add = {
            'name': '名称',
            'model': '型号',
            'brand': '品牌',
            'module_type': '类型',
        }
        add.update(dt)
        return add

    def clean(self):
        super().clean()
        if self.brand:
            self.brand = str(self.brand).capitalize()
