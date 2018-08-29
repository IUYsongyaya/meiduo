# -*- coding: utf-8 -*-
# @File  : urls.py
# @Author: huwenxin
# @time: 18-8-28 下午4:03
from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from areas.views import AreasInfoView

# 注册路由
# 视图集就需要用路由
router = DefaultRouter()
router.register(r'infos', AreasInfoView, base_name='area')
urlpatterns =[

]

urlpatterns += router.urls
