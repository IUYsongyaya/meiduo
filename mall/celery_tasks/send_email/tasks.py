# -*- coding: utf-8 -*-
# @File  : tasks.py
# @Author: huwenxin
# @time: 18-8-26 下午4:57
from django.core.mail import send_mail

from celery_tasks.main import app
from mell import settings


@app.task(name='send_email_code')
def send_email_code(email, verify_url):
    """
    send_mail : 是django中自带
    subject :   是主题

    """
    subject = '主题'
    message = '发送内容'
    html_message = '<p>尊敬的用户您好！</p>' \
                   '<p>感谢您使用美多商城。</p>' \
                   '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                   '<p><a href="%s">%s<a></p>' % (email, verify_url, verify_url)
    # from_email 邮箱是那个发的
    # recipient_list  需要发送的列表
    send_mail(subject=subject, message='', from_email=settings.EMAIL_FROM, recipient_list=[email],
              html_message=html_message)
