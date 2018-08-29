# -*- coding: utf-8 -*-
# @File  : users.py
# @Author: huwenxin
# @time: 18-8-22 下午4:42
import re

from django.contrib.auth.backends import ModelBackend

from users.models import User


def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    print(user)
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }


def get_user_by_account(username):
    # 判断用户传来的是手机号还是用户名
    try:
        # 优先用户名的情况下
        user = User.objects.get(username=username)
        # 优先手机的情况下
        # if re.match(r'^1[3-9]\d{9}$', username):
        #     user = User.objects.get(mobile=username)
        # else:
        #     user = User.objects.get(username=username)

    # 因为get查询的时候 查不到就会报这个异常
    except User.DoesNotExist:
        try:
            if re.match(r'^1[3-9]\d{9}$', username):
                user = User.objects.get(mobile=username)
            else:
                user = None
        except User.DoesNotExist:
            user = None

    return user


class UsernameMobileAuthBackend(ModelBackend):

    # 重写django自带的验证的方法
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = get_user_by_account(username)

        if user is not None and user.check_password(password):
            return user