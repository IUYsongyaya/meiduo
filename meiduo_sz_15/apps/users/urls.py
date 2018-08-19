# -*- coding: utf-8 -*-
# @File  : urls.py
# @Author: liheng
# @time: 18-8-19 下午8:02
from django.conf.urls import url

from . import views


urlpatterns =  [
    #/users/usernames/(?P<username>\w{5,20})/count/,
url(r'^usernames/(?P<username>\w{5,20})/count/$',views.RegisterUsernameCountAPIView.as_view(),name='usernamecount'),
]
