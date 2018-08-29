# -*- coding: utf-8 -*-
# @File  : users.py
# @Author: liheng
# @time: 18-8-23 下午2:47
# 这个方法 会在我们登录认证成功之后,调用
# 就是为了 扩展 返回多个值的需求
# 默认只返回了一个 token
def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    :param token:  jwt 自动生成的token
    :param user:   我们登录认证成功之后的用户信息
    :param request:
    :return:
    """
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }

"""
1. 当我们在前段输入用户名和密码之后会提交给后端
2. 我们的后端会调用 from django.contrib.auth.backends import ModelBackend 中的验证方法
3.def authenticate(self, request, username=None, password=None, **kwargs):
    这个验证的业务逻辑是 根据用户名 查询 User信息
    如果有User信息 ,则验证密码是否正确
    如果没有User信息,肯定是错误的


明确我们要做的事情
输入用户名或者手机号 都能登录

1. 我们在注册的时候 用户名和手机号是对应的,所以可以用用户名查找的用户肯定可以用手机号查找到
2. 用户名和手机号如何区分?  手机号有规则,用户名一般都是字符串   [不考虑用户名和手机号一致的情况]
3. 重写

"""
from django.contrib.auth.backends import ModelBackend
import re
from users.models import User

def get_user_by_account(account):
    #根据正则来判断是手机号还是用户名
    try:
        if re.match('1[3-9]\d{9}', account):
            user = User.objects.get(mobile=account)
            # 满足手机号我们就认为是 手机号
            # 根据手机号查询信息
        else:
            #这里get获取的是单个对象,如果查询不到会报异常,所以需要捕获一下
            user = User.objects.get(username=account)

    except User.DoesNotExist:
        user = None

    return user

class UserMobileUserName(ModelBackend):

    #
    def authenticate(self, request, username=None, password=None, **kwargs):
        # 自定义用户名或手机号认证
        # authenticate:认证,鉴定,证明
        # 1. 根据用户输入的 username 来判断 是手机号还是 用户名
        # 2. 获取用户信息
        user = get_user_by_account(username)
        # 3. 根据用户信息判断密码
        #check_pasword 会把前端传过来的密码进行 sha256 加密
        if user is not None and user.check_password(password):
            return user
        # 用户信息不为None,而且密码校验正确,则返回用户信息
        else:
            return None
