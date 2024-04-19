from pydantic import BaseModel
import os
import datetime
from typing import Optional, List, Union, Dict
from bson import ObjectId
from mongoengine import (
    Document, queryset_manager,
    BooleanField, FloatField, IntField, DictField,
    # signals,
    DateTimeField,
    StringField
)
from mongoengine.queryset.visitor import Q, QCombination
import json

from jackutils.time_tool import utc2local
# app
from app.core.mongodb_utils import  mongoengine_handle_filter_dt
from app.core.errors import MyExceptions
from app.core.config import DOC_TPL_DEST
from app.core.docx import to_docx_file
from app.core.excel import pd_to_wb, wb_to_xlsx_file


class BaseDocumentNoAttr(Document):
    '''
    Summary: 基础document,无is_deleted,name
    '''
    _classname = 'BaseDocumentNoAttr'
    _children = ''  # 将会关联到此class的类
    _father = ''  # 此类关联的class

    update_time = DateTimeField(default=datetime.datetime.utcnow)  # 新建时
    create_time = DateTimeField(default=datetime.datetime.utcnow)  # 新建时

    meta = {
        'abstract': True,
    }

    def api_hook_before_save(self): ...
    def api_hook_after_save(self): ...
    def api_hook_create_before_save(self): ...
    def api_hook_create_after_save(self): ...
    def api_hook_edit_before_save(self): ...
    def api_hook_edit_after_save(self): ...
    def api_hook_before_delete(self): ...

    @property
    def create_time_local(self):
        return utc2local(self.create_time)

    @property
    def create_date_local_str(self) -> str:
        return self.create_time_local.strftime('%Y-%m-%d')

    @property
    def update_time_local(self):
        return utc2local(self.update_time)

    @property
    def update_date_local_str(self) -> str:
        return self.update_time_local.strftime('%Y-%m-%d')

    def to_dict(self):
        '''
        Summary: 返回 dict
        '''
        return json.loads(self.to_json())

    def save_and_reload(self, clean: bool = False):
        # save 并 重置
        self.save(clean=clean)
        self.reload()
        return self

    # @classmethod
    @queryset_manager
    def get_qs(doc_cls,
               queryset,
               filter_dt_and: dict = None,  # and关系
               filter_dt_or: dict = None,  # or关系
               order_by: Union[list, str] = "-create_time",
               recent_days: int = 0,
               start: Union[datetime.datetime, str] = None,  # 包含start and end
               end: Union[datetime.datetime, str] = None,
               fuzzy_keys: str = None,  # 模糊, 'name,description'
               keyword: str = '',
               use_workgroup: bool = False,
               workgroup_sid: str = None,
               owner_sid: str = None):
        '''
        Summary: 各种条件筛选
        '''
        # 存在的 fields
        fields = doc_cls.__dict__['_fields_ordered']
        # 日期筛选
        if recent_days or start or end:
            qs = doc_cls.filter_by_date(recent_days=recent_days,
                                        start=start,
                                        end=end)
        else:
            qs = doc_cls.objects()
        # and关系 query
        filter_dt_and = mongoengine_handle_filter_dt(
            filter_dt=filter_dt_and, fields=fields)
        qs = qs.filter(**filter_dt_and)
        #  or 的关系query
        filter_dt_or = mongoengine_handle_filter_dt(
            filter_dt=filter_dt_or, fields=fields)
        # 模糊查询fuzzy
        if keyword is None:
            ...
        else:
            keyword = str(keyword).strip()
        if fuzzy_keys and keyword:
            dt = {f'{k}__icontains': keyword for k in fuzzy_keys.split(',')}
            filter_dt_or.update(dt)
        # QCombination OR 关系
        queries = [Q(**{k: v}) for k, v in filter_dt_or.items()]
        query = QCombination(QCombination.OR, queries)
        qs = qs.filter(query)
        if order_by:
            if isinstance(order_by, str):
                qs = qs.order_by(order_by)
            elif isinstance(order_by, list):
                qs = qs.order_by(*order_by)
        if use_workgroup and hasattr(doc_cls, 'workgroup_sid'):
            if workgroup_sid == 'all':
                return qs
            qs = qs.filter(workgroup_sid=workgroup_sid)
        return qs

    @classmethod
    def get_by_sid(cls, sid: str) -> 'BaseDocumentNoAttr':
        # 根据 str objectid  找到 instance
        try:
            oid = ObjectId(sid)
        except Exception:
            return None
        return cls.objects(id=oid).first()

    @classmethod
    def get_by_sid_or_404(cls, sid: str) -> 'BaseDocumentNoAttr':
        # 根据 str objectid  找到 instance,找不到则直接raise HTTPException
        obj = cls.get_by_sid(sid=sid)
        if not obj:
            raise MyExceptions.not_found
        return obj

    def clean(self):
        '''
        NOTE
        # 此特殊函数会在.save()之前运行
        # 也可以使用 singles进行监听 pre_save 行为（database 层面）
        NOTE: 使用 update函数时候 不会触发
        '''
        # 必须要 reload 才行,不然 @property 会采用原有的缓存
        self.save_and_reload(clean=False)
        self.update_time = datetime.datetime.utcnow()

    @property
    def sid(self):
        if hasattr(self, 'id'):
            return str(getattr(self, 'id'))
        return None

    @queryset_manager
    def filter_by_date(doc_cls,
                       queryset,
                       recent_days: int = 0,
                       start: Union[datetime.datetime,
                                    str] = None,  # 包含start and end
                       end: Union[datetime.datetime, str] = None):
        qs = queryset
        if recent_days:
            # 优先参数,只有recent_days为空 才考察start、end
            td = datetime.timedelta(days=recent_days)
            dt = datetime.datetime.today()-td  # 限制的日期
            qs = qs.filter(create_time__gte=dt)
        else:  # 至少有其中一个参数
            if start:
                if isinstance(start, datetime.datetime) or isinstance(start, datetime.date):
                    qs = qs.filter(create_time__gte=start)
                elif isinstance(start, str):
                    try:
                        start = datetime.datetime.strptime(start, "%Y-%m-%d")
                        qs = qs.filter(create_time__gte=start)
                    except Exception:
                        ...
            if end:
                if isinstance(end, datetime.datetime) or isinstance(end, datetime.date):
                    qs = qs.filter(create_time__lte=end)
                try:
                    end = datetime.datetime.strptime(end, "%Y-%m-%d")
                    qs = qs.filter(create_time__lte=end)
                except Exception:
                    ...
        return qs

    def one_to_docx(self,
                    tpl_name: str = None,
                    filename: str = None,
                    to_file: bool = False,
                    context: dict = None):
        '''
        Summary: 单个instance转换为docx
        '''
        if not tpl_name:
            raise MyExceptions.tpl_not_found
        tpl = os.path.join(DOC_TPL_DEST, tpl_name)
        # 如果没有找到TPL,则说明不提供下载功能
        if not os.path.exists(tpl):
            raise MyExceptions.tpl_not_found
        today = datetime.datetime.today().strftime("%Y-%m-%d")
        context = context or {}
        context['ins'] = self
        context['today'] = today
        return to_docx_file(tpl_name=tpl_name,
                            filename=f'{today}_{filename or self.name}',
                            context=context,
                            to_file=to_file)

    @classmethod
    def many_to_docx(cls,
                     qs: "QuerySet",
                     tpl_name: str = None,
                     filename: str = None,
                     context: dict = None,
                     to_file: bool = False):
        '''
        Summary: QuerySet 报表to_docx
        '''
        # 验证tpl
        if not tpl_name:
            raise MyExceptions.tpl_not_found
        tpl = os.path.join(DOC_TPL_DEST, tpl_name)
        if not os.path.exists(tpl):
            raise MyExceptions.tpl_not_found
        today = datetime.datetime.today().strftime("%Y-%m-%d")
        # context update
        context = context or {}
        context['qs'] = qs
        context['today'] = today
        return to_docx_file(tpl_name=tpl_name,
                            context=context,
                            filename=f'{today}_{filename or "LIST"}',
                            to_file=to_file)

    @classmethod
    def many_to_excel(cls,
                      qs: "QuerySet",
                      pd_class: BaseModel,
                      title: str = None,
                      description: str = None,
                      to_file: bool = False):
        wb = pd_to_wb(pd_class=pd_class, data=qs,
                      title=title, description=description)
        return wb_to_xlsx_file(wb=wb, to_file=to_file)

    def clone(self):
        '''
        Summary: 克隆自身,去掉_id,update_time 重新保存
        '''
        try:
            dt = self.to_dict()
            del dt['_id']
            if '_cls' in dt:
                del dt['_cls']
            # del dt['create_time']
            if 'update_time' in dt:
                del dt['update_time']
            if 'name' in dt:
                dt['name'] = dt['name'] + '(clone)'
            # del dt['is_deleted']
            new = self.__class__(**dt)
            new.save()
            return new
        except Exception as e:
            raise e

    @classmethod
    def get_cache(cls,
                  keys: List = list(
                      ['sid', 'name', "is_deleted", "owner_sid"]),
                  order_by: str = '-create_time') -> List[Dict]:
        '''
        Summary: [{sid:name}] 用于 前台 select
        NOTE: 手动缓存 改善性能
        '''
        # print(fields)
        keys = [k for k in keys if hasattr(cls, k)]
        ls = []
        if hasattr(cls, 'is_deleted'):
            qs = cls.objects(is_deleted=False)
        else:
            qs = cls.objects()
        for x in qs.order_by(order_by).all():
            dt = {}
            dt['is_deleted'] = False
            for key in keys:
                dt[key] = getattr(x, key)
            dt['sid'] = x.sid
            ls.append(dt)
        return ls

    @classmethod
    def get_count(cls,
                  filter_dt_and: dict = None,
                  recent_days: int = 0,
                  start: Optional[datetime.datetime] = None,
                  end: Optional[datetime.datetime] = None,
                  ) -> int:
        return cls.get_qs(filter_dt_and=filter_dt_and,
                          recent_days=recent_days,
                          start=start,
                          end=end).count()

    def set_attr_by_sid(self,
                        sid_name: str,  # project_sid
                        attr_name: str,  # project_name
                        obj_attr: str = 'name',  # self.project.name
                        orm_class: 'BaseDocumentNoAttr' = None):
        '''
        Summary: 根据类似 project_sid, 设定 project_name
        '''
        if not hasattr(self, sid_name) or not hasattr(self, attr_name):
            print(f'No attr {sid_name} or {attr_name}')
            return None
        if not sid_name:
            setattr(self, attr_name, '')
            return None
        if not orm_class:
            return None
        obj = orm_class.get_by_sid(getattr(self, sid_name))
        if not obj:
            setattr(self, attr_name, '')
        else:
            setattr(self, attr_name, getattr(obj, obj_attr))
        return obj

    @classmethod
    def order_keywords_dict(cls):
        '''
        Summary: 可用于排序的
        '''
        return {
            'create_time': '创建时间',
            'update_time': '更新时间'
        }

    @classmethod
    def create_by_pd(cls, pd: BaseModel, **kwargs):
        '''
        Summary: 根据pd,
        '''
        return cls(**pd.dict())

    def edit_by_pd(self,  pd: BaseModel, **kwargs):
        '''
        Summary: 根据pd,更新model
        '''
        self.update(**pd.dict())
        return self


