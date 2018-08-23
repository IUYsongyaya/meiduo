# -*- coding: utf-8 -*-
# @File  : main.py
# @Author: liheng
# @time: 18-8-21 上午11:40
# tasks --> broker(redis) --> worker
#1.我们需要告诉celery我们当前的django配置文件在哪里
import os

from celery import Celery

if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'meiduo_sz_15.settings'
# 2. 创建celery实例对象
# Celery的第一个参数 : 习惯设置为 celery的脚本路径, 确保celery的唯一的就可以
app = Celery(main='celery_tasks')
# 3. 让celery实例对象 加载配置信息 来实现 broker的设置
app.config_from_object('celery_tasks.config')
# 4. 让celery实例对象自动检测任务
# [] 列表的任务 需要是 任务的路径
app.autodiscover_tasks(['celery_tasks.sms'])

# worker 只需要使用指令,在我们的虚拟环境中运行就可以
# celery -A celery main(实例对象的脚本路径) worker -l info

# celery -A celery_tasks.main worker -l info