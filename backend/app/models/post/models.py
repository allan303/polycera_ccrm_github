from mongoengine import (
    StringField, BooleanField, IntField,
    DateTimeField
)

from bs4 import BeautifulSoup
# app
from app.models.user.models import BaseDocumentOwner
from app.models.comment.models import CommentOrm
from app.models.project.models import ProjectOrm
from app.models.oem.models import OemOrm
from app.models.contact.models import ContactOrm
from app.models.order.models import OrderOrm
from app.models.pilot.models import PilotOrm
from .schemas import PostManyToExcelPD


class PostOrm(BaseDocumentOwner):
    '''
    Summary:  Post
    '''
    _classname = 'post'
    _children = ''  # 将会关联到此class的类
    _father = 'project,oem,contact,order,pilot,'  # 此类关联的class

    project_sid = StringField(default='')
    oem_sid = StringField(default='')
    contact_sid = StringField(default='')
    order_sid = StringField(default='')
    pilot_sid = StringField(default='')
    is_system = BooleanField(default=False)  # 是否系统自动生成
    # 对应的名称，不用每次去数据库query
    project_name = StringField()
    oem_name = StringField()
    contact_name = StringField()
    order_name = StringField()
    pilot_name = StringField()
    # 主要内容
    body = StringField(default='')
    allowed_comment = BooleanField(default=True)
    # 自动 更新 ，通过 api
    last_comment_time = DateTimeField(default=None)
    comments_count = IntField(default=0)

    # @property
    # def comments_count(self):
    #     return CommentOrm.objects(is_deleted=False, post_sid=self.sid).count()

    @property
    def soup(self):
        return BeautifulSoup(self.body, "html.parser")

    @property
    def body_str(self):
        soup = self.soup
        '''xml解析到word不能包含<>'''
        dt = {'>': '＞', '<': '＜'}
        st = str(soup.get_text())
        for x in dt:
            st = st.replace(x, dt[x])
        st.replace('<br/>', '')
        return st

    @property
    def body_list(self):
        # 转换为 list 列表
        def deal_bs4_li(soup: BeautifulSoup, ls: list):
            if not soup.string == None:  # 单个节点或者NavigableString才能获取soup
                if soup.name == 'li':
                    ls.append(f'- {soup.string}')
                else:
                    ls.append(f'{soup.string}')
            else:
                contents = soup.contents
                if contents:
                    for c in contents:
                        deal_bs4_li(soup=c, ls=ls)
        ls = []
        deal_bs4_li(soup=self.soup, ls=ls)
        return ls

    

    @property
    def comments(self):
        '''
        Summary: 旗下comment，最近update_time
        '''
        return list(CommentOrm.objects(is_deleted=False, post_sid=self.sid).order_by('-update_time').all()) or []

    @property
    def last_comment_time_str(self) -> str:
        if not self.last_comment_time:
            return ''
        return self.last_comment_time.strftime('%Y-%m-%d')

    @property
    def project(self):
        if not self.project_sid:
            return None
        return ProjectOrm.get_by_sid(sid=self.project_sid)

    @property
    def oem(self):
        if not self.oem_sid:
            return None
        return OemOrm.get_by_sid(sid=self.oem_sid)

    @property
    def contact(self):
        if not self.contact_sid:
            return None
        return ContactOrm.get_by_sid(sid=self.contact_sid)

    @property
    def order(self):
        if not self.order_sid:
            return None
        return OrderOrm.get_by_sid(sid=self.order_sid)

    @property
    def pilot(self):
        if not self.pilot_sid:
            return None
        return PilotOrm.get_by_sid(sid=self.pilot_sid)

    def set_names(self):
        '''
        Summary: 每次修改时候改变 .save()
        '''
        self.set_attr_by_sid(sid_name='project_sid',
                             attr_name='project_name',
                             obj_attr='name',
                             orm_class=ProjectOrm)
        self.set_attr_by_sid(sid_name='oem_sid',
                             attr_name='oem_name',
                             obj_attr='name',
                             orm_class=OemOrm)
        self.set_attr_by_sid(sid_name='pilot_sid',
                             attr_name='pilot_name',
                             obj_attr='name',
                             orm_class=PilotOrm)
        self.set_attr_by_sid(sid_name='order_sid',
                             attr_name='order_name',
                             obj_attr='name',
                             orm_class=OrderOrm)
        self.set_attr_by_sid(sid_name='contact_sid',
                             attr_name='contact_name',
                             obj_attr='name',
                             orm_class=ContactOrm)

    def clean(self):
        '''
        Summary: 
        '''
        # 必须要 reload 才行，不然 @property 会采用原有的缓存

        # self.save_and_reload()
        super().clean()
        self.set_names()
        self.comments_count = CommentOrm.objects(
            is_deleted=False, post_sid=self.sid).count()

    def delete_newest_comment(self):
        '''
        Summary: 删除最新的
        '''
        comment = CommentOrm.objects(
            is_deleted=False, post_sid=self.sid).order_by('-update_time').first()
        if comment:
            comment.delete()
        else:
            print('No Comment')
        self.save()

    def delete_oldest_comment(self):
        '''
        Summary: 删除最老的
        '''
        comment = CommentOrm.objects(
            is_deleted=False, post_sid=self.sid).order_by('+update_time').first()
        if comment:
            comment.delete()
        else:
            print('No Comment')
        self.save()

    @classmethod
    def get_qs(cls, **kwargs):
        return super().get_qs(fuzzy_keys='owner_name,owner_name,body,project_name,oem_name,contact_name,order_name,pilot_name', **kwargs)

    @classmethod
    def order_keywords_dict(cls):
        dt = super().order_keywords_dict()
        add = {
            'project_name': '关联项目',
            'oem_name': '关联客户',
            'contact_name': "关联联系人",
            'order_name': "关联订单",
            'pilot_name': "关联实验"
        }
        add.update(dt)
        return add

    @classmethod
    def many_to_docx(cls,
                     qs: "QuerySet",
                     tpl_name: str = 'posts_tpl.docx',
                     to_file: bool = False,
                     context: dict = None):
        '''
        Summary: QuerySet 报表to_docx
        '''
        tpl_name = tpl_name or 'posts_tpl.docx'
        context = context or {}
        if qs.count() > 0:
            context['start'] = qs.order_by('create_time')[
                0].create_date_local_str
            context['end'] = qs.order_by(
                '-create_time')[0].create_date_local_str
        return super().many_to_docx(qs=qs,
                                    tpl_name=tpl_name,
                                    filename='日志报表',
                                    to_file=to_file,
                                    context=context)

    @classmethod
    def many_to_excel(cls, qs: "QuerySet",
                      pd_class: 'BaseModel' = None,
                      title: str = None,
                      description: str = None,
                      to_file: bool = False):
        return super().many_to_excel(qs=qs,
                                     pd_class=PostManyToExcelPD,
                                     title=title,
                                     description=description,
                                     to_file=to_file)

    @property
    def related(self):
        ls = []
        if self.project:
            ls.append(f'[关联项目]:{self.project.name}')
        if self.oem:
            ls.append(f'[关联客户]:{self.oem.name}')
        if self.contact:
            ls.append(f'[关联联系人]:{self.contact.name}')
        if self.pilot:
            ls.append(f'[关联实验]:{self.pilot.name}')
        if self.order:
            ls.append(f'[关联订单]:{self.order.name}')
        return ls
