#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2021-11-28
'''
Summary: update version
'''

if __name__ == '__main__':
    from mongoengine import connect, disconnect
    from app.core import config
    from app.manage import update_version
    disconnect()
    connect(config.MONGO_DB)
    update_version()