class BaseDocument(BaseDocumentNoAttr):
    '''
    基础document
    '''
    _classname = 'BaseDocument'

    is_deleted = BooleanField(default=False)
    deleted_time = DateTimeField(default=None)  # 新建时

    meta = {
        'abstract': True,
    }

    @property
    def delete_time_local(self):
        '''
        Summary: 删除时间（假删除）
        '''
        return utc2local(self.deleted_time)

    @property
    def delete_date_local_str(self) -> str:
        return self.delete_time_local.strftime('%Y-%m-%d')

    def switch_delete(self):
        '''
        Summary: 假删除 切换
        '''
        self.is_deleted = not self.is_deleted
        self.deleted_time = datetime.datetime.utcnow()
        self.save()
        return self

    @classmethod
    def get_active_by_sid(cls, sid: str) -> 'BaseDocument':
        '''
        Summary: 仅仅提供active的结果
        '''
        obj = cls.get_by_sid(sid=sid)
        if not obj:
            return None
        if obj.is_deleted:
            return None
        return obj

    @classmethod
    def get_active_by_sid_or_404(cls, sid: str) -> 'BaseDocument':
        # 根据 str objectid  找到 instance,找不到则直接raise HTTPException
        obj = cls.get_active_by_sid(sid=sid)
        if not obj:
            raise MyExceptions.not_found
        return obj


