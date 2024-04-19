import logging

from pymongo import MongoClient
from app.core.config import (
    MONGO_HOST, MONGO_DB,
    MONGO_USER, MONGO_PASS
)
from mongoengine import connect, disconnect


def connect_mongodb():
    logging.info("连接数据库中...")

    connect(
        db=MONGO_DB,
        username=MONGO_USER,
        password=MONGO_PASS,
        host=MONGO_HOST
    )
    logging.info("连接数据库成功！")


def disconnect_mongodb():
    logging.info("关闭数据库连接...")
    disconnect(
        db=MONGO_DB,
        username=MONGO_USER,
        password=MONGO_PASS,
        host=MONGO_HOST
    )
    logging.info("数据库连接关闭！")


QUERY_OPERATORS = 'ne,lt,lte,gt,gte,not,in,nin,mod,all,size,exists,exact,iexact,contains,icontains,startswith,istartwith,endwith,iendwith,match'
QUERY_OPERATORS_LIST = QUERY_OPERATORS.split(',')


def check_mongoengine_operators(*args):
    '''
    Summary: 判定 多个 str 是否为正确的 操作符
    '''
    for x in args:
        if not x in QUERY_OPERATORS_LIST:
            return False
    return True


def mongoengine_handle_filter_dt(filter_dt: dict, fields: dict) -> dict:
    '''
    Summary: 清洗 filter_dt
    NOTE:mongoengine格式
    '''
    # 清洗无效筛选条件，不然会导致结果为[]
    if not filter_dt:
        return {}
    dt = {}
    for k in filter_dt.keys():
        if '__' in k:
            keyls = str(k).split('__')
            # 可能存在 xx__not__mod等操作方式
            k0 = keyls.pop(0)
            if k0 in fields:
                if check_mongoengine_operators(*keyls):
                    dt[k] = filter_dt[k]
        else:
            if k in fields:  # 有效属性
                dt[k] = filter_dt[k]
    filter_dt = dt
    return filter_dt
