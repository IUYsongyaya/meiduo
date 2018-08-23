# -*- coding: utf-8 -*-
# @File  : urls.py
# @Author: liheng
# @time: 18-8-23 下午5:58
from django.conf.urls import url
from . import views

urlpatterns = [
    #   /oauth/qq/statues/
    url(r'^qq/statues/$', views.QQOauthURLView.as_view(), name='statues'),
    #  /oauth/qq/users/
    url(r'qq/users/$', views.QQTokenView.as_view(), name='users'),

]