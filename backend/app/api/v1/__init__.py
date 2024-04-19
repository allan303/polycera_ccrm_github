#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2021-07-03

'''
Summary:  统一的 CRUD router
'''
from typing import Optional, List,  Union
from fastapi import Depends, APIRouter
from starlette.responses import StreamingResponse

from app.core.jwt import CurrentUser
from pydantic import BaseModel
import datetime
from mongoengine.queryset.visitor import Q, QCombination
from jackutils.mongodb_util import paginate
# app
from app.core.jwt import MyExceptions
from app.models.base_model import BaseDocumentNoAttr, BaseDocument
from app.models.base_pd import MsgResponese, SidResponese, IntResponese, BaseListPD
from app.core import config
from app.models.user.models import UserOrm, BaseDocumentOwner
from app.models.utils import merge_to, get_father, get_children
from app.models.oem.models import OemOrm
'''
Summary: List 改成 POST method，方便灵活接受更多参数
'''


class ListQureyData(BaseModel):
    '''
    Summary: 用于 LIST-query的参数
    '''
    scope: str = 'me'
    page: Optional[int] = 1
    per_page: Optional[int] = 20
    keyword: Optional[str] = ''
    order_by: Optional[str] = ''
    desc: Optional[int] = 1  # 是否倒叙
    filter_dt_and: Optional[dict] = None
    start: Optional[datetime.date] = None
    end: Optional[datetime.date] = None
    recent_days: Optional[int] = None
    tpl_name: Optional[str] = None
    context: Optional[dict] = None
    workgroup_sid: Optional[str] = None
    download_many_file_type: str = 'word'


class InsToDocxData(BaseModel):
    '''
    Summary: 用于单个ins下载的参数
    '''
    sid: Optional[str] = None
    tpl_name: Optional[str] = None
    download_option: Optional[dict] = None


def list_query(orm_class: Union[BaseDocumentNoAttr, BaseDocument, BaseDocumentOwner],
               model_name: str,  # 工厂函数中
               #    scope: str = 'me',  # me, total, deleted
               data: ListQureyData = ListQureyData(),
               cu: UserOrm = None):
    '''
    Summary: 普适性的LIST Objs query
    Params:
        orm_class: Mongoengine orm CLASS
        model_name:  project, oem ...
        scope: me OR total
        data: query options
        cu: current user ORM Instance
    '''
    scope = data.scope
    if scope not in ['me', 'total', 'deleted', 'related', 'shared']:
        raise MyExceptions.not_found
    filter_dt_and_force = {}
    # 以下为 对 query 参数的获取,用于 AND 关系的筛选
    exclude_keywords = ['page', 'keyword', '_id',
                        'is_deleted', 'per_page', 'order_by', 'desc']
    if scope == 'me':
        # 权限判定
        if not cu.can(model=model_name, action='read', scope='me'):
            raise MyExceptions.permission_deny
        filter_dt_and_force = {'is_deleted': False, 'owner_sid': cu.sid}
        exclude_keywords.append('owner_sid')  # 对于list-me 必须限定cu sid
    elif scope == 'total':
        # 权限判定
        if not cu.can(model=model_name, action='read', scope='total'):
            raise MyExceptions.permission_deny
        filter_dt_and_force = {'is_deleted': False}
    elif scope == 'deleted':
        # 权限判定
        if not cu.is_su:
            raise MyExceptions.permission_deny
        filter_dt_and_force = {'is_deleted': True}
    elif scope == 'related':
        filter_dt_and_force = {'is_deleted': False}
    elif scope == 'shared':  # 他人分享的
        filter_dt_and_force = {'is_deleted': False,
                               'owner_sid__ne': cu.sid, }
        # 增加一个 or 关系，包含用户sid 或者包含 all
        # filter_dt_or = {'share_list__contains': cu.sid,
        #                 'share_list__contains': 'all'}
    # 加入前端传来的filter条件
    if data.filter_dt_and:
        for k, v in data.filter_dt_and.items():
            if k not in exclude_keywords and v is not None and v != '':
                filter_dt_and_force[k] = v
    # 排序 参数
    order_keywords = orm_class.order_keywords_dict()
    order_by = data.order_by
    if not order_by in order_keywords:
        order_by = 'create_time'  # 默认
    if data.desc:
        order_by = f'-{order_by}'
    else:
        order_by = f'+{order_by}'

    qs = orm_class.get_qs(filter_dt_and=filter_dt_and_force,
                          keyword=data.keyword,
                          start=data.start,
                          end=data.end,
                          recent_days=data.recent_days,
                          order_by=order_by,
                          use_workgroup=True,
                          workgroup_sid=data.workgroup_sid or '',
                          owner_sid=cu.sid)
    if scope == 'shared':
        queries = [Q(share_list='all'), Q(share_list=cu.sid)]
        query = QCombination(QCombination.OR, queries)
        qs = qs.filter(query)
    # Workgroup 限制
    return qs


