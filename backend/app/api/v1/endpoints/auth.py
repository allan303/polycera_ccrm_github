#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2019-10-28


import datetime
import time
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional, Union
# app level
# from app.core.email import send_email
# from app.core.email_async import send_email_async
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, DEFAULT_USER_PASSWORD
from app.core.jwt import create_access_token
from app.models.base_pd import MsgResponese
# from app.models.config.models import ValidateCode
from app.mycache import create_mycache
from app.core.jwt import CurrentUser
from app.core.errors import MyExceptions
from app.models.user.models import UserOrm
from app.models.user.schemas import UserDbPD, ProfileEditPD, UserSimplePD, UserConfig
from app.models.config.models import ConfigOrm
from app.models.config.schemas import ConfigPD
from app.core.config import MYCACHE
# 以下用于重置 MYCACHE
from app.models.project.models import ProjectOrm
from app.models.oem.models import OemOrm
from app.models.contact.models import ContactOrm
from app.models.product.models import ProductOrm
from app.models.role.models import RoleOrm
from app.models.pilot.models import PilotOrm
from app.models.order.models import OrderOrm
from app.models.polycera_membrane.models import PolyceraModuleOrm
from app.models.post.models import PostOrm
from app.models.permission.schemas import perm_option

# 实例化 APIRouter，并将本页所有URL挂到此router下
router = APIRouter(prefix='/auth',
                   tags=['auth'])


'''
以下操作用户
每个API都要进行权限判定
'''


class AllCachePD(BaseModel):
    names: Optional[str] = ''
    total: bool = True


@router.post('/all_cache_info')
async def all_cache_info(data: AllCachePD):
    '''
    Summary: 根据 names,返回一个 特定的 cache dict
    '''
    if data.total:
        return MYCACHE
    if not data.names:
        return MYCACHE
    names = [x.strip() for x in data.names.split(',')]
    dt = {}
    for key in names:
        if key in MYCACHE:
            dt[key] = MYCACHE[key]
    if not dt:  # 不返回空
        # print('2')
        return MYCACHE
    # print('3', list(dt.keys()))
    return dt


@router.post('/reset_all_cache_info', response_model=MsgResponese)
async def reset_all_cache_info(cu: UserOrm = Depends(CurrentUser(su_required=True))):
    '''
    Summary: 重设所有 cache，消耗很大
    '''
    dt = create_mycache()
    MYCACHE.update(dt)
    return {'msg': '已经更新所有缓存'}


# class GetVcodePD(BaseModel):
#     email: EmailStr
#     target: str = 'register'


# @router.post('/generate-vcode', response_model=MsgResponese)
# async def generate_vcode(data: GetVcodePD):
#     '''
#     Summary: 向email 发送注册码，保存在EmailVcode 数据库中
#     Note : Email 地址 Lower()
#     '''
#     email, target = str(data.email).lower(), data.target
#     if str(target).lower() == 'register':
#         user = UserOrm.objects(email=email).first()
#         if user:
#             raise MyExceptions.email_already_exist
#     else:
#         user = UserOrm.objects(email=email).first()
#         if not user:
#             raise MyExceptions.user_not_found

#     vcode = generate_random_str(size=6, only_number=True)
#     ev = ValidateCode.objects(email=email).first()
#     if ev:
#         # 如果已经存在
#         time_delt = datetime.datetime.utcnow() - ev.update_time
#         seconds = time_delt.total_seconds()
#         if seconds <= 60:
#             # 60秒只能一次
#             return {"msg": f'[{target}]Please get validate code after {seconds}s'}
#         ev.vcode = vcode
#         # ev.update_time = datetime.datetime.utcnow()
#         ev.save()
#     else:
#         ev = ValidateCode(email=email, vcode=vcode).save()
#     await send_email_async(title='[POREX Online TMF Design] validate code',
#                            message=f'Your validate code is {vcode}, please use it in 15 minutes.',
#                            to=email)
#     return {"msg": 'success'}


# class RegisterData(BaseModel):
#     # 注册信息
#     email: EmailStr
#     password: str
#     vcode: str = ''


# @router.post('/register', response_model=MsgResponese)
# async def register(data: RegisterData):
#     '''
#     Summary: 注册信息
#     Return : 返回注册
#     '''
#     # 验证码
#     email, vcode, password = str(data.email).lower(), data.vcode, data.password
#     oldu = UserOrm.objects(email=email).first()
#     if oldu:
#         raise MyExceptions.email_already_exist
#     ev = ValidateCode.objects(email=data.email, vcode=data.vcode).first()
#     if not ev:
#         raise MyExceptions.bad_vcode
#     if not ev.vcode == data.vcode:
#         raise MyExceptions.bad_vcode
#     now = datetime.datetime.utcnow()
#     dlt = now - ev.update_time  # 更新的时间
#     if dlt.total_seconds() > 15 * 60:
#         raise MyExceptions.vcode_expired
#     # 无错的话注册用户
#     user = UserOrm(email=data.email)
#     user.save()
#     user.password = data.password
#     user.save()
#     return {'msg': 'Register Success'}


# class TokenLogin(BaseModel):
#     access_token: str = ''
#     token_type: str = ''
#     username: Optional[str] = ''
#     email: EmailStr = None
#     scopes: List[str] = []
#     is_su: bool = False
#     is_admin: bool = False
#     lang: str = 'en'

class LoginResponse(BaseModel):
    '''
    Summary: 登录后返回的信息
    '''
    cu: UserDbPD
    access_token: str
    token_type: str
    expire_minutes: int
    perm_option: dict


