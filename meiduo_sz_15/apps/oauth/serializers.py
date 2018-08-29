# -*- coding: utf-8 -*-
# @File  : serializers.py
# @Author: liheng
# @time: 18-8-25 下午4:32
from django_redis import get_redis_connection
from rest_framework import serializers

# serializers.ModelSerializer
# serializers.Serializer
from  users.models import User
from .models import OAuthQQUser


class QQTokenSerialzier(serializers.Serializer):
    """   明确你的需求,分析已知条件, 根据已知条件,创建实现的步骤
       1. 前段应该将 短信,密码和手机号 以及 access_token(openid)的信息 传递给我们
       2. 后端接受到数据之后,对数据进行校验
       3.  user信息??? 我们根据手机号来判断
       4. 我们需要将 openid 和 user信息保存(绑定)起来
   """
    access_token = serializers.CharField(label='操作token')
    mobile = serializers.RegexField(label='手机号', regex=r'^1[345789]\d{9}$')
    password = serializers.CharField(label='密码', max_length=20, min_length=8)
    sms_code = serializers.CharField(label='短信验证码', max_length=6, min_length=6)

    def validate(self, attrs):
        #校验
        print('attrs的值:%s' % attrs)
        # 1.校验token(openid)
        access_token= attrs.get('access_token')
        # 在哪里解密的就在哪里解密
        openid = OAuthQQUser.openid_by_token(access_token)
        if openid is None:
            raise serializers.ValidationError('openid不正确')
        # 把openid传递到 attrs字典中,当进行create的方法的时候 validated_data 就有这个数据了
        attrs['openid'] = openid

        #2.校验短信验证码
        #2.1链接redis数据库
        mobile = attrs.get('mobile')
        sms_code = attrs.get('sms_code')
        redis_conn = get_redis_connection('code')
        #2.2获取数据
        redis_code = redis_conn.get('sms_%s' % mobile)
        if redis_conn is None:
            return serializers.ValidationError('短信验证码已经过期了')
        #2.3比较
        if sms_code != redis_code.decode():
            return serializers.ValidationError('短信验证码输入有误')


        #3.根据手机号,查询用户信息
        try:
            #这里 TODO '这里会出现查询两条openid一样的数据,报错查询错误'
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            # 说明是一个没有注册的用户
            # 没有注册的用户应该给它创建一个用户,创建用户的代码 写到 create方法中
            attrs['user'] = None
        else:
            # 说明是一个已经注册的用户
            # 我们需要对密码进行校验,
            if not user.check_password(attrs['password']):
                raise serializers.ValidationError('密码输入有误')
            attrs['user'] = user

        return attrs

    def create(self, validated_data):
        # validated_data
        # 已经校验过之后的数据,这个数据的前身是 data --> attrs --> validated_data
        """
        1. 没有注册的用户应该给它创建一个用户,创建用户的代码 写到 create方法中
        2. 要将 openid 和 user信息保存
        """
        #1.获取用户信息
        user = validated_data.get('user')
        #2.判断用户信息是否存在:
        if user is None:
            #不存在就创建
            user = User.objects.create(
                username=validated_data.get('mobile'),
                password=validated_data.get('password'),
                mobile=validated_data.get('mobile'),
            )
            # 密码还是明文
            user.set_password(validated_data['password'])
            user.save()

        OAuthQQUser.objects.create(
            user=user,
            openid=validated_data.get('openid')
        )

        return user

