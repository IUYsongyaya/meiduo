# -*- coding: utf-8 -*-
# @File  : models.py
# @Author: liheng
# @time: 18-8-23 下午4:43
from django.db import models

# 我们期望以后的表 继承自这个类,每个表都添加2个字段
class BaseModel(models.Model):
    """为模型类补充字段"""
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        abstract = True  # 说明是抽象模型类, 用于继承使用，数据库迁移时不会创建BaseModel的表