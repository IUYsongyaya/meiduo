# -*- coding: utf-8 -*-
# @File  : tasks.py
# @Author: huwenxin
# @time: 18-8-20 下午5:22

from celery_tasks.main import app



# 可以设置name参数
from libs.yuntongxun.sms import CCP


@app.task
def send_sms_code(mobile, sms_code):
    ccp = CCP()
    ccp.send_template_sms(mobile, [sms_code, 5], 1)