@router.post('/login', response_model=LoginResponse)
async def login(data: OAuth2PasswordRequestForm = Depends()):
    '''
    Summary: 提供 不同登录方式：username/email/phone(Form传过来都是username)
    Note   : 只有 /login 会进行登录错误exception，其他页面按照匿名用户登录
    Return : access token & token type
    '''
    # 解压form中的参数
    username, password, scopes = data.username, data.password, data.scopes
    if not username or not password:
        # 缺少 用户名或密码
        raise MyExceptions.bad_username_password
    # 通过Email注册
    user = UserOrm.get_qs(
        filter_dt_or={'email__iexact': username, 'phone__iexact': username}).first()
    # user: UserOrm = UserOrm.objects(email__iexact=username).first()
    if not user:
        raise MyExceptions.bad_username_password
    if user.is_deleted:
        raise MyExceptions.locked_user
    # 密码验证
    if not user.verify_password(password=password):
        raise MyExceptions.bad_username_password
    # 登录时间更新
    user.update_last_seen()
    # 都正确，则生成access_token并返回
    # print({'username': user.username, 'email': user.email, 'scopes': scopes},)
    access_token = await create_access_token(
        # 用 用户名 作为playload
        data={'sub': user.sid, 'scopes': scopes},
        expire_minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # 以下信息用于构建 FrontEnd  Authentication Header
    # NOTE: 返回的dict形式access_token 和 token_type 是必须在1级目录的，不然会影响 获取 currentUser时候得函数
    return {
        'cu': user,
        'access_token': access_token,
        'token_type': 'Bearer',
        'expire_minutes': ACCESS_TOKEN_EXPIRE_MINUTES,
        'perm_option': perm_option
    }


@router.post('/update_token', response_model=LoginResponse)
async def update_token(cu: UserOrm = Depends(CurrentUser())):
    '''
    Summary: 通过现有token，更新前台 login 数据
    NOTE:包含 过期时间（比如 60分钟内）
    '''
    cu.update_last_seen()
    access_token = await create_access_token(
        # 用 用户名 作为playload
        data={'sub': cu.sid, 'scopes': ''},
        expire_minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return {'cu': cu,
            'access_token': access_token,
            'token_type': 'Bearer',
            'expire_minutes': ACCESS_TOKEN_EXPIRE_MINUTES,
            'perm_option': perm_option
            }

# @router.post('/reset-password-by-email', response_model=MsgResponese)
# async def reset_password_by_email(data: RegisterData):
#     '''
#     Summary: 忘记密码 通过email 重新设置密码
#     Note   : 无需登录
#     '''
#     email, vcode, password = data.email, data.vcode, data.password
#     user = UserOrm.objects(email=email).first()
#     if not user:
#         raise MyExceptions.user_not_found
#     ev = ValidateCode.objects(email=data.email, vcode=data.vcode).first()
#     if not ev:
#         raise MyExceptions.bad_vcode
#     if not ev.vcode == data.vcode:
#         raise MyExceptions.bad_vcode
#     now = datetime.datetime.utcnow()
#     dlt = now - ev.update_time  # 更新的时间
#     if dlt.total_seconds() > 15 * 60:
#         raise MyExceptions.vcode_expired
#     # 无错的话重置密码
#     user.password = data.password
#     user.save()
#     return {'msg': 'Change Password Success'}


@router.get('/myprofile', response_model=UserSimplePD)
async def myprofile(cu: UserOrm = Depends(CurrentUser())):
    '''用户详情页'''
    return cu


@router.post('/myprofile/edit', response_model=MsgResponese)
async def myprofile_edit(data: ProfileEditPD, cu: UserOrm = Depends(CurrentUser())):
    '''编辑 myprofile'''
    cu.edit_by_pd(pd=data)
    return {'msg': 'success'}


class ChangePasswordPD(BaseModel):
    old_password: str
    new_password: str


@router.post('/change-password', response_model=MsgResponese)
async def change_password(data: ChangePasswordPD, cu: UserOrm = Depends(CurrentUser())):
    '''
    Summary: 通过旧密码——更改密码
    '''
    if not cu.verify_password(data.old_password):
        raise MyExceptions.bad_old_password
    cu.password = data.new_password
    cu.save()
    return {'msg': 'success'}


@router.post('/default-user-password', response_model=MsgResponese)
async def default_user_password(cu: UserOrm = Depends(CurrentUser(su_required=True))):
    '''
    Summary: 显示user默认密码
    '''
    return {'msg': DEFAULT_USER_PASSWORD}


@router.post('/update-user-config', response_model=MsgResponese)
async def update_user_config(data: UserConfig, cu: UserOrm = Depends(CurrentUser())):
    '''
    Summary: 更新 User Config
    '''
    cu.update(**{'user_config': data.dict()})
    cu.save()
    return {'msg': 'success'}

'''
=============================以下为 chart 信息
1/ project
    - active all count
    - closed all count
    - active 7days count
    - closed 7days count
2/ oem 
    - all count
    - all 7days count 
3/ contact 
    - all count
    - all 7days count
4/ post 
    - me count
    - 7days me count
5/ order 
    - all count
    - all price
    - all me
    - 7days me count 

'''


class TimeFilterPD(BaseModel):
    '''
    Summary: 数据分析筛选
    '''
    # filter_dt_and: dict = None # 这个不从前台获得
    recent_days: int = 0
    start: Optional[Union[datetime.datetime, str]] = None
    end: Optional[Union[datetime.datetime, str]] = None
