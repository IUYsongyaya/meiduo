# -*- coding: utf-8 -*-
# @File  : fdfsstorage.py
# @Author: liheng
# @time: 18-8-31 下午9:08

# 1）需要继承自django.core.files.storage.Storage

from django.core.files.storage import Storage

class MyStorage(Storage):
    """
    自定义文件上传类
    """
    #又任何参数必须放到settings里面

    # def __init__(self, option=None):
    #     if not option:
    #         option = settings.CUSTOM_STORAGE_OPTIONS