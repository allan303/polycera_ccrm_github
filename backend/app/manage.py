#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-09-13

'''
用于 管理 APP
'''
from mongoengine import disconnect, connect
import random
import datetime
import os
import time
import pandas as pd
# app
from app.models.role.models import RoleOrm
from app.models.user.models import UserOrm
from app.models.oem.models import OemOrm
from app.models.config.models import ConfigOrm
from app.models.project.models import ProjectOrm, ProjectOemOrm, ProjectUpdateOrm
from app.models.contact.models import ContactOrm, insert_contact_from_excel
from app.models.pilot.models import PilotOrm
from app.models.post.models import PostOrm
from app.models.comment.models import CommentOrm
from app.models.order.models import OrderOrm, OrderProduct, ContactInfo
from app.models.product.models import ProductOrm
from app.models.design.models import DesignOrm, StandardDesignOrm
from app.models.workgroup.models import WorkgroupOrm
from app.models.design.schemas import OptionAll
from app.models.polycera_membrane.models import (
    PolyceraMembraneOrm, PolyceraModuleOrm, PolyceraSerieOrm)
from app.models.polycera_membrane.schames import (
    PolyceraSerieBasePD, PolyceraModuleBasePD, PolyceraMembraneBasePD)
from app.core.config import PRODUCT_EXCEL_DEST, MONGO_DB, DEFAULT_USER_PASSWORD
from app.models.design_module.models import DesignModuleOrm
from app.core.utils import create_logger
from app.models.all import get_models_list
# 通过下面的方式进行简单配置输出方式与日志级别


logger = create_logger(name="update_version", path="./update_version.log")


def logger_and_print(msg: str):
    logger.info(msg)
    print(msg)


def update_version():
    '''
    Summary: 用于 数据结构更新 每次修改
    '''
    # ConfigOrm.init_model()
    import pymongo
    from pymongo import MongoClient
    myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017")
    db = myclient[MONGO_DB]
    print(db)
    # PolyceraModuleOrm 也受到 size 影响
    init_polycera_modules()
    logger_and_print('Design Module: schame change')
    # db.polycera_module_orm.update_many(
    #     filter={}, update={'$unset': {'size': 1}})
    # db.polycera_serie_orm.update_many(
    #     filter={}, update={'$unset': {'size': 1}})
    # logger_and_print('删除size 字段')
    # for x in PostOrm.objects.all():
    #     if str(x.body).startswith('[') and ']' in x.body:
    #         x.is_system = True
    #         x.save()
    # logger_and_print("设置系统Post is_system")
    # 导入 电厂化学会 联系人表
    # cu = UserOrm.objects(name='刘君').first()
    # insert_contact_from_excel(
    #     cu=cu,
    #     filename='2021年电厂化学设计技术交流会通讯表.xls',
    #     remark="2021年电厂化学设计技术交流会通讯表")
    # print('导入 电厂化学会议联系人表 SUCCESS')
    # ORDER ORM 增加free(bool)
    # db.order_orm.update_many(
    #     {}, {'$set': {'free': False}})
    # print('Order 增加free 成功，全部设置为False')
    # product-order 加入1812等产品
    # ProductOrm.insert_membrane_product()
    # logger.info('增加所有1812产品 success')
    # 插入所有workgroup_sid
    # models_list = get_models_list()
    # CommentOrm.objects.delete()
    # logger_and_print('清空comment')
    # for orm_class in models_list:
    #     for x in orm_class.objects.all():
    #         try:
    #             x.save()
    #         except Exception as e:
    #             print(e)
    # logger_and_print("所有instance 执行save(),为了更新workgroup_sid")
    # su_user workgroup =None
    # su_user = UserOrm.objects(username='su_user').first()
    # su_user.workgroup_sid = ''
    # su_user.workgroup_name = ''
    # su_user.save()
    # logger_and_print("su_user workgroup =None")
    # logger_and_print(f"Update Version")
    # for x in DesignModuleOrm.objects.all():
    #     x.save()
    # logger_and_print(f"所有设计产品brand 都变成首字母大写")


