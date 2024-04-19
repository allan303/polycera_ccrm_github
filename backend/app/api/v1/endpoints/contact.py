#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-09-11


from fastapi import APIRouter, File, UploadFile, Depends
import pandas as pd
# app level
from app.models.base_pd import MsgResponese
from app.models.contact.models import ContactOrm
from app.models.contact.schemas import ContactCreatePD, ContactPD, ContactSimplePD, ContactListPD
from app.api.v1 import create_crud_routers
from app.models.oem.models import OemOrm
from app.core.jwt import CurrentUser
from app.models.user.models import UserOrm
from app.core.errors import MyExceptions

router = APIRouter(prefix='/contact',
                   tags=['contact'])

# 此函数创建了 所有标准CRUD
create_crud_routers(
    router=router,
    orm_class=ContactOrm,
    create_pd=ContactCreatePD,
    edit_pd=ContactCreatePD,
    list_pd=ContactListPD,
    response_pd=ContactPD,
    perm_list=['contact'],
    model_name='contact',
    cache_name='contact',
    router_exclude=['download_one', 'download_many']
)


@router.post('/insert-by-excel')
# , cu: UserOrm = Depends(CurrentUser())):
async def insert_by_excel(file: UploadFile = File(...), cu: UserOrm = Depends(CurrentUser())):
    filename = file.filename
    ext = str(filename).split('.')[-1]
    if str(ext).lower() not in ['xlsx', 'xls']:
        raise MyExceptions.wrong_file_type
    # file.seek(0)
    df = pd.read_excel(file.file._file)
    df.fillna('')
    ls = list(df.T.to_dict().values())  # 转换为List[Dict]
    i = []
    ei = []
    for dt in ls:
        try:
            p = ContactCreatePD(**dt)
            ins = ContactOrm.create_by_pd(pd=p, owner_sid=cu.sid)
            ins.save()
            i.append(p.name or '无姓名')
        except Exception as e:
            ei.append(p.name or '无姓名')
            print(e)
    return {"i": i, 'ei': ei}
