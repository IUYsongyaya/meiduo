# -*- coding: utf-8 -*-
# @File  : urls.py
# @Author: liheng
# @time: 18-8-19 下午8:02
from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from . import views
# from users import views


urlpatterns =  [
    #/users/usernames/(?P<username>\w{5,20})/count/,
    url(r'^usernames/(?P<username>\w{5,20})/count/$',views.RegisterUsernameCountAPIView.as_view(),name='usernamecount'),
    url(r'^phones/(?P<mobile>1[3456789]\d{9})/count/$', views.RegisterPhoneCountAPIView.as_view(),name='phonecount'),
    url(r'^$', views.RegisterUsername.as_view()),
    # users/auths/
    url(r'^auths/',obtain_jwt_token),

    #users/infos/  404 多为路径找不到
    url(r'^infos/$', views.UserDetailView.as_view(), name='detail'),

    #users/emails/
    url(r'^emails/$', views.EmailView.as_view(), name='send_mail'),

    #users/emails/verification/?token=xxx
    url(r'^emails/verification/$', views.VerificationEmailView.as_view(), name='verify_email')
]
#eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.      header
# eyJ1c2VybmFtZSI6Iml0Y2FzdCIsImV4cCI6MTUzNDk5NDQ3NywidXNlcl9pZCI6NiwiZW1haWwiOiIifQ.
# _N6trZw1YlJPhl5slmCpseFKKTgmq23gaiqn4AaGz2k
#
