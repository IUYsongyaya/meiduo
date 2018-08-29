# -*- coding: utf-8 -*-
# @File  : urls.py
# @Author: huwenxin
# @time: 18-8-23 下午4:03
from django.conf.urls import url

from oauth import views

urlpatterns = [
    # /oauth/qq/statues/
    url(r'^qq/statues/$', views.QQAuthURLView.as_view()),

    url(r'^qq/users/$', views.QQTokenView.as_view()),
]