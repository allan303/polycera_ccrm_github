from mongoengine import StringField, DateField
import datetime
# app
from app.models.user.models import BaseDocumentOwner
from app.models.oem.models import OemOrm
from app.models.project.models import ProjectOrm


class PilotOrm(BaseDocumentOwner):
    '''
    Summary: 中试
    '''
    _classname = 'pilot'
    _children = 'post'  # 将会关联到此class的类
    _father = 'project,oem'  # 此类关联的class

    name = StringField(default='')  # 针对项目
    project_sid = StringField(default='')  # 针对项目
    oem_sid = StringField(required=True)  # 针对客户
    location = StringField(default='')  # 地区
    industry = StringField(default='')  # 地区
    wwtype = StringField(default="")
    start = DateField(default=None)
    end = DateField(default=None)
    remark = StringField(default='')
    # AUTO
    project_name = StringField()
    oem_name = StringField()

    @property
    def oem(self):
        '''
        Summary: 客户信息
        '''
        return OemOrm.get_by_sid(self.oem_sid) or {}

    @property
    def project(self):
        '''
        Summary: 项目
        '''
        return ProjectOrm.get_by_sid(self.project_sid) or {}

    def clean(self):
        super().clean()
        self.set_attr_by_sid(sid_name='project_sid',
                             attr_name='project_name',
                             obj_attr='name',
                             orm_class=ProjectOrm)
        self.set_attr_by_sid(sid_name='oem_sid',
                             attr_name='oem_name',
                             obj_attr='name',
                             orm_class=OemOrm)

    @classmethod
    def get_qs(cls, **kwargs):
        return super().get_qs(fuzzy_keys='owner_name,name,project_name,oem_name,location,industry,remark', **kwargs)

    @classmethod
    def order_keywords_dict(cls):
        dt = super().order_keywords_dict()
        add = {
            'name': '名称',
            'project_name': '关联项目',
            'oem_name': "关联客户",
            'location': "地区",
            'industry': "行业",
        }
        add.update(dt)
        return add
