from mongoengine import StringField
from typing import List, Dict
from jackutils.excel_tool import get_from_excel
# app
from app.models.user.models import BaseDocumentOwner, UserOrm
from app.models.oem.models import OemOrm
from .schemas import ContactCreateWithOemNamePD, ContactCreatePD, ContactCreateRawPD
from app.core import config
from app.core.errors import MyExceptions
from app.models.config.models import ConfigOrm


class ContactOrm(BaseDocumentOwner):
    _classname = 'contact'
    _children = 'post'  # 将会关联到此class的类
    _father = 'oem'  # 此类关联的class

    name = StringField(default='')
    oem_sid = StringField(default='')
    department = StringField(default='')
    title = StringField(default='')
    phone = StringField(default='')
    email = StringField(default='')
    address = StringField(default='')
    remark = StringField(default='')
    # auto
    oem_name = StringField(default='')

    def clean(self):
        super().clean()
        self.set_attr_by_sid(
            sid_name='oem_sid',
            attr_name='oem_name',
            obj_attr='name',
            orm_class=OemOrm
        )

    @property
    def oem(self):
        oem = OemOrm.get_active_by_sid(self.oem_sid)
        if not oem:
            return {}
        return oem

    @classmethod
    def get_cache(cls) -> List[Dict]:
        '''
        Summary: [{sid:name}] 用于 前台 select
        NOTE： 手动缓存 改善性能
        '''
        return super().get_cache(keys=['sid', 'name', "is_deleted", "oem_sid", "owner_sid", 'oem_name'])

    @classmethod
    def get_qs(cls, **kwargs):
        return super().get_qs(fuzzy_keys='owner_name,name,email,address,oem_name', **kwargs)

    @classmethod
    def order_keywords_dict(cls):
        dt = super().order_keywords_dict()
        add = {
            'name': '名称',
            'oem_name': '关联客户',
            'department': "部门",
            'title': "职位",
        }
        add.update(dt)
        return add

    @classmethod
    def create_by_pd(cls, pd: ContactCreatePD, owner_sid: str, **kwargs):
        '''
        Summary: 通过pd新建
        '''
        if not pd.name:
            raise MyExceptions.name_needed
        cfg = ConfigOrm.objects.first()
        if not pd.new_oemtype in cfg.oemtype:
            pd.new_oemtype = '其他'
        pd1 = ContactCreateRawPD.from_orm(pd)
        if pd.oem_sid:
            # 传入了oem_sid
            ...
        else:
            # 没有传入oem_sid
            oem_obj = OemOrm.objects(name=pd.new_oemname).first()
            if oem_obj:  # 现有的oem
                pd1.oem_sid = oem_obj.sid
            else:
                # 需要新建OEM
                oem_obj = OemOrm(name=pd.new_oemname,
                                 owner_sid=owner_sid,
                                 oemtype=pd.new_oemtype).save()
                pd1.oem_sid = oem_obj.sid
        # 检查 contact是否已存在
        exist_contact = ContactOrm.objects(
            name=pd1.name, oem_sid=pd1.oem_sid).first()
        if exist_contact:
            raise MyExceptions.contact_already_exist
        return cls(**pd1.dict(), owner_sid=owner_sid)

    def edit_by_pd(self, pd: ContactCreatePD):
        newpd = ContactCreateRawPD(**pd.dict())
        self.update(**newpd.dict())
        return self


def create_contact_with_oem_name(cu: UserOrm, data: ContactCreateWithOemNamePD, remark: str = ''):
    '''
    Summary: 新增用户，带OEM名称
    '''
    contact_pd = data.contact
    if data.oem_name and not contact_pd.oem_sid:  # 如果提供了,并且没有oem_sid 提供
        oem_obj = OemOrm.objects(name=data.oem_name).first()
        if not oem_obj:
            oem_obj = OemOrm(name=data.oem_name,
                             owner_sid=cu.sid,
                             company_address=contact_pd.address,
                             remark=remark).save()
        contact_pd.oem_sid = oem_obj.sid
        contact_pd.remark = remark
    exist_contact = ContactOrm.objects(
        name=contact_pd.name, oem_sid=contact_pd.oem_sid).first()
    if exist_contact:
        print(
            f'Contact [{contact_pd.name},{data.oem_name}] already exist, no action.')
        return None
    contact = ContactOrm(**contact_pd.dict())
    contact.owner_sid = cu.sid
    contact.save()
    return contact


def insert_contact_from_excel(cu: UserOrm, filename: str, dirpath: str = config.EXCEL_DEST, remark: str = ''):
    '''
    Summary: 从excel中直接导入大量
    表头：
        name, oem_name, title, address, phone
    '''
    pd = get_from_excel(filename=filename, dirpath=dirpath)
    ls = list(pd.T.to_dict().values())  # 转换为List[Dict]
    for dt in ls:
        data = ContactCreateWithOemNamePD(**dt)
        data.contact = ContactCreatePD(**dt)
        create_contact_with_oem_name(cu=cu, data=data)
