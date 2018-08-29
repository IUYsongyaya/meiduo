# -*- coding: utf-8 -*-
# @File  : urls.py
# @Author: huwenxin
# @time: 18-8-19 下午4:37
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

from users.views import AddressView
from . import views

urlpatterns = [
    url(r'usernames/(?P<username>\w{5,20})/count/$', views.RegisterUsernameCountAPIView.as_view()),
    url(r'phones/(?P<phone>\d{11})/count/$', views.RegisterPhoneCountAPIView.as_view()),
    url(r'^$', views.RegisterCreateView.as_view()),
    url(r'^auths/$', obtain_jwt_token, name='auths'),
    # 邮箱视图路由
    url(r'^infos/$', views.UserDetailView.as_view()),
    url(r'^emails/$', views.EmailView.as_view()),
    url(r'^emails/verification/$', views.VerificationEmailView.as_view()),
    # url(r'^addresses/$', views.AddressView.as_view()),
]

router = DefaultRouter()
router.register(r'addresses', AddressView, base_name='address')

urlpatterns += router.urls
