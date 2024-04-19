
from typing import List, Union, Dict
from mongoengine import (
    StringField, EmailField,
    BooleanField, DateTimeField,
    ListField,  EmbeddedDocument, EmbeddedDocumentField,
    queryset_manager
)
import datetime
# App level
from app.models.base_model import BaseDocument
from app.core.secure import verify_password_raw,  get_password_hash
from app.core.errors import MyExceptions
from app.models.config.models import ValidateCode
from app.core.utils import can
from app.models.role.models import RoleOrm
from app.models.workgroup.models import WorkgroupOrm
from jackutils.time_tool import utc2local
from app.core.errors import MyExceptions
from app.core import config
from .schemas import UserCreatePD


class UserConfigEmbeddedDocument(EmbeddedDocument):
    locale = StringField(default='zh')
    use_half = BooleanField(default=False)


class UserOrm(BaseDocument):
    '''
    Summary: 用户db Model
    Note   : 
    Example: 
    '''
    _classname = 'user'
    _children = ''  # 将会关联到此class的类
    _father = 'role,workgroup'  # 此类关联的class

    role_sid = StringField(default='')
    workgroup_sid = StringField(default='')  # 工作组
    role_name = StringField()  # Auto
    username = StringField(max_length=50)
    email = StringField(default='')
    phone = StringField(default='')
    company = StringField(default='聚瓷（上海）科技有限公司')
    last_seen = DateTimeField(default=None)
    lang = StringField(default='en')
    password_hash = StringField(default='')
    name = StringField(default='')
    name_en = StringField(default='')  # 英文名
    title = StringField(default='')
    # wechat
    country = StringField(max_length=200, default='')
    province = StringField(max_length=200, default='')  # 地区
    gender = StringField(default='')  # 1 男 2女 0未知
    remark = StringField(default='')
    # wechat info
    # openid = StringField(max_length=200)
    # nickname = StringField(max_length=200, default='')
    # gender = IntField(default=0, required=False)  # 1 男 2女 0未知
    # city = StringField(max_length=200, default='')
    # headimgurl = StringField(max_length=250, default='')  # 头像
    # 自动计算
    role_name = StringField(default='')
    workgroup_name = StringField(default='')
    user_config = EmbeddedDocumentField(
        UserConfigEmbeddedDocument, default=UserConfigEmbeddedDocument())  # 用户配置

    @property
    def perm(self):
        '''
        Summary: same with Role.perm
        '''
        if not self.role:
            return {}
        return self.role.perm

    @property
    def is_su(self):
        return str(self.role_name).lower() == 'su'

    def clean(self):
        # 根据 role_sid 设定 role_name
        super().clean()
        if self.username == config.SU_USERNAME:
            su_role = RoleOrm.su()
            self.role_sid = su_role.sid
            self.role_name = su_role.name
        else:
            self.set_attr_by_sid(
                sid_name='role_sid',
                attr_name='role_name',
                obj_attr='name',
                orm_class=RoleOrm)
        self.set_attr_by_sid(
            sid_name='workgroup_sid',
            attr_name='workgroup_name',
            obj_attr='name',
            orm_class=WorkgroupOrm)
        if not self.password_hash:
            self.password = config.DEFAULT_USER_PASSWORD

    @property
    def role(self):
        # orm obj
        return RoleOrm.get_by_sid(sid=self.role_sid)

    @property
    def is_admin(self):
        '''
        Summary: 是否具备管理员权限
        '''
        if self.is_su:
            return True
        if self.role_name == 'admin':
            return True
        return False

    @property
    def last_seen_local(self) -> datetime.datetime:
        '''
        Summary: 最后登录
        '''
        if not self.last_seen:
            return None
        return utc2local(self.last_seen)

    @classmethod
    def insert_su(cls, reset: bool = False):
        '''
        Summary: 插入或者更新 SU
        '''
        if reset:
            cls.objects.delete()
        su = cls.objects(role_name__iexact='su').first()
        rl_su = RoleOrm.objects(name='su').first()
        if not su:
            from app.core import config
            # 新建
            print('没有SU，插入SU用户')
            su = cls(
                username=config.SU_USERNAME,
                email='su@admin.com',
                company='admin',
                name='超级管理员',
                role_sid=rl_su.sid
            )
            su.password = config.SU_PASSWORD
            su.save()
        else:
            su.password = config.SU_PASSWORD

    @property
    def validate_code(self):
        return ValidateCode.objects(email=self.email).first()

    @property
    def password(self):
        return None

    @password.setter
    def password(self, password: str):
        # set password & salt
        if not password:
            raise ValueError('密码不能为空')
        password_hash = get_password_hash(
            password=password)  # 生成password_hash
        self.password_hash = password_hash  # 存入数据库

    def verify_password(self, password: str) -> bool:
        # 验证密码
        return verify_password_raw(password=password, password_hash=self.password_hash)

    def update_last_seen(self):
        # 刷新用户最后登录时间，每次收到用户请求都会调用ping方法
        self.last_seen = datetime.datetime.utcnow()
        self.save()

    def is_sub(self, user=None) -> bool:
        '''
        Summary: 判定一个用户是不是 self 的 属下
        '''
        return False

    def can(self,
            model: str,  # 必须提供
            action: str = None,
            scope: str = 'me',
            obj: object = None,
            qs: "QuerySet" = None):
        '''
        Summary: 权限判定
        action : 操作名称
        NOTE: 即使是SU也不可编辑其他人创建的信息，但是可以删除
        '''
        owner_sid = getattr(obj, 'owner_sid', None)
        share_list = getattr(obj, 'share_list', None)
        return can(
            perm=self.perm,
            is_su=self.is_su,
            user_sid=self.sid,
            model=model,
            action=action,
            scope=scope,
            owner_sid=owner_sid,
            share_list=share_list,
            qs=qs
        )

        # @property
        # def perm(self):
        #     '''
        #     Summary: 权限
        #     '''
        #     return self.role.perm if self.role else {}

    @classmethod
    def get_cache(cls) -> List[Dict]:
        '''
        Summary: [{sid:name}] 用于 前台 select
        NOTE： 手动缓存 改善性能
        '''
        return super().get_cache(keys=['sid', 'name', 'username', "is_deleted", "email", 'role_name'])

    @classmethod
    def get_qs(cls, **kwargs):
        return super().get_qs(fuzzy_keys='name,email,username,role_name,company,title,province,country,workgroup_name', **kwargs)

    @classmethod
    def order_keywords_dict(cls):
        add = {
            'name': '姓名',
            'username': '用户名',
            'email': '邮箱',
            'role_name': "角色",
            'company': '公司',
        }
        return add

    @staticmethod
    def validate_email_phone(phone: str = None, email: str = None):
        '''
        Summary:  保存之前 验证 email 或 phone 是否重复
        '''
        if not phone and not email:
            return True
        if phone:
            c = UserOrm.objects(phone__iexact=phone).first()
            if c:
                raise MyExceptions.phone_already_exist
        if email:
            c = UserOrm.objects(email__iexact=email).first()
            if c:
                raise MyExceptions.email_already_exist

    @classmethod
    def create_by_pd(cls, pd: UserCreatePD, **kwargs):
        '''
        Summary: 根据pd，create
        '''
        if str(pd.username).lower() == config.SU_USERNAME:
            raise MyExceptions.su_user_not_allowed
        # 验证是否重复
        cls.validate_email_phone(email=pd.email, phone=pd.phone)
        return cls(**pd.dict())

    def edit_by_pd(self,  pd: UserCreatePD):
        '''
        Summary: 根据pd，edit
        '''
        dt = pd.dict()
        if self.username == config.SU_USERNAME:
            raise MyExceptions.su_not_allowed_edit
        email, phone = dt.get('email', None), dt.get('phone', None)
        # 与现在相同，则不需要验证
        if email == self.email:
            email = None
        if phone == self.phone:
            phone = None
        self.validate_email_phone(phone=phone, email=email)
        self.update(**pd.dict())
        return self


