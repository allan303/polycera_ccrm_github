from mongoengine import (
    StringField, FloatField,
    EmbeddedDocument, EmbeddedDocumentListField,
    EmbeddedDocumentField, DateField, BooleanField
)
import datetime
from jackutils.format import to_00,to_price
from jackutils.currency_tool import gen_cn_price

# app
from app.core.jwt import MyExceptions
from app.models.user.models import BaseDocumentOwner
from app.models.oem.models import OemOrm
from app.models.contact.models import ContactOrm
from app.models.project.models import ProjectOrm
from .schemas import OrderCreatePD


class OrderProduct(EmbeddedDocument):
    '''
    Summary: 订单中的产品
    '''
    brand = StringField(default='Polycera')
    description = StringField(default='')  # 描述
    unit_price = FloatField(default=0)  # 单价
    nums = FloatField(default=1)  # 数量
    # auto
    name = StringField(default='')  # 产品名称
    model = StringField(default='')  # 产品型号
    unit = StringField(default='支')

    @property
    def price(self):
        return self.unit_price * self.nums

    @property
    def nums_int(self):
        return int(self.nums)


class ContactInfo(EmbeddedDocument):
    '''
    Summary: 收货联系人
    '''
    name = StringField(default='')
    phone = StringField(default='')
    address = StringField(default='')
    zip_code = StringField(default='')


class OrderOrm(BaseDocumentOwner):
    '''
    Summary: 订单信息
    '''
    _classname = 'order'
    _children = 'post,order_update'  # 将会关联到此class的类
    _father = 'project,oem,contact'  # 此类关联的class

    order_date = DateField(default=None)
    project_sid = StringField(default='')
    oem_sid = StringField(default='')  # 合同客户
    contact_sid = StringField(default='')  # 合同联系人
    products = EmbeddedDocumentListField(OrderProduct)  # 产品信息
    payment_term = StringField(default=f'100%全款')
    shipment_term = StringField(default='1周内')
    shipment_contact = EmbeddedDocumentField(ContactInfo)  # 收货信息
    invoice_contact = EmbeddedDocumentField(ContactInfo)  # 发票邮寄
    remark = StringField()
    free = BooleanField(default=False)
    # auto
    project_name = StringField()
    oem_name = StringField()
    contact_name = StringField()
    name = StringField()  # 自动生成的订单编号
    price = FloatField(default=0)
    price_cn = StringField(default='')
    status = StringField(default='未签订')

    def clean(self):
        # NOTE:不能之前使用 clean ，save_and_reload会导致本身save，命名时候出现bug
        # super().clean()
        super().clean()
        self.set_attr_by_sid(sid_name='project_sid',
                             attr_name='project_name',
                             obj_attr='name',
                             orm_class=ProjectOrm)
        self.set_attr_by_sid(sid_name='oem_sid',
                             attr_name='oem_name',
                             obj_attr='name',
                             orm_class=OemOrm)
        self.set_attr_by_sid(sid_name='contact_sid',
                             attr_name='contact_name',
                             obj_attr='name',
                             orm_class=ContactOrm)
        self.price = sum([x.unit_price * x.nums for x in self.products])
        self.price_cn = gen_cn_price(self.price)

    @staticmethod
    def gen_order_id(pd: OrderCreatePD):
        '''
        Summary: 生成 唯一的 order_name，一旦生成，不再改变，例：PCSH2021070101
        '''
        if not pd.order_date:
            # print('默认order_date')
            order_date = datetime.datetime.today()
        date_str = order_date.strftime('%Y%m%d')  # '20201014'
        # print(date_str)
        # 今日 order 数量
        # current_cum = OrderOrm.objects(order_date=self.order_date).count()
        # cum_num = current_cum + 1  # 增加1
        # if current_cum <= 9:
        #     cum_str = f'0{cum_num}'
        # else:
        #     cum_str = f'{cum_num}'
        # self.name = f'PCSH{date_str}{cum_str}'
        last = OrderOrm.objects(
            order_date=order_date).order_by('-create_time').first()
        if not last:
            suffix = '01'
        else:
            suffix_num = int(last.name[-2:])+1
            suffix = to_00(suffix_num)
        name = f'PCSH{date_str}{suffix}'
        return {
            'order_date': order_date,
            'name': name
        }

    @classmethod
    def get_qs(cls, **kwargs):
        return super().get_qs(fuzzy_keys='owner_name,name,project_name,oem_name,contact_name,remark,shipment_term,payment_term', **kwargs)

    @classmethod
    def order_keywords_dict(cls):
        dt = super().order_keywords_dict()
        add = {
            'name': '名称',
            'project_name': '关联项目',
            'oem_name': "关联客户",
            'contact_name': "关联联系人",
        }
        add.update(dt)
        return add

    @property
    def oem(self):
        # 用于 tpl
        return OemOrm.get_by_sid(self.oem_sid)

    @property
    def contact(self):
        # 用于 tpl
        return ContactOrm.get_by_sid(self.contact_sid)

    @property
    def order_date_str(self):
        # 用于 tpl
        return self.order_date.strftime('%Y-%m-%d')

    def api_hook_create_after_save(self):
        '''
        Summary: 配套新建 status
        '''
        OrderUpdateOrm(order_sid=self.sid, status=self.status,
                       owner_sid=self.owner_sid).save()

    @classmethod
    def create_by_pd(cls, pd: OrderCreatePD, **kwargs):
        '''
        Summary: 根据pd，create
        '''
        # 验证是否重复
        dt = pd.dict()
        dt2 = cls.gen_order_id(pd=pd)
        dt.update(dt2)
        return cls(**dt)

    def one_to_docx(self,
                    tpl_name: str = None,
                    to_file: bool = False,
                    context: dict = None):
        '''
        Summary: ins to docx
        '''
        tpl_name = tpl_name or 'order_tpl.docx'
        if self.free:
            tpl_name = 'order_free_tpl.docx'
        context = context or {}
        context['to_price'] = to_price
        return super().one_to_docx(
            tpl_name=tpl_name,
            to_file=to_file,
            context=context
        )


class OrderUpdateOrm(BaseDocumentOwner):
    '''
    Summary: 订单状态
    '''
    _classname = 'order_update'

    order_sid = StringField(required=True)
    status = StringField(default='未签订')
    remark = StringField(default='')
    # auto
    order_name = StringField(default='')

    def clean(self):
        super().clean()
        # print("order_update clean")
        order = OrderOrm.get_by_sid(self.order_sid)
        if not order:
            raise MyExceptions.need_order_sid
        self.order_name = order.name
        order.status = self.status
        order.save()

    @classmethod
    def get_qs(cls, **kwargs):
        return super().get_qs(fuzzy_keys='owner_name,status,order_name,remark', **kwargs)

    @classmethod
    def order_keywords_dict(cls):
        dt = super().order_keywords_dict()
        add = {
            'status': '状态',
        }
        add.update(dt)
        return add
