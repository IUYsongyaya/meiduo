# -*- coding: utf-8 -*-
# @File  : users.py
# @Author: liheng
# @time: 18-8-23 下午2:47
def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }