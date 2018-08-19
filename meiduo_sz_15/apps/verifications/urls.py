# -*- coding: utf-8 -*-
# @File  : urls.py
# @Author: liheng
# @time: 18-8-19 下午9:31
from django.conf.urls import url
from . import views

urlpatterns = {
    url(r'^imagecodes/(?P<image_code_id>).+/', views.RegisterImageCodeView.as_view(), name='imagecode'),
}