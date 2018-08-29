# -*- coding: utf-8 -*-
# @File  : serializers.py
# @Author: huwenxin
# @time: 18-8-25 下午2:41
from rest_framework import serializers

from oauth.models import OAuthQQUser
from django_redis import get_redis_connection

from users.models import User


class QQTokenSerializer(serializers.Serializer):
    # 绑定用户信息所需要的字段
    access_token = serializers.CharField(label='操作token')
    mobile = serializers.RegexField(label='手机号', regex=r'^1[345789]\d{9}$')
    password = serializers.CharField(label='密码', max_length=20, min_length=8)
    sms_code = serializers.CharField(label='短信验证码', max_length=6, min_length=6)

    def validate(self, attrs):

        # 对字段进行验证   access_token 就是加密的openid
        openid = OAuthQQUser.check_openid(attrs['access_token'])

        if openid is None:
            raise serializers.ValidationError('无效的token')

        attrs['openid'] = openid

        # 检查手机验证码
        # 获取链接
        redis_conn = get_redis_connection('code')
        redis_sms_code = redis_conn.get('sms_%s' % attrs['mobile'])

        if not redis_sms_code:
            raise serializers.ValidationError('短信验证码过期')

        if attrs['sms_code'] != redis_sms_code.decode():
            raise serializers.ValidationError('短信验证码错误')

        # 判断用户是否注册过
        try:
            user = User.objects.get(mobile=attrs['mobile'])
        except User.DoesNotExist:
            # 用户不存在 就是没有注册过 进行注册
            user = None
            attrs['user'] = user
        else:
            # 用户存在就是注册过的  进行绑定
            # 对密码进行验证
            if not user.check_password(attrs['password']):
                raise serializers.ValidationError('密码错误')

            # 进行绑定
            # 在这里保存也行， 在create里面保存也行

            attrs['user'] = user

        return attrs

    def create(self, validated_data):
        # 数据的转换
        # request.query_params => attrs => validated_data

        # 判断user是否为注册过的
        user = validated_data['user']
        if user is None:
            # 没注册的用户先进行注册
            user = User.objects.create(
                username=validated_data['mobile'],
                mobile=validated_data['mobile'],
                password=validated_data['password']
            )
            # 对密码进行密文保存
            user.set_password(validated_data['password'])
            user.save()

        # 把user存到OAuthQQUser表里  进行绑定
        OAuthQQUser.objects.create(
            openid=validated_data['openid'],
            user=user
        )
        # 返回
        return user
