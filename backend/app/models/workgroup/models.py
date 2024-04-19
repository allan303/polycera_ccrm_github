from mongoengine import  StringField
from typing import List, Dict

# app
from app.models.base_model import BaseDocument


'''
默认 角色 权限
'''
# superadmin


class WorkgroupOrm(BaseDocument):
    '''
    工作组，用于区分不同公司成员权限范围，主要是list query 时候
    '''
    _classname = 'workgroup'
    _children = 'user'  # 将会关联到此class的类
    _father = ''  # 此类关联的class

    name = StringField(required=True, unique=True)  # 以name 作为 PK
    remark = StringField(default='')

    @classmethod
    def init_model(cls):
        '''
        Summary: 初始化
        '''
        cls.objects.delete()
        default_names = ['polycera']
        for x in default_names:
            cls(name=x, remark=x).save()

    @classmethod
    def get_cache(cls) -> List[Dict]:
        '''
        Summary: [{sid:name}] 用于 前台 select
        NOTE： 手动缓存 改善性能
        '''
        ls = [{'sid': 'all', 'name': 'all',
               'is_deleted': False, 'remark': '全局'}]
        dt = super().get_cache(keys=['sid', 'name', "is_deleted", "remark"])
        ls = ls + dt
        return ls

    @classmethod
    def get_qs(cls, **kwargs):
        return super().get_qs(fuzzy_keys='name,remark', **kwargs)

    @classmethod
    def order_keywords_dict(cls):
        dt = super().order_keywords_dict()
        add = {
            'name': '名称',
        }
        add.update(dt)
        return add
