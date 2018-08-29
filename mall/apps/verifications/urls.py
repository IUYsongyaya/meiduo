# -*- coding: utf-8 -*-
# @File  : urls.py
# @Author: huwenxin
# @time: 18-8-19 下午8:25
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^imagecodes/(?P<image_code_id>.+)/$', views.RegisterImageCodeView.as_view()),

    # 手机验证的路由
    url(r'^smscodes/(?P<mobile>1[356789]\d{9})/$', views.RegisterSMSCodeView.as_view()),
]