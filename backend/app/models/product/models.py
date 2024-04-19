from mongoengine import (
    StringField, FloatField, BooleanField
)
import os
from jackutils.json_tool import get_from_json, save_to_json
from typing import List, Dict
# app
from app.models.base_model import BaseDocument
from app.models.design_module.models import DesignModuleOrm
from app.models.polycera_membrane.models import PolyceraModuleOrm
from app.core.config import STATIC_DEST
from .schemas import ProductCreatePD


class ProductOrm(BaseDocument):
    '''
    Summary: 用于订单 的产品
    NOTE： 默认包含所有膜元件产品，还可以添加其他
    '''
    _classname = 'product'
    _children = ''  # 将会关联到此class的类
    _father = ''  # 此类关联的class

    name = StringField(required=True)
    brand = StringField(default='')
    model = StringField()  # 型号
    description = StringField(default='')
    unit_price = FloatField(default=0)
    unit = StringField(default='支')
    remark = StringField(default='')

    @classmethod
    def insert_membrane_product(cls):
        '''
        Summary: 添加 标准膜元件产品 + 1812产品
        '''
        for x in PolyceraModuleOrm.objects().all():
            curr = cls.objects.filter(
                model__iexact=x.model, brand__iexact=x.brand).first()
            # 已存在同名的则不添加
            if not curr:
                pd = ProductCreatePD.from_orm(x)
                pd.description = x.description_cn
                print('新增产品', pd.model)
                cls(**pd.dict()).save()

    @classmethod
    def insert_other_products(cls):
        '''
        Summary: 插入 试验机产品
        '''
        ls = [
            {
                'name': '小型超滤1812实验机',
                'model': 'PS-1801',
                'description': '超滤1812实验机,包含2支1812超滤膜元件',
                'unit_price': 2900,
                'unit': '套'
            },
            {
                'name': '小型纳滤1812实验机',
                'model': 'PS-1802',
                'description': '纳滤1812实验机,包含2支1812纳滤膜元件',
                'unit_price': 3900,
                'unit': '套'
            },
            {
                'name': '运费',
                'model': '-',
                'description': '运费',
                'unit_price': 0,
                'unit': '-'
            },
            {
                'name': '税费',
                'model': '-',
                'description': '增值税',
                'unit_price': 0,
                'unit': '-'
            },
        ]
        for x in ls:
            pd = ProductCreatePD(**x)
            cls(**pd.dict()).save()

    @classmethod
    def save_to_json(cls, filename: str = 'products'):
        '''
        Summary: 目前的product 保存到Json
        '''
        dt = [ProductCreatePD.from_orm(x).dict() for x in cls.objects.all()]
        path = os.path.join(STATIC_DEST, 'products')
        save_to_json(data=dt, filename=filename, dirpath=path)

    @classmethod
    def init_model(cls, use_json: bool = False):
        '''
        Summary: 
        如果use_json，则查询 STATIC/products/products.json，否则重置
        '''
        cls.objects().delete()
        if use_json:
            path = os.path.join(STATIC_DEST, 'products')
            js = get_from_json(filename='products', dirpath=path)
            if js:
                for dt in js:
                    cls(
                        **ProductCreatePD(**dt).dict()
                    ).save()
                print('成功从Json重置ProductOrm')
                return None
            else:
                print('未找到json 文件')
        cls.insert_membrane_product()
        print('成功加入膜产品')
        cls.insert_other_products()
        print('成功加入其它产品')

    @classmethod
    def get_cache(cls) -> List[Dict]:
        '''
        Summary: [{sid:name}] 用于 前台 select
        NOTE： 手动缓存 改善性能
        '''
        return super().get_cache(keys=['sid', 'name', 'model', "description", "unit", "unit_price"])

    @classmethod
    def get_qs(cls, **kwargs):
        return super().get_qs(fuzzy_keys='name,model,description,remark', **kwargs)

    @classmethod
    def order_keywords_dict(cls):
        dt = super().order_keywords_dict()
        add = {
            'name': '名称',
            'model': '型号',
            'unit': '计量单位',
        }
        add.update(dt)
        return add
