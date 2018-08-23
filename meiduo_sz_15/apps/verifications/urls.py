# -*- coding: utf-8 -*-
# @File  : urls.py
# @Author: liheng
# @time: 18-8-19 下午9:31
from django.conf.urls import url
from . import views

urlpatterns = {

    #正则会
    url(r'^imagecodes/(?P<image_code_id>.+)/', views.RegisterImageCodeView.as_view(), name='imagecode'),
    # GET /verifications/smscodes/(?P<mobile>1[345789]\d{9})/?text=xxxx & image_code_id=xxxx
    url(r'^smscodes/(?P<mobile>1[345789]\d{9})/', views.RegisterSMSCodeView.as_view(), name='smscode'),

}