def list_query_paginate(orm_class: Union[BaseDocumentNoAttr, BaseDocument, BaseDocumentOwner],
                        model_name: str,  # 工厂函数中
                        # scope: str = 'me',  # me, total, deleted
                        data: ListQureyData = ListQureyData(),
                        cu: UserOrm = None):
    '''
    Summary: 加入了Paginate
    '''
    qs = list_query(orm_class=orm_class,
                    model_name=model_name,
                    # scope=scope,
                    data=data,
                    cu=cu)
    objs = list(paginate(qs, per_page=data.per_page, page=data.page))
    return {'objs': objs, 'count_this_page': len(objs), 'count': qs.count()}


def create_crud_routers(router: APIRouter,
                        # 业务逻辑ORM对象
                        orm_class: Union[BaseDocumentNoAttr, BaseDocument, BaseDocumentOwner],
                        create_pd: BaseModel,  # 创建ORM的pd
                        edit_pd: BaseModel,
                        list_pd: BaseListPD,  # response simple pd
                        response_pd: BaseModel,  # 详细response pd
                        perm_list: List[str],  # 要求的权限list
                        model_name: str,
                        cache_name: str,  # 缓存名称
                        router_exclude: List[str] = []
                        ):
    '''
    Summary: 创建统一的CRUD router
    '''
    async def list_paginate(data: ListQureyData = ListQureyData(),
                            cu: UserOrm = Depends(CurrentUser(perms=perm_list))):
        '''
        Summary: current user ， 需要先query 之后 分页
        '''
        return list_query_paginate(orm_class=orm_class,
                                   model_name=model_name,
                                   data=data,
                                   cu=cu)

    async def download_one(sid: str,
                           data: InsToDocxData = InsToDocxData(),
                           cu: UserOrm = Depends(CurrentUser(perms=perm_list))):
        '''
        Summary: 单个ins 下载
        '''
        ins = orm_class.get_by_sid_or_404(sid=sid)
        if not cu.can(model=model_name, action='download_one', obj=ins):
            raise MyExceptions.permission_deny
        filename = f'{ins.name}.docx'
        file = ins.one_to_docx(tpl_name=data.tpl_name,
                               to_file=False,
                               context=data.download_option)
        response = StreamingResponse(content=file)
        response.headers['content-type'] = 'application/x-msdownload'
        response.headers["Content-Disposition"] = "attachment; filename={}".format(
            filename.encode().decode("latin-1")
        )
        return response

    async def download_many(file_type: str = 'word',
                            data: ListQureyData = ListQureyData(),
                            cu: UserOrm = Depends(CurrentUser())):
        '''
        Summary: List Query之后下载报表
        '''
        qs = list_query(orm_class=orm_class,
                        model_name=model_name,
                        data=data,
                        cu=cu)

        if not cu.can(model=model_name, action='download_many', scope=data.scope, qs=qs):
            raise MyExceptions.permission_deny
        filename = f'{model_name}_list'
        # 前台下载时候设置filename,可以调整tpl和context
        if file_type == 'word':
            file = orm_class.many_to_docx(
                qs=qs, tpl_name=data.tpl_name, to_file=False, context=data.context)
        elif file_type == 'excel':
            file = orm_class.many_to_excel(
                qs=qs, to_file=False, pd_class=response_pd)
        else:
            raise MyExceptions.not_found
        response = StreamingResponse(content=file)
        response.headers['content-type'] = 'application/x-msdownload'
        response.headers["Content-Disposition"] = "attachment; filename={}".format(
            filename.encode().decode("latin-1")
        )
        return response

    async def create(data: create_pd,  cu: UserOrm = Depends(CurrentUser(perms=perm_list))):
        '''
        Summary: create
        '''
        if not cu.can(model=model_name, action='create'):
            raise MyExceptions.permission_deny
        ins: BaseDocumentNoAttr = orm_class.create_by_pd(
            pd=data, owner_sid=cu.sid)
        # set owner_sid
        if hasattr(orm_class, 'owner_sid'):
            ins.owner_sid = cu.sid
        ins.api_hook_before_save()
        ins.api_hook_create_before_save()
        ins.save()
        ins.api_hook_after_save()
        ins.api_hook_create_after_save()
        # 更新缓存
        if cache_name in config.MYCACHE:
            config.MYCACHE[cache_name] = orm_class.get_cache()
        if cache_name == 'contact':
            # 可能同时增加 一个 OEM
            config.MYCACHE['oem'] = OemOrm.get_cache()
        # 创建时候可选择 同时创建post，针对 [oem,project,contact,pilot,order] [order_update,project_oem,project_update]
        if not orm_class.__name__ == 'PostOrm':
            from app.models.post.models import PostOrm
        if orm_class.__name__ == 'ProjectOrm':
            PostOrm(owner_sid=cu.sid, project_sid=ins.sid, is_system=True,
                    body=f"[创建新项目]: {ins.name}").save()
        elif orm_class.__name__ == 'OemOrm':
            PostOrm(owner_sid=cu.sid, oem_sid=ins.sid, is_system=True,
                    body=f"[创建新客户]: {ins.name}").save()
        elif orm_class.__name__ == 'ContactOrm':
            PostOrm(owner_sid=cu.sid,
                    contact_sid=ins.sid,
                    oem_sid=ins.oem_sid,
                    is_system=True,
                    body=f"[创建新联系人]: {ins.name}").save()
        elif orm_class.__name__ == 'PilotOrm':
            PostOrm(owner_sid=cu.sid, pilot_sid=ins.sid, is_system=True,
                    body=f"[创建新实验]: {ins.name}").save()
        elif orm_class.__name__ == 'OrderOrm':
            PostOrm(owner_sid=cu.sid,
                    order_sid=ins.sid,
                    project_sid=ins.project_sid,
                    oem_sid=ins.oem_sid,
                    contact_sid=ins.contact_sid,
                    is_system=True,
                    body=f"[创建新订单]: {ins.name}, {ins.oem_name}").save()
        elif orm_class.__name__ == 'OrderUpdateOrm':
            PostOrm(owner_sid=cu.sid,
                    order_sid=ins.order_sid,
                    is_system=True,
                    body=f"[更新订单信息]: {ins.order_name}, 最新状态：{ins.status}").save()
        elif orm_class.__name__ == 'ProjectUpdateOrm':
            PostOrm(owner_sid=cu.sid,
                    project_sid=ins.project_sid,
                    is_system=True,
                    body=f"[更新项目状态]: {ins.project.name}, 最新状态：{ins.pjstage}, {ins.win_percentage}%").save()
        elif orm_class.__name__ == 'ProjectOemOrm':
            PostOrm(owner_sid=cu.sid,
                    project_sid=ins.project_sid,
                    oem_sid=ins.oem_sid,
                    is_system=True,
                    body=f"[添加项目参与客户]: {ins.project.name}, {ins.oem.name}").save()
        elif orm_class.__name__ in 'DesignOrm':
            PostOrm(owner_sid=cu.sid,
                    is_system=True,
                    project_sid=ins.project_sid,
                    oem_sid=ins.oem_sid,
                    body=f"[添加新设计]: {ins.name}").save()
        elif orm_class.__name__ in 'StandardDesignOrm':
            PostOrm(owner_sid=cu.sid,
                    is_system=True,
                    body=f"[添加新标准设计]: {ins.name}").save()
        return {'sid': ins.sid}

    async def read(sid: str, cu: UserOrm = Depends(CurrentUser(perms=perm_list))):
        '''
        read
        '''
        ins = orm_class.get_by_sid_or_404(sid=sid)
        if not cu.can(model=model_name, action='read', obj=ins):
            raise MyExceptions.permission_deny
        return ins

    async def edit(sid: str, data: edit_pd, cu: UserOrm = Depends(CurrentUser(perms=perm_list))):
        '''
        edit：是否要防止 RoleOrm  SU 误操作
        '''
        ins = orm_class.get_active_by_sid_or_404(sid=sid)
        if not cu.can(model=model_name, action='edit', obj=ins):
            raise MyExceptions.permission_deny
        ins.edit_by_pd(pd=data)
        ins.api_hook_before_save()
        ins.api_hook_edit_before_save()
        ins.save()
        ins.api_hook_after_save()
        ins.api_hook_edit_after_save()
        # 更新缓存
        if cache_name in config.MYCACHE:
            config.MYCACHE[cache_name] = orm_class.get_cache()
        return {'sid': ins.sid}

    async def delete_switch(sid: str, cu: UserOrm = Depends(CurrentUser(perms=perm_list))):
        '''
        Summary: 冻结 切换
        '''
        ins = orm_class.get_by_sid_or_404(sid=sid)
        if orm_class.__name__ == 'RoleOrm' and ins.name == config.SU_USERNAME:
            raise MyExceptions.su_not_allowed_edit
        if orm_class.__name__ == 'UserOrm' and ins.role.name == 'su':
            raise MyExceptions.su_not_allowed_edit
        if not cu.can(model=model_name, action='delete', obj=ins):
            raise MyExceptions.permission_deny
        ins = ins.switch_delete()
        # 更新缓存
        if cache_name in config.MYCACHE:
            config.MYCACHE[cache_name] = orm_class.get_cache()
        if ins.is_deleted:
            return {'msg': 'Delete Success'}
        else:
            return {'msg': 'Roll Back Success'}

    async def real_delete(sid: str, cu: UserOrm = Depends(CurrentUser(su_required=True))):
        '''
        Summary:真正删除
        '''
        ins = orm_class.get_by_sid_or_404(sid=sid)
        if orm_class.__name__ == 'RoleOrm' and ins.name == 'su':
            raise MyExceptions.su_not_allowed_edit
        if orm_class.__name__ == 'UserOrm' and ins.role.name == 'su':
            raise MyExceptions.su_not_allowed_edit
        ins.delete()
        return {'msg': 'Deleted'}

    async def real_delete_all(cu: UserOrm = Depends(CurrentUser(su_required=True))):
        '''
        Summary:真正删除
        '''
        if orm_class.__name__ in ['RoleOrm', 'UserOrm']:
            raise MyExceptions.permission_deny
        orm_class.objects().delete()
        return {'msg': 'Deleted All Items '}

    async def real_delete_all_deleted(cu: UserOrm = Depends(CurrentUser(su_required=True))):
        '''
        Summary: 清空所有已删除项
        '''
        orm_class.objects(is_deleted=True).delete()
        return {'msg': 'Cleared All Deleted Objects '}

    async def clone(sid: str, cu: UserOrm = Depends(CurrentUser(perms=perm_list))):
        '''
        clone: 更改： id，updatetime， owner_sid，其他均不变
        条件： hasattr ： owner_sid, is_deleted=False
        '''
        ins = orm_class.get_active_by_sid_or_404(sid=sid)
        # 权限同 read
        if not cu.can(model=model_name, action='clone', obj=ins):
            raise MyExceptions.permission_deny
        if orm_class.__name__ == 'RoleOrm' and ins.name == 'su':
            raise MyExceptions.su_not_allowed_edit
        new_ins = ins.clone()
        if hasattr(orm_class, 'owner_sid'):
            new_ins.owner_sid = cu.sid
            new_ins.save()
        if cache_name in config.MYCACHE:
            config.MYCACHE[cache_name] = orm_class.get_cache()
        return {'sid': new_ins.sid}

    async def assign(sid: str, new_owner_sid: str, cu: UserOrm = Depends(CurrentUser(perms=perm_list))):
        ins = orm_class.get_active_by_sid_or_404(sid=sid)
        if not hasattr(ins, 'owner_sid'):
            raise MyExceptions.not_found
        if not cu.can(model=model_name, action='assign', obj=ins):
            raise MyExceptions.permission_deny
        new_owner = UserOrm.get_active_by_sid_or_404(sid=new_owner_sid)
        old_owner = UserOrm.get_active_by_sid_or_404(sid=ins.owner_sid)

        if not orm_class.__name__ == 'PostOrm':
            from app.models.post.models import PostOrm
        if orm_class.__name__ == 'ProjectOrm':
            PostOrm(owner_sid=cu.sid, project_sid=ins.sid,
                    body=f"[Assign 项目]: {ins.name},{old_owner.name} -> {new_owner.name}",
                    is_system=True).save()
        elif orm_class.__name__ == 'OemOrm':
            PostOrm(owner_sid=cu.sid, oem_sid=ins.sid,
                    body=f"[Assign 客户]: {ins.name},{old_owner.name} -> {new_owner.name}",
                    is_system=True).save()
        elif orm_class.__name__ == 'ContactOrm':
            PostOrm(owner_sid=cu.sid, contact_sid=ins.sid,
                    body=f"[Assign 联系人]: {ins.name},{old_owner.name} -> {new_owner.name}",
                    is_system=True).save()
        elif orm_class.__name__ == 'PilotOrm':
            PostOrm(owner_sid=cu.sid, pilot_sid=ins.sid,
                    body=f"[Assign 实验]: {ins.name},{old_owner.name} -> {new_owner.name}",
                    is_system=True).save()
        elif orm_class.__name__ == 'OrderOrm':
            PostOrm(owner_sid=cu.sid, order_sid=ins.sid,
                    body=f"[Assign 订单]: {ins.name},{old_owner.name} -> {new_owner.name}",
                    is_system=True).save()
        elif orm_class.__name__ in 'DesignOrm':
            PostOrm(owner_sid=cu.sid,
                    body=f"[Assign 设计]: {ins.name},{old_owner.name} -> {new_owner.name}",
                    is_system=True).save()
        elif orm_class.__name__ in 'StandardDesignOrm':
            PostOrm(owner_sid=cu.sid,
                    body=f"[Assign 标准设计]: {ins.name},{old_owner.name} -> {new_owner.name}",
                    is_system=True).save()
        else:
            raise MyExceptions.permission_deny
        ins.owner_sid = new_owner_sid
        ins.owner_name = new_owner.name
        ins.owner_username = new_owner.username
        ins.save()
        return {'msg': f'new owner: {new_owner.name}({new_owner.email})'}

    async def merge(sid: str, new_sid: str, cu: UserOrm = Depends(CurrentUser(perms=perm_list))):
        ins = orm_class.get_by_sid_or_404(sid=sid)
        new_ins = orm_class.get_by_sid(sid=new_sid)
        # 必须对2个ins都进行判断
        if not cu.can(model=model_name, action='merge', obj=ins):
            raise MyExceptions.permission_deny
        if not cu.can(model=model_name, action='merge', obj=new_ins):
            raise MyExceptions.permission_deny
        merge_to(ins=ins, sid=new_sid)

        if not orm_class.__name__ == 'PostOrm':
            from app.models.post.models import PostOrm
        if orm_class.__name__ == 'ProjectOrm':
            PostOrm(owner_sid=cu.sid, project_sid=new_sid,
                    body=f"[Merge 项目]: {ins.name} 合并到 {new_ins.name}",
                    is_system=True).save()
        elif orm_class.__name__ == 'OemOrm':
            PostOrm(owner_sid=cu.sid, oem_sid=new_sid,
                    body=f"[Merge 客户]: {ins.name} 合并到 {new_ins.name}",
                    is_system=True).save()
        elif orm_class.__name__ == 'ContactOrm':
            PostOrm(owner_sid=cu.sid, contact_sid=new_sid,
                    body=f"[Merge 联系人]: {ins.name} 合并到 {new_ins.name}",
                    is_system=True).save()
        elif orm_class.__name__ == 'PilotOrm':
            PostOrm(owner_sid=cu.sid, pilot_sid=new_sid,
                    body=f"[Merge 实验]: {ins.name} 合并到 {new_ins.name}",
                    is_system=True).save()
        else:
            raise MyExceptions.permission_deny
        if model_name in config.MYCACHE:
            config.MYCACHE[model_name] = orm_class.get_cache()
        return {'sid': new_sid}

    # 将endpoint（即处理request的函数）注册到Router上
    if hasattr(orm_class, 'owner_sid'):
        if not 'clone' in router_exclude:
            router.add_api_route(path='/clone/{sid}',
                                 methods=['post'],
                                 endpoint=clone,
                                 response_model=SidResponese,
                                 description='克隆一个对象')
        if not 'assign' in router_exclude:
            router.add_api_route(path='/assign/{sid}/{new_owner_sid}',
                                 methods=['post'],
                                 endpoint=assign,
                                 response_model=MsgResponese,
                                 description='分配，即改变拥有者')
    if not 'list_paginate' in router_exclude:
        router.add_api_route(path='/list-paginate',
                             methods=['post'],
                             endpoint=list_paginate,
                             response_model=list_pd,
                             description='当前用户清单')
    if not 'download_one' in router_exclude:
        router.add_api_route(path='/download-one/{sid}',
                             methods=['post'],
                             endpoint=download_one,
                             description='单个ins下载word')
    if not 'download_many' in router_exclude:
        router.add_api_route(path='/download-many/{file_type}',
                             methods=['post'],
                             endpoint=download_many,
                             description='QueryList下载word')
    if not 'create' in router_exclude:
        router.add_api_route(path='/create',
                             methods=['post'],
                             endpoint=create,
                             response_model=SidResponese,
                             description='创建Create')
    if not 'read' in router_exclude:
        router.add_api_route(path='/read/{sid}',
                             methods=['get'],
                             endpoint=read,
                             response_model=response_pd,
                             description='读取Read')
    if not 'edit' in router_exclude:
        router.add_api_route(path='/edit/{sid}',
                             methods=['post'],
                             endpoint=edit,
                             response_model=SidResponese,
                             description='编辑Edit')
    if not 'merge' in router_exclude:
        router.add_api_route(path='/merge/{sid}/{new_sid}',
                             methods=['post'],
                             endpoint=merge,
                             response_model=SidResponese,
                             description='合并到其他项')
    if hasattr(orm_class, 'is_deleted'):
        if not 'delete_switch' in router_exclude:
            router.add_api_route(path='/delete-switch/{sid}',
                                 methods=['post'],
                                 endpoint=delete_switch,
                                 response_model=MsgResponese,
                                 description='删除切换(假删除)')
        if not 'real_delete_all_deleted' in router_exclude:
            router.add_api_route(path='/real-deleted-all-deleted',
                                 methods=['post'],
                                 endpoint=real_delete_all_deleted,
                                 response_model=MsgResponese,
                                 description='删除所有已删除项')
    if not 'real_delete' in router_exclude:
        router.add_api_route(path='/real-delete/{sid}',
                             methods=['post'],
                             endpoint=real_delete,
                             response_model=MsgResponese,
                             description='真删除')
    # 防止误删，仅dev环境才挂载
    if config.ENV == 'dev':
        router.add_api_route(path='/real-delete-all',
                             methods=['post'],
                             endpoint=real_delete_all,
                             response_model=MsgResponese,
                             description='删除所有项目')
