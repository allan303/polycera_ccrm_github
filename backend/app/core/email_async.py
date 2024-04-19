#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2019-11-21
'''
邮件
'''

import logging
import asyncio

import aiosmtplib
from typing import List
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .config import MailConfig as mc


async def send_email_async(title: str = '',
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
    msg['From'] = 'PolyCera'
    # 发送给
    msg['To'] = str(to)
    # 添加到邮件内容中
    msg.attach(content)
    if attach_file:
        # 如果有附件
        att1 = MIMEText(open(attach_file, 'rb').read(), 'base64', 'utf-8')
        att1['Content-Type'] = 'application/octet-stream'
        att1['Content-Disposition'] = 'attachment; filename="report.txt"'
        msg.attach(att1)
    logging.info('开始发送...')
    await aiosmtplib.send(
        message=msg,
        sender=mc.MAIL_USERNAME,
        recipients=[to],
        hostname=mc.MAIL_HOST,
        port=mc.MAIL_PORT,
        username=mc.MAIL_USERNAME,
        password=mc.MAIL_PASSWORD,
        start_tls=True
    )
    logging.info('已经发送!!!')
    # disconnect_email_server(s=s)
    # return status
