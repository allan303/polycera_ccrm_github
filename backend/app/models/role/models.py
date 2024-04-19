from mongoengine import (
    StringField, BooleanField, FloatField, IntField, ListField, DictField
)
from typing import Dict, List
from jackutils.json_tool import get_from_json, save_to_json
# app
from app.models.base_model import BaseDocument
from app.core.config import DEFAULT_PERMISSIONS_DEST
from app.core.errors import MyExceptions
from .schemas import RoleCreatePD, RoleEditPD


'''
默认 角色 权限
'''
# superadmin
default_role_names = ['su', 'admin', 'sales_manager',
                      'sales', 'tech', 'tech_manager', 'finance', 'order', 'hr']


class RoleOrm(BaseDocument):
    '''
    角色, 与UserOrm为one-to-many
    '''
    _classname = 'role'
    _children = 'user'  # 将会关联到此class的类
    _father = ''  # 此类关联的class

    name = StringField(required=True, unique=True)  # 以name 作为 PK
    remark = StringField(default='')
    perm = DictField(default=dict)

    @classmethod
    def init_model(cls):
        '''
        Summary: 初始化
        '''
        cls.objects.delete()
        for x in default_role_names:
            perm = get_from_json(x, DEFAULT_PERMISSIONS_DEST)
            role = cls(name=x, perm=perm)
            role.save()

    @classmethod
    def update_permission_from_json(cls):
        '''
        Summary: 从 json 文件 更新 权限
        '''
        for x in cls.objects.all():
            perm = get_from_json(x.name, DEFAULT_PERMISSIONS_DEST)
            x.perm = perm
            x.save()

    @classmethod
    def save_perms_to_json(cls):
        '''
        Summary: 当前数据库中的 权限保存到 json 中
        '''
        for x in cls.objects.all():
            save_to_json(data=x.perm, filename=x.name,
                         dirpath=DEFAULT_PERMISSIONS_DEST)
            print(f'保存{x.name}到JSON成功')

    @classmethod
    def get_cache(cls) -> List[Dict]:
        '''
        Summary: [{sid:name}] 用于 前台 select
        NOTE： 手动缓存 改善性能
        '''
        return super().get_cache(keys=['sid', 'name', "is_deleted", "remark"])

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

    @classmethod
    def su(cls):
        # SU role
        return cls.objects(name='su').first()

    @classmethod
    def create_by_pd(cls, pd: RoleCreatePD, **kwargs):
        if str(pd.name).strip().lower() == 'su':
            raise MyExceptions.permission_deny
        # 验证name 重复
        name = pd.name
        if cls.objects(name=name).first():
            raise MyExceptions.role_already_exist
        return cls(**pd.dict())

    def edit_by_pd(self,  pd: RoleEditPD):
        '''
        Summary: 根据pd，edit
        '''
        if self.name == 'su':
            raise MyExceptions.su_not_allowed_edit
        # 不能编辑name
        self.update(**pd.dict())
        return self
