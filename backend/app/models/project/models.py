from mongoengine import (
    StringField, IntField, BooleanField, DateField, FloatField
)
import datetime
from typing import List, Optional
import numbers
# app
from app.core.jwt import MyExceptions
from app.models.user.models import BaseDocumentOwner
# from app.models.pilot.models import PilotOrm
from app.models.config.models import create_default_config
from app.models.oem.models import OemOrm
from app.models.config.models import ConfigOrm
from .schemas import ProjectUpdateCreatePD, ProjectOemCreatePD, ProjectManyToExcelPD


class ProjectUpdateOrm(BaseDocumentOwner):
    '''
    Summary: 项目状态更新，支持 delete，add，read，不能edit
    '''
    _classname = 'project_update'
    _children = ''  # 将会关联到此class的类
    _father = 'project'  # 此类关联的class

    project_sid = StringField(required=True)
    pjstage = StringField(default='')  # 项目阶段
    win_percentage = IntField(default=None)  # 成功率权重
    forecast_date = DateField(default=None)
    remark = StringField(default='')

    def switch_delete(self):
        '''
        Summary: 假删除 切换
        '''
        pj = ProjectOrm.get_by_sid(self.project_sid)
        self.is_deleted = not self.is_deleted
        self.deleted_time = datetime.datetime.utcnow()
        self.save()
        new = ProjectUpdateOrm.objects(
            project_sid=pj.sid, id__ne=self.id, is_deleted=False).order_by('-create_time').first()
        if new:
            # 回滚
            pj.pjstage = new.pjstage
            pj.win_percentage = new.win_percentage
            pj.forecast_date = new.forecast_date
            pj.save()
        else:
            pj.pjstage = None
            pj.win_percentage = None
            pj.forecast_date = None
            pj.save()
        return self

    def clean(self):
        '''
        Summary: 保存前的中间函数
        '''
        super().clean()
        pjstage_list = ConfigOrm.objects().first().pjstage
        # pjstage : win_percentage 关联
        for x in pjstage_list:
            if self.pjstage == x['name']:
                if not isinstance(self.win_percentage, numbers.Number):
                    # 如果没有，则自动关联
                    self.win_percentage = x['win_percentage']
                # 如果已有，强制关联一部分
                if x['win_percentage'] in [0, 100]:
                    self.win_percentage = x['win_percentage']
        # 更新 项目信息
        pj: ProjectOrm = ProjectOrm.get_by_sid(sid=self.project_sid)
        if not pj:
            return None
        pj.pjstage = self.pjstage
        pj.win_percentage = self.win_percentage or 10
        pj.forecast_date = self.forecast_date
        pj.forecast_amount_cal = pj.forecast_amount * pj.win_percentage / 100
        pj.save()

    @classmethod
    def order_keywords_dict(cls):
        dt = super().order_keywords_dict()
        add = {
            'win_percentage': "成功率",
            'pjstage': "项目阶段",
            'forecast_date': "预计时间"
        }
        add.update(dt)
        return add

    @classmethod
    def get_qs(cls, **kwargs):
        return super().get_qs(fuzzy_keys='owner_name,remark,pjstage', **kwargs)

    @property
    def project(self):
        return ProjectOrm.get_by_sid(self.project_sid)


class ProjectOemOrm(BaseDocumentOwner):
    '''
    Summary: 项目下的OEM
    '''
    _classname = 'project_oem'
    _children = ''  # 将会关联到此class的类
    _father = 'project,oem'  # 此类关联的class

    project_sid = StringField(required=True)
    oem_sid = StringField(required=True)
    is_filing = BooleanField(default=False)  # 备案与否
    remark = StringField(default='')  # 备案内容

    @staticmethod
    def validate_data(project_sid: str, oem_sid: str):
        '''
        Summary:  保存之前 验证 email 或 phone 是否重复
        '''
        c = ProjectOemOrm.objects(
            project_sid=project_sid, oem_sid=oem_sid).first()
        if c:
            raise MyExceptions.project_oem_already_exist

    @classmethod
    def create_by_pd(cls, pd: ProjectOemCreatePD, **kwargs):
        '''
        Summary: 根据pd，create
        '''
        # 验证是否重复
        cls.validate_data(project_sid=pd.project_sid, oem_sid=pd.oem_sid)
        return cls(**pd.dict())

    def edit_by_pd(self,  pd: ProjectOemCreatePD):
        '''
        Summary: 根据pd，edit
        '''
        if not pd.project_sid == self.project_sid or not pd.oem_sid == self.oem_sid:
            '''
            Summary: 其中有一项不同，则验证
            '''
            self.validate_data(project_sid=pd.project_sid, oem_sid=pd.oem_sid)
        self.update(**pd.dict())
        return self

    @classmethod
    def order_keywords_dict(cls):
        dt = super().order_keywords_dict()
        add = {
            'is_filing': "备案状态"
        }
        add.update(dt)
        return add

    @classmethod
    def get_qs(cls, **kwargs):
        return super().get_qs(fuzzy_keys='owner_name,remark', **kwargs)

    @property
    def project(self):
        return ProjectOrm.get_by_sid(self.project_sid)

    @property
    def oem(self):
        return OemOrm.get_by_sid(self.oem_sid)


