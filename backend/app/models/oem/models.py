from mongoengine import StringField
from typing import List, Optional, Dict
# app
from app.models.user.models import BaseDocumentOwner


class OemOrm(BaseDocumentOwner):
    _classname = 'oem'
    _children = 'post,contact,project_oem,design'  # 将会关联到此class的类
    _father = ''  # 此类关联的class

    name = StringField(required=True, unique=True)
    location = StringField(default='')
    oemtype = StringField(default='')
    # 开票信息
    company_code = StringField(default='')  # 税号
    company_address = StringField(default='')  # 开票地址
    company_bank = StringField(default='')  # 银行
    company_bank_account = StringField(default='')  # 银行账户
    company_telephone = StringField(default='')  # 电话
    company_zipcode = StringField(default='')  # 邮编
    # 通讯地址
    remark = StringField(default='')  # 备注

    @classmethod
    def get_cache(cls) -> List[Dict]:
        '''
        Summary: [{sid:name}] 用于 前台 select
        NOTE： 手动缓存 改善性能
        '''
        return super().get_cache(keys=['sid', 'name', "is_deleted", "oemtype", "owner_sid"])

    @classmethod
    def get_qs(cls, **kwargs):
        return super().get_qs(fuzzy_keys='owner_name,name,location,company_code,oemtype,company_zipcode,company_telephone,company_bank,remark', **kwargs)

    @classmethod
    def order_keywords_dict(cls):
        dt = super().order_keywords_dict()
        add = {
            'name': '名称',
            'oemtype': '客户类型',
            'company_zipcode': "邮编",
        }
        add.update(dt)
        return add
