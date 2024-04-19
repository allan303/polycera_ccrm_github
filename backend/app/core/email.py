#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2019-11-21
'''
邮件
'''

import logging


import smtplib
from typing import List
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .config import MailConfig as mc


# 全局邮箱服务器instance


def connect_email_server() -> smtplib.SMTP:
    '''
    Summary: 与邮件服务器进行连接（防止每次发送都就进行一次登录和退出）
    Return : 已经登录的STMP Instance
    '''
    # 建立连接
    # python3.7版本开始，在SMTP建立阶段就要指明host地址，3.7之前不需要
    logging.info('连接EMAIL服务器...')
    s = smtplib.SMTP(host=mc.MAIL_HOST, port=mc.MAIL_PORT)
    s.connect(host=mc.MAIL_HOST, port=mc.MAIL_PORT)
    # 网站需要安全认证时添加
    #     s.ehlo()
    s.starttls()  # port = 587说明需要TSL连接  此时需要加这行代码
    # 登录发送邮件账户
    s.login(mc.MAIL_USERNAME, mc.MAIL_PASSWORD)
    logging.info('连接EMAIL服务器成功（SUCCESS）！')
    return s


async def disconnect_email_server(s: smtplib.SMTP):
    '''
    Summary: 邮件服务器退出
    '''
    logging.info('断开EMAIL SERVER中...')
    try:
        s.close()
    except Exception as e:
        print(e)
        logging.info('断开EMAIL SERVER（ERROR）！')
    logging.info('断开EMAIL SERVER！')


async def send_email(title: str = '',
                     message: str = '',
                     to: str = '',
                     attach_file: str = None,
                     mode='plain'):
    '''
    Summary: 发送邮件，初始配置在总体CONFIG中
    paras  : 
        - title 邮件主题
        - message 正文内容
        - receivers： List[str] 收件人
    '''
    # s = connect_email_server()
    if not to:
        logging.info('没有邮件收件人。')
        return None
    # 内容 class
    msg = MIMEMultipart()
    # 文本信息
    content = MIMEText(message, mode, 'utf-8')
    # 主题
    msg['Subject'] = f'{title}'
    # 来自
    msg['From'] = 'PolyCera 聚瓷上海'
    # 发送给
    msg['To'] = str(to)
    # 添加到邮件内容中
    msg.attach(content)
    status = None
    if attach_file:
        # 如果有附件
        att1 = MIMEText(open(attach_file, 'rb').read(), 'base64', 'utf-8')
        att1['Content-Type'] = 'application/octet-stream'
        att1['Content-Disposition'] = 'attachment; filename="report.txt"'
        msg.attach(att1)
    try:
        email_server = connect_email_server()
        email_server.sendmail(from_addr=mc.MAIL_USERNAME,
                              to_addrs=[to], msg=msg.as_string())
        status = 'success'
        logging.info('Email 发送成功！')
    except smtplib.SMTPException as e:
        print(e)
        logging.info('Email 发送失败...')
        status = str(e)
    await disconnect_email_server(s=email_server)
    return status
    # disconnect_email_server(s=s)
    # return status
