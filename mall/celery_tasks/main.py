# -*- coding: utf-8 -*-
# @File  : main.py
# @Author: huwenxin
# @time: 18-8-20 下午5:22


# main 函数用于作为celery的启动文件

from celery import Celery

# 为celery使用django配置文件进行设置
import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'mell.settings'

# 创建Celery对象
# 参数main 设置脚本名

app = Celery('celery_tasks')

# 加载配置文件
app.config_from_object('celery_tasks.config')

# 自动加载任务
app.autodiscover_tasks(['celery_tasks.sms', 'celery_tasks.send_email'])