# -*- coding: utf-8 -*-
# @File  : tasks.py
# @Author: liheng
# @time: 18-8-21 上午11:39
# 1.我们需要实现对应的任务,
# 2.这个任务需要被celery实例对象的 task装饰器装饰
from celery_tasks.main import app
from libs.yuntongxun.sms import CCP

# @app.task
# name 就是任务的名字 可以不设置,采用默认的
@app.task(name='aaaa')
def send_sms_code(mobile, sms_code):
    # 任务就是发送短信
    ccp = CCP() # mobile:向谁发 []:发什么, 5/分钟:过期时间, 1:模板  ,
    ccp.send_template_sms(mobile, [sms_code, 5], 1)
    print()