# def update_signal(sender, document: BaseDocumentOwner):
#     document.set_attr_by_sid(
#         sid_name='owner_sid',
#         attr_name='owner_name',
#         obj_attr='name',
#         orm_class=UserOrm)


# class BaseDocumentOwner(BaseDocument):
#     '''
#     Summary: 有 owner_sid 的
#     '''
#     owner_sid = StringField()
#     is_personal = BooleanField(default=False)  # 是否私密,仅本人可见
#     owner_name = StringField()

#     meta = {
#         'abstract': True,
#     }

#     @property
#     def owner(self):
#         if not self.owner_sid:
#             return {
#                 'username': '',
#                 'email':  '',
#                 'sid':  '',
#                 'name':  ''
#             }
#         from app.models.user.models import UserOrm
#         return UserOrm.get_by_sid(sid=self.owner_sid) or {'username': '',
#                                                           'email':  '',
#                                                           'sid':  '',
#                                                           'name':  ''}


class BaseDesignModuleOrm(BaseDocument):
    '''
    Summary: 用于 Design 的 基本产品信息（统一维护）？
    NOTE:所有 膜产品（用于设计） 都应该以此作为base
    '''
    _classname = 'BaseDesignModuleOrm'

    name = StringField(default='')
    material = StringField(default='')  # 材质
    membrane_type = StringField(default='')
    module_type = StringField(default='')
    brand = StringField(default='')
    model = StringField(required=True)
    fa = FloatField(required=True)
    is_contained_pv = BooleanField(default=False)
    flux_per_bar_25 = FloatField(default=80)
    liter_inside = FloatField(default=40)
    spacer_mil = IntField(default=40)  # 有格网
    module_size = StringField(default='')
    rej_dt = DictField()
    description = StringField(default='')

    meta = {
        'abstract': True,
    }
