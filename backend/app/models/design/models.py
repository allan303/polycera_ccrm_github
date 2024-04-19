from mongoengine import StringField, DynamicField, IntField
from typing import List, Optional, Dict
import datetime
from dataclasses import asdict
# autodesign
from autodesign.projects.polycera.design import PolyceraDesign
from autodesign.designs.base_options import OptionAll
# app
from app.models.base_model import BaseDocument
from app.models.user.models import UserOrm, BaseDocumentOwner
from app.models.project.models import ProjectOrm
from app.models.oem.models import OemOrm
from app.models.design_module.schemas import DesignModuleCreatePD
from app.models.design_module.models import DesignModuleOrm
from app.models.polycera_membrane.models import PolyceraModuleOrm


class StandardDesignOrm(BaseDocumentOwner):
    '''
    Summary: 标准配置
    '''
    _classname = 'standard_design'
    _children = ''  # 将会关联到此class的类
    _father = ''  # 此类关联的class

    name = StringField(default='标准配置')
    remark = StringField(default='')
    options = DynamicField()  # 保存设计参数


class DesignOrm(BaseDocumentOwner):
    '''
    Summary: Design Model 
    // 膜元件的选择 在 前端完成
    '''
    _classname = 'design'
    _children = ''  # 将会关联到此class的类
    _father = 'project,oem'  # 此类关联的class

    version = StringField(default="V1.0")
    name = StringField(default='标准配置')
    remark = StringField(default='')
    options = DynamicField()  # 保存设计参数
    project_sid = StringField(default='')
    oem_sid = StringField(default='')
    # 自动计算
    module_name = StringField()
    module_nums = IntField(default=0)
    project_name = StringField()
    oem_name = StringField()
    design_result = DynamicField(default=dict)  # 保存设计结果 通过clean

    def set_design_result(self):
        '''
        Summary: 设计结果保存到数据库
        '''
        self.design_result = {}
        if not self.options:
            self.options = {}
            self.design_result = {}
            return None
        op_pd = OptionAll(**self.options)
        if self.module:
            self.module_name = self.module.model
            op_pd.module = DesignModuleCreatePD.from_orm(self.module)
        # 更新options
        self.options = op_pd.dict()
        ds = PolyceraDesign(options=op_pd.dict())
        self.design_result = asdict(ds)
        self.module_nums = ds.main_balance.nums_info.total.module
        # self.save()

    def clean(self):
        '''
        Summary: 保存之前
        '''
        # if not self.name:
        #     self.name = 'PolyceraDesign-'+str(datetime.date.today())
        super().clean()
        self.set_attr_by_sid(
            sid_name='project_sid',
            attr_name='project_name',
            obj_attr='name',
            orm_class=ProjectOrm
        )
        self.set_attr_by_sid(
            sid_name='oem_sid',
            attr_name='oem_name',
            obj_attr='name',
            orm_class=OemOrm
        )
        self.set_design_result()

    @property
    def dc(self) -> PolyceraDesign:
        '''
        Summary: 返回 dc 
        '''
        if not self.options:
            self.design_result = {}
            return None
        return PolyceraDesign(options=self.options)

    @property
    def module(self) -> DesignModuleOrm:
        '''
        Summary: 对应数据库中的module orm
        默认： hydro-uf-100-40-8040
        '''
        op = self.options
        dft = DesignModuleOrm.objects(
            model__iexact='hydro-uf-100-40-8040').first()
        model = ''
        if not op:
            return dft
        if not op.get('module'):
            return dft
        if not op['module'].get('model'):
            return dft
        # 必须 brand 和 model 都匹配
        model = op['module'].get('model')
        brand = op['module'].get('brand', "polycera")
        orm = DesignModuleOrm.objects(
            model__iexact=model, brand__iexact=brand).first()
        if not orm:
            return dft
        return orm

    @property
    def polycera_module(self):
        '''
        Summary: 如果采用polycera
        '''
        return PolyceraModuleOrm.objects(model__iexact=self.module_name).first()

    @classmethod
    def get_qs(cls, **kwargs):
        return super().get_qs(fuzzy_keys='owner_name,name,project_name,oem_name,remark', **kwargs)

    @classmethod
    def order_keywords_dict(cls):
        dt = super().order_keywords_dict()
        add = {
            'name': '名称',
            'oem_name': '关联客户',
            'project_name': "关联项目",
            'module_name': "膜组件",
        }
        add.update(dt)
        return add

    @classmethod
    def get_cache(cls) -> List[Dict]:
        '''
        Summary: [{sid:name}] 用于 前台 select
        NOTE： 手动缓存 改善性能
        '''
        return super().get_cache(keys=['sid', 'name', "is_deleted", "owner_sid", 'module_name'])

    def one_to_docx(self,
                    tpl_name: str = 'design_uf_sheet_fiber_jack_tpl.docx',
                    to_file: bool = False,
                    context: dict = None):
        '''
        Summary: 转换为docx
        '''
        from .schemas import DesignDownloadContextPD
        tpl_name = tpl_name or 'design_uf_sheet_fiber_jack_tpl.docx'
        context = context or {}
        # 限定context
        context = DesignDownloadContextPD(**context).dict()
        return super().one_to_docx(tpl_name=tpl_name,
                                   to_file=to_file,
                                   context=context)