def init_polycera_modules(pathdir: str = None, excel: str = "polyceraproducts_cn.xlsx"):
    '''膜产品数据-数据库初始化'''
    # 使用pandas从Excel中导入数据
    pathdir = pathdir or PRODUCT_EXCEL_DEST
    excel = os.path.join(pathdir, excel)
    t0 = time.process_time()
    print('start....')
    # 先全删
    print('delete old data....')
    PolyceraModuleOrm.objects().delete()
    PolyceraSerieOrm.objects().delete()
    PolyceraMembraneOrm.objects().delete()
    print('deleted !!!')
    # 先建立PolyceraMembraneORM
    print('PolyceraMembraneOrm inserting....')
    df1 = pd.read_excel(excel, sheet_name='平膜')
    # df1 = df1.fillna(0)
    dts1 = list(df1.T.to_dict().values())
    for x in dts1:
        pd1 = PolyceraMembraneBasePD(**x)
        PolyceraMembraneOrm(**pd1.dict()).save()
    # serie
    print('PolyceraSerieOrm inserting....')
    df2 = pd.read_excel(excel, sheet_name='系列')
    # df2 = df2.fillna(0)
    dts2 = list(df2.T.to_dict().values())
    srs = list(df2.name)
    for x in dts2:
        pd2 = PolyceraSerieBasePD(**x)
        PolyceraSerieOrm(**pd2.dict()).save()
    # module
    print('PolyceraModuleOrm inserting....')
    df3 = pd.read_excel(excel, sheet_name='组件')
    df3 = df3.fillna(f'N/A')
    # df3.l1.fillna(f'N/A')
    df4 = df3[df3['serie_name'].isin(srs)]
    dts3 = list(df4.T.to_dict().values())
    for x in dts3:
        pd3 = PolyceraModuleBasePD(**x)
        new = PolyceraModuleOrm(**pd3.dict())
        new.save()
        new.set_test_perm_flux()
    print('Setting membrane_type...')
    for x in PolyceraMembraneOrm.objects().all():
        if x.membrane_type == 'nf':
            x.membrane_str = 'Nanofiltration'
            x.save()
        elif 'offshore' in x.name:
            x.membrane_str = 'Off-Shore Ultrafiltration'
            x.save()
    for x in PolyceraSerieOrm.objects().all():
        x.membrane_type = x.membrane.membrane_type
        x.save()
    for x in PolyceraModuleOrm.objects().all():
        x.membrane_type = x.serie.membrane_type
        if x.membrane_type == 'uf':
            x.name = '超滤膜'
        else:
            x.name = '纳滤膜'
        x.fs_serie = x.membrane.serie
        x.spacer_mil = x.serie.spacer_mil
        x.membrane_name = x.membrane.name
        x.description = f'Polycera聚瓷膜组件,{str(x.membrane.serie).upper()}系列,{x.name},{x.spacer_mil:.0f}mil格网,{x.membrane.mwco},{x.module_size}组件'
        if x.module_size == 8080:
            x.liter_inside = 40
        elif x.module_size == 8040:
            x.liter_inside = 20
        elif x.module_size == 4040:
            x.liter_inside = 10
        elif x.module_size == 2540:
            x.liter_inside = 5
        elif x.module_size == 1812:
            x.liter_inside = 0.5
        x.save()
    print('设置CTUF')
    PolyceraModuleOrm.set_ctufs()
    print('Completed.')
    print(time.process_time() - t0)


def create_connection(database_name: str = 'polycera_ccrm'):
    '''
    Summary: Mongo创建连接
    '''
    host = '127.0.0.1'
    disconnect()
    connect(database_name, host=host)


def init_app():
    '''
    Summary: 初始化APP
    '''
    RoleOrm.init_model()
    UserOrm.objects.delete()
    UserOrm.insert_su(reset=True)
    ConfigOrm.init_model()
    init_polycera_modules()
    ProductOrm.init_model(use_json=True)
    print('insert Order product success')
    DesignModuleOrm.insert_modules(
        delete_all=True, orm_cls_list=[PolyceraModuleOrm])
    print('insert design module success')
    WorkgroupOrm.init_model()
    print('insert workgroup success')