class ProjectOrm(BaseDocumentOwner):
    '''
    Summary: Project，核心 model
    NOTE:
        1) 将 设计信息，如 q、wwtype、design_lmh、module_name 等放到 DesignOrm中
        2) 将 客户信息，如 oem_sid,  等信息，放到 ProjectOemOrm中 
    '''
    _classname = 'project'
    _children = 'project_update,project_oem,post,design'  # 将会关联到此class的类
    _father = ''  # 此类关联的class

    name = StringField(default='', unique=True)
    location = StringField(default='')  # 地区
    industry = StringField(default='')  # 行业
    pjtype = StringField(default='')  # 新建
    source = StringField(default='')  # 来源
    # 按照时间更新状态：只能read不能编辑、删除，可增加
    remark = StringField(default='')
    forecast_amount = FloatField(default=0)  # 预期销售额
    module = StringField(default='')
    module_nums = IntField(default=0)
    # auto
    pjstage = StringField(default='线索')  # 项目阶段
    win_percentage = IntField(default=10)  # 成功率权重
    forecast_date = DateField(default=None)
    forecast_amount_cal = FloatField(default=0)  # 预期销售额

    @classmethod
    def get_qs(cls, **kwargs):
        return super().get_qs(fuzzy_keys='owner_name,name,location,industry,pjtype,source,remark', **kwargs)

    @classmethod
    def order_keywords_dict(cls):
        dt = super().order_keywords_dict()
        add = {
            'name': '名称',
            'location': '地区',
            'industry': '行业',
            'pjtype': '类型',
            'source': "来源",
            'win_percentage': "成功率",
            'pjstage': "项目阶段"
        }
        add.update(dt)
        return add

    # def clean(self):
    #     pj: ProjectUpdateOrm = ProjectUpdateOrm.objects(
    #         is_deleted=False).order_by('-update_time').first()
    #     if pj:
    #         self.pjstage = pj.pjstage
    #         self.win_percentage = pj.win_percentage
    #     super().clean()

    def api_hook_create_after_save(self):
        '''
        Summary: API CREAT save 之后
        '''
        pju: ProjectUpdateCreatePD = ProjectUpdateCreatePD.from_orm(self)
        pju.project_sid = self.sid
        pju.remark = ""
        ProjectUpdateOrm(**pju.dict(), owner_sid=self.owner_sid).save()

    @property
    def project_oems(self):
        '''
        Summary: 参与用户
        '''
        from app.models.utils import get_children
        return get_children(self, 'project_oem', order_by='create_time')

    @property
    def project_updates(self):
        '''
        Summary: 更新
        '''
        from app.models.utils import get_children
        return get_children(self, 'project_update', order_by='-create_time')

    @property
    def posts(self):
        '''
        Summary: 更新
        '''
        from app.models.utils import get_children
        return get_children(self, 'post', order_by='-create_time')

    @property
    def filing_oem(self) -> ProjectOemOrm:
        '''
        Summary: 备案的公司
        '''
        return ProjectOemOrm.objects(project_sid=self.sid, is_filing=True).first()

    @property
    def filing_summary(self):
        '''
        Summary: 备案公司名称
        '''
        if not self.filing_oem:
            return ''
        foem = self.filing_oem
        return f'[{foem.owner.name}] {foem.create_date_local_str}, {foem.oem.name}'

    def one_to_docx(self, tpl_name: str = 'project_tpl.docx', to_file: bool = False, context: dict = None):
        '''
        Summary: 转换为docx
        '''
        tpl_name = tpl_name or 'project_tpl.docx'
        return super().one_to_docx(tpl_name=tpl_name,
                                   to_file=to_file,
                                   context=context)

    @classmethod
    def many_to_docx(cls,
                     qs: "QuerySet",
                     tpl_name: str = 'projects_tpl.docx',
                     to_file: bool = False,
                     context: dict = None):
        '''
        Summary: QuerySet 报表to_docx
        '''
        tpl_name = tpl_name or 'projects_tpl.docx'
        return super().many_to_docx(qs=qs,
                                    tpl_name=tpl_name,
                                    filename='项目报表',
                                    to_file=to_file,
                                    context=context)

    @classmethod
    def many_to_excel(cls, qs: "QuerySet",
                      pd_class: 'BaseModel' = None,
                      title: str = None,
                      description: str = None,
                      to_file: bool = False):
        return super().many_to_excel(qs=qs,
                                     pd_class=ProjectManyToExcelPD,
                                     title=title,
                                     description=description,
                                     to_file=to_file)
