# -*- coding: utf-8 -*-
# @File  : tasks.py
# @Author: liheng
# @time: 18-8-26 下午5:53
from celery_tasks.main import app
from django.core.mail import send_mail   #django自带的发邮件的模块
from meiduo_sz_15 import settings


@app.task(name='send_verify_mail')
def send_verify_mail(to_email,verify_url):
    subject = '美多商城邮箱验证'
    html_message = '<p>尊敬的用户您好！</p>' \
                   '<p>感谢您使用美多商城。</p>' \
                   '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                   '<p><a href="%s">%s<a></p>' % (to_email, verify_url, verify_url)
    send_mail(subject, "", settings.EMAIL_FROM, [to_email], html_message=html_message)