def insert_fake_data():
    '''
    Summary: 使用Faker 注入虚假信息
    '''
    init_app()
    cfg = ConfigOrm.objects().first()
    from faker import Faker
    fk = Faker(locale='zh_CN')  # 中文
    # role
    RoleOrm.init_model()

    # user
    UserOrm.objects().delete()
    UserOrm.insert_su()  # 插入 SU账户
    # 清空 StandardDesignOrm
    StandardDesignOrm.objects().delete()
    workgroup_sids = [x.sid for x in WorkgroupOrm.objects.all()]
    # 创建20个非SU账户
    role_sids = [x.sid for x in RoleOrm.objects().all()
                 if x.name != 'su']  # R
    role_names = [x.name for x in RoleOrm.objects().all()
                  if x.name != 'su']  # R
    # 创建几个固定的非SU账号用于测试
    for u in role_names:
        user = UserOrm(
            name=u,
            email=u+"@polycera.com",
            role_sid=RoleOrm.objects(name=u).first().sid,
            workgroup_sid=random.choice(workgroup_sids),
            title=fk.job(),
            phone=fk.phone_number(),
            company=fk.company(),
            username=fk.user_name()+u,
            update_time=fk.date_time(),
            country=fk.country(),
            province=fk.province(),  # 地区
            gender=random.choice(['male', 'female'])  # 1 男 2女 0未知
        )
        user.password = DEFAULT_USER_PASSWORD
        user.save()

    for i in range(20):
        user = UserOrm(
            name=fk.name(),
            email=f'{i}'+fk.email(),
            role_sid=random.choice(role_sids),
            workgroup_sid=random.choice(workgroup_sids),
            title=fk.job(),
            phone=fk.phone_number(),
            company=fk.company(),
            username=fk.user_name()+f'{i}',
            update_time=fk.date_time(),
            country=fk.country(),
            province=fk.province(),  # 地区
            gender=random.choice(['male', 'female'])  # 1 男 2女 0未知
        )
        user.password = DEFAULT_USER_PASSWORD
        user.save()
    user_sids = [x.sid for x in UserOrm.objects().all()]  # User Sids
    print('fake users success')
    # 插入 fake 信息
    # oems
    OemOrm.objects().delete()
    oemtype_list = cfg.oemtype
    for i in range(random.randint(10, 50)):
        oem = OemOrm(
            name=fk.company()+f'{i}',
            location=fk.province(),
            oemtype=random.choice(oemtype_list),
            # 开票信息
            company_code=fk.ssn()+f'{i}',  # 税号
            company_address=fk.address(),  # 开票地址
            company_bank=fk.company_prefix()+f'{i}银行',  # 银行
            company_bank_account=fk.credit_card_number()+f'{i}',  # 银行账户
            company_telephone=fk.phone_number(),  # 电话
            company_zipcode=str(fk.random_int(100000, 999999)),  # 邮编
            # 通讯地址
            remark=fk.text(),
            owner_sid=random.choice(user_sids),  # 备注
            update_time=fk.date_time()
        )
        oem.save()
    oem_sids = [x.sid for x in OemOrm.objects().all()]
    print('fake oems success')
    # projects
    ProjectOrm.objects().delete()
    for i in range(random.randint(30, 100)):
        pj = ProjectOrm(
            name=fk.company_prefix()+f'{i}项目',
            location=random.choice(cfg.location),  # 地区
            industry=random.choice(cfg.industry),  # 行业
            pjtype=random.choice(cfg.pjtype),  # 新建
            source=random.choice(cfg.source),  # 来源
            remark=fk.text(),
            owner_sid=random.choice(user_sids),
            update_time=fk.date_time(),
        )
        pj.save()
    project_sids = [x.sid for x in ProjectOrm.objects().all()]
    print('fake projects success')
    # project update
    ProjectUpdateOrm.objects().delete()
    for i in range(ProjectOrm.objects.count()*3):
        pju = ProjectUpdateOrm(
            owner_sid=random.choice(user_sids),
            project_sid=random.choice(project_sids),
            pjstage=random.choice([x['name'] for x in cfg.pjstage]),  # 项目阶段
            win_percentage=random.choice(
                [x['win_percentage'] for x in cfg.pjstage]),  # 成功率权重
            forecast_date=fk.date_between_dates(date_start=datetime.date(2020, 1, 1),
                                                date_end=datetime.date(2025, 1, 1)),
            remark=fk.text(),  # 备注
            update_time=fk.date_time()
        )
        pju.save()
    print('fake project_updates success')

    # project oem
    ProjectOemOrm.objects().delete()
    for i in range(ProjectOrm.objects.count()):
        try:
            pjo = ProjectOemOrm(
                owner_sid=random.choice(user_sids),
                project_sid=random.choice(project_sids),
                oem_sid=random.choice(oem_sids),
                is_filing=random.choice([True, False]),  # 备案与否
                remark=fk.text(),  # 备案内容
                update_time=fk.date_time()
            )
            pjo.save()
        except:
            ...
    print('fake project_oems success')
    # contact
    ContactOrm.objects().delete()
    for i in range(random.randint(20, 100)):
        contact = ContactOrm(
            name=fk.name(),
            oem_sid=random.choice(oem_sids),
            department=random.choice(cfg.department),
            title=random.choice(cfg.title),
            phone=fk.phone_number(),
            email=fk.email(),
            remark=fk.text(),
            owner_sid=random.choice(user_sids),
            update_time=fk.date_time(),
        )
        contact.save()
    contact_sids = [x.sid for x in ContactOrm.objects().all()]
    print('fake contacts success')
    # order
    OrderOrm.objects.delete()
    products = ProductOrm.objects.all()
    for i in range(random.randint(20, 100)):
        products_list = []
        for i in range(random.randint(1, 5)):
            pd = random.choice(products)
            opd = OrderProduct(
                name=pd.name,
                model=pd.model,
                description=pd.description,  # 描述
                unit_price=random.randint(1, 100)*100,  # 单价
                nums=random.randint(1, 200)  # 数量
            )
            products_list.append(opd)
        od = OrderOrm(
            order_date=fk.date_time(),
            oem_sid=random.choice(oem_sids),  # 合同客户
            contact_sid=random.choice(contact_sids),  # 合同联系人
            products=products_list,  # 产品信息
            # payment_term=StringField(default=f'100%全款')
            # shipment_term=StringField(default='1周内')
            shipment_contact=ContactInfo(
                name=fk.name(),
                phone=fk.phone_number(),
                address=fk.address(),
            ),  # 收货信息
            invoice_contact=ContactInfo(
                name=fk.name(),
                phone=fk.phone_number(),
                address=fk.address(),
            ),  # 发票邮寄
            owner_sid=random.choice(user_sids),
            update_time=fk.date_time()
            # # 自动修改
            # name=StringField()  # 自动生成的订单编号
            # price=FloatField(default=0)
            # price_cn=StringField()
        )
        od.save()
    order_sids = [x.sid for x in OrderOrm.objects().all()]
    print('fake orders success')
    # pilot
    PilotOrm.objects.delete()
    for i in range(random.randint(20, 50)):
        plt = PilotOrm(
            name=fk.name()+'小实验',  # 针对项目
            project_sid=random.choice(project_sids),  # 针对项目
            oem_sid=random.choice(oem_sids),  # 针对客户
            location=random.choice(cfg.location),  # 地区
            industry=random.choice(cfg.industry),  # 地区
            wwtype=random.choice(cfg.wwtype),
            start=datetime.date.today(),
            remark=fk.text(),
            owner_sid=random.choice(user_sids),
        )
        plt.save()
    pilot_sids = [x.sid for x in PilotOrm.objects().all()]
    print('fake pilots success')
    # post
    PostOrm.objects.delete()
    for i in range(random.randint(100, 1000)):
        pj = random.choice(project_sids) if random.choice([0, 1]) else ''
        oem = random.choice(oem_sids)if random.choice([0, 1]) else ''
        contact = random.choice(contact_sids)if random.choice([0, 1]) else ''
        order = random.choice(order_sids)if random.choice([0, 1]) else ''
        pilot = random.choice(pilot_sids)if random.choice([0, 1]) else ''
        post = PostOrm(
            project_sid=pj,
            oem_sid=oem,
            contact_sid=contact,
            order_sid=order,
            pilot_sid=pilot,
            body=fk.text(),
            owner_sid=random.choice(user_sids),
            update_time=fk.date_time()
        )
        post.save()
    post_sids = [x.sid for x in PostOrm.objects().all()]
    print('fake posts success')
    # comment
    for i in range(random.randint(100, 1000)):
        CommentOrm(
            post_sid=random.choice(post_sids),
            at_users_sid=[random.choice(user_sids)],  # @ 的用户，后期用于 消息提醒
            body=fk.text(),
            quote_comment=fk.text(),
            owner_sid=random.choice(user_sids),
            update_time=fk.date_time()  # 引用的评论
        ).save()
    print('fake comments success')
    # design
    DesignOrm.objects.delete()
    for q in range(10, 200, 20):  # 水量
        op_pd = OptionAll()
        op_pd.raw_flow.q = q
        op_pd.raw_flow.q_unit = random.choice(['m3/d', 'm3/h'])
        op_pd.is_target_perm = random.choice([True, False])
        use_cir = random.choice([True, False])
        if use_cir:
            use_backflow = False
        else:
            use_backflow = random.choice([True, False])
        op_pd.cir.is_use = use_cir
        op_pd.cir.m3ph_per_train = random.randint(5, 50)
        op_pd.backflow.is_use = use_backflow
        op_pd.backflow.m3ph_per_train = random.randint(5, 50)
        op_pd.module.model = random.choice(['Hydro-uf-100-40-8040',
                                            'Hydro-uf-100-65-8040',
                                            'Hydro-uf-100-90-8040'])
        ds = DesignOrm(
            name=f'Q{q},是产水{op_pd.is_target_perm},Cir={use_cir},BF={use_backflow}',
            project_sid=random.choice(project_sids),
            oem_sid=random.choice(oem_sids),
            options=op_pd.dict(),
            owner_sid=random.choice(user_sids),
            update_time=fk.date_time()  # 引用的评论
        )
        ds.save()
        StandardDesignOrm(options=ds.options,
                          owner_sid=random.choice(
                              user_sids),
                          remark=fk.text(),
                          name=fk.name()+'配置').save()
    print('fake designs & design-options success')
    print('......')
    print('SUCCESS')


if __name__ == '__main__':
    update_version()
