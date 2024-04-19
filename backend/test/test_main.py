#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2021-07-19

'''
Unit Test 
'''
from fastapi.testclient import TestClient
from mongoengine import connect, disconnect
import json
from app.factory import create_app
from app.models.user.models import UserOrm, RoleOrm
from app.models.project.models import ProjectOrm, ProjectUpdateOrm
from app.models.oem.models import OemOrm
from app.models.contact.models import ContactOrm
from app.core import config
from app.mycache import create_mycache
from app.manage import insert_fake_data


def get_auth_token(email: str, password: str) -> dict:
    '''
    Summary: 通过login api 获得 auth token
    '''
    res = app.post(url="/api/auth/login",
                   data={'username': email, 'password': password})
    if res.status_code == 200:
        dt = res.json()
        return {'Authorization': f"{dt['token_type']} {dt['access_token']}"}
    else:
        print(res.status_code, email, password)
    return None


# 断开Mongo
disconnect()
# 连接测试数据库
connect('polycera_ccrm_test')
# connect('polycera_ccrm')
# fake数据
# insert_fake_data()
# app工厂函数
ccrm = create_app()
# 测试APP启动
app = TestClient(app=ccrm)
# 缓存初始化
config.MYCACHE = create_mycache()
# 初始化hds：保存不同用户登录信息token
hds = {}
# 非su用户 密码 = 邮箱
role_list = [x.name for x in RoleOrm.objects.only(
    'name').all()]
# 每个角色选一个
while role_list:
    r = role_list.pop()
    u = UserOrm.objects(role_name=r).first()
    if u:
        dt = get_auth_token(u.email or u.phone, config.DEFAULT_USER_PASSWORD)
        hds[u.role_name] = dt
        # if dt:
        #     hds[u.role_name] = dt
        # else:
        #     print('No auth', r)
su_u = UserOrm.objects(role_name='su').first()
hds['su'] = get_auth_token(su_u.email, 'admin1111')


def test_login():
    '''
    Summary: 登录
    '''
    res = app.post(url="/api/auth/login",
                   data={'username': 'su@polycera.com', 'password': 'admin1111'})
    assert res.status_code == 200
    # dt = response.json()
    # print('response:', response.json())
    # assert dt['token_type'] == 'Bearer1'
    # assert dt['access_token'] == 'token'
    # assert dt['count'] > 0


def test_myprofile():
    '''
    Summary: myprofile,SU
    '''
    res = app.get('/api/auth/myprofile', headers=hds['su'])
    dt = res.json()
    assert dt['name'] == '超级管理员'
    assert res.status_code == 200


def test_not_su_user():
    '''
    Summary: 权限：除了su用户，不能访问
    '''
    apis = [
        f'/api/role/list-paginate',
        f'/api/user/list-paginate'
    ]
    for api in apis:
        res = app.post(api, headers=hds['hr'], params={'scope': 'total'})
        assert res.status_code == 403


def test_list_total():
    '''
    Summary:  list-total 测试
    '''
    api = f'/api/project/list-paginate'
    res = app.post(url=api,
                   headers=hds['su'],
                   params={'page': 1, 'keyword': '', 'scope': 'total'})
    dt = res.json()
    print('总数:', dt['count'])
    print('本页:', dt['count_this_page'])
    print('本页:', len(dt['objs']))
    assert res.status_code == 200


def test_list_me():
    '''
    Summary:
        page: Optional[int] = 1
        per_page: Optional[int] = 20
        keyword: Optional[str] = ''
        order_by: Optional[str] = ''
        desc: Optional[int] = 1  # 是否倒叙
        filter_dt_and: Optional[dict] = None
        start: Optional[datetime.date] = None
        end: Optional[datetime.date] = None
        recent_days: Optional[int] = None
    '''
    api = f'/api/project/list-paginate'
    res = app.post(url=api,
                   headers=hds['hr'],
                   params={'page': 1, 'keyword': '', 'scope': 'me'})
    dt = res.json()
    print('总数:', dt['count'])
    print('本页:', dt['count_this_page'])
    print('本页:', len(dt['objs']))
    assert res.status_code == 200


def test_can():
    # 测试权限
    su: UserOrm = UserOrm.objects(role_name='su').first()
    sales: UserOrm = UserOrm.objects(role_name='sales').first()
    order: UserOrm = UserOrm.objects(role_name='order').first()
    sales_pj: ProjectOrm = ProjectOrm.objects(owner_sid=sales.sid).first()
    assert sales.can(model='post') == True
    assert sales.can(model='post', action='create') == True
    assert sales.can(model='project', action='read') == True
    assert sales.can(model='project', action='read', scope='total') == False
    assert sales.can(model='pilot', action='read', scope='total') == True
    assert su.can(model='pilot', action='read', scope='total') == True
    assert su.can(model='pilot', action='edit', scope='total') == True
    assert su.can(model='pilot', action='edit', obj=sales) == True
    assert su.can(model='project', action='edit', obj=sales_pj) == False
    assert sales.can(model='project', action='edit', obj=sales_pj) == True
    # assert sales.can(model='project', action='real_delete',
    #                  obj=sales_pj) == False
    assert order.can(model='quote',) == False


def test_contact_list():
    api = f'/api/contact/list-paginate'
    res = app.post(url=api,
                   headers=hds['su'],
                   params={'page': 1, 'keyword': ''})
    ls = res.json()
    print(ls or "没有")
    assert res.status_code == 200


def test_assign():
    '''
    Summary: assign
    '''
    contact = ContactOrm.objects.first()
    old_owner = contact.owner
    new_owner = UserOrm.objects.first()
    api1 = f'/api/contact/assign/{contact.sid}/{new_owner.sid}'
    res1 = app.post(api1, headers=hds['su'])
    assert res1.status_code == 200
    contact.reload()
    assert contact.owner_sid == new_owner.sid

    pju = ProjectUpdateOrm.objects.first()
    old_owner = pju.owner
    new_owner = UserOrm.objects.first()
    api2 = f'/api/project_update/assign/{pju.sid}/{new_owner.sid}'
    res2 = app.post(api2, headers=hds['su'])
    assert res2.status_code == 403


def test_download_many():
    '''
    Summary: download_many 权限测试
    '''
    api = f'/api/project/download-many'
    res = app.post(url=api,
                   headers=hds['hr'],
                   json={'keyword': '项目', 'scope': 'me', 'desc': 0})
    res1 = app.post(url=api,
                    headers=hds['hr'],
                    json={'keyword': '项目', 'scope': 'total', 'desc': 0})
    assert res.status_code == 200
    assert res1.status_code == 403