class BaseDocumentOwner(BaseDocument):
    '''
    Summary: 有 owner_sid 的
    '''
    _classname = 'BaseDocumentOwner'

    owner_sid = StringField()
    is_public = BooleanField(default=False)  # 是否私密，仅本人可见
    owner_name = StringField()
    owner_username = StringField()
    workgroup_sid = StringField()  # workgroup
    share_list = ListField(StringField())  # 用于控制share,仅适用于有OWNER属性的orm

    meta = {
        'abstract': True,
    }

    @property
    def owner(self):
        return UserOrm.get_by_sid(sid=self.owner_sid)

    def clean(self):
        super().clean()
        u: UserOrm = UserOrm.get_by_sid(self.owner_sid)
        if not u:
            return None
        self.owner_name = u.name
        self.owner_username = u.username
        self.workgroup_sid = u.workgroup_sid

    @classmethod
    def order_keywords_dict(cls):
        dt = super().order_keywords_dict()
        add = {
            'owner_name': "OWNER",
        }
        add.update(dt)
        return add

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
        owner: UserOrm = UserOrm.get_by_sid(sid=owner_sid)
        if owner:
            # 如果是超级管理员，可以选择workgroup_sid
            if owner.is_su:
                return super().get_qs(filter_dt_and=filter_dt_and,  # and关系
                                      filter_dt_or=filter_dt_or,  # or关系
                                      order_by=order_by,
                                      recent_days=recent_days,
                                      start=start,  # 包含start and end
                                      end=end,
                                      fuzzy_keys=fuzzy_keys,  # 模糊, 'name,description'
                                      keyword=keyword,
                                      use_workgroup=use_workgroup,
                                      workgroup_sid=workgroup_sid)
            else:
                workgroup_sid = owner.workgroup_sid
        else:
            workgroup_sid = ''
        # 非SU情况下，强制使用use_workgroup, 并将workgroup_sid调整为owner.workgroup_sid
        return super().get_qs(filter_dt_and=filter_dt_and,  # and关系
                              filter_dt_or=filter_dt_or,  # or关系
                              order_by=order_by,
                              recent_days=recent_days,
                              start=start,  # 包含start and end
                              end=end,
                              fuzzy_keys=fuzzy_keys,  # 模糊, 'name,description'
                              keyword=keyword,
                              use_workgroup=use_workgroup,
                              workgroup_sid=workgroup_sid)
