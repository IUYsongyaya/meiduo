# -*- coding: utf-8 -*-
# @File  : serializers.py
# @Author: huwenxin
# @time: 18-8-20 下午7:45
import re

from django.core.mail import send_mail
from rest_framework import serializers
from django_redis import get_redis_connection
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from celery_tasks.send_email.tasks import send_email_code
from mell import settings
from users.models import User, Address


class RegisterCreateSerializer(serializers.ModelSerializer):
    # allow_blank 字段是否为空    allow_null 字段是否可以传None
    password2 = serializers.CharField(label='校验密码', allow_null=False, allow_blank=False, write_only=True)
    sms_code = serializers.CharField(label='短信验证码', max_length=6, min_length=6, allow_null=False, allow_blank=False,
                                     write_only=True)
    allow = serializers.CharField(label='是否同意协议', allow_null=False, allow_blank=False, write_only=True)
    # 只能读取  不能写
    token = serializers.CharField(label='token', read_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'mobile', 'sms_code', 'password2', 'allow', 'token')

        # 对表中的字段进行了更改。
        extra_kwargs = {
            'id': {'read_only': True},
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }

    # 进行手机号的验证
    def validate_mobile(self, value):

        if not re.match(r'1[356789]\d{9}', value):
            raise serializers.ValidationError('手机号格式不正确')
        return value

    # 对是否同意协议进行验证
    def validate_allow(self, value):
        # js 的 布尔是小写
        if value != 'true':
            raise serializers.ValidationError('请先同意用户协议')

    # 进行多字段的验证
    def validate(self, attrs):
        # 因为序列化分四步来验证
        # 1.是字段类型
        # 2.字段限制
        # 3.单个字段的验证
        # 4.多个字段的验证
        # 到这里前面都验证完了

        # 短信验证
        redis_conn = get_redis_connection('code')
        redis_sms_code = redis_conn.get('sms_%s' % attrs['mobile'])

        # 判断验证码是否过期
        if redis_sms_code is None:
            raise serializers.ValidationError('短信验证码已经过期')

        # 判断用户验证码是否输入正确
        if attrs['sms_code'] != redis_sms_code.decode():
            raise serializers.ValidationError('验证码输入错误')

        if attrs['password2'] != attrs['password']:
            raise serializers.ValidationError('两次密码输入不一致')

        return attrs

    def create(self, validated_data):
        # 重写create方法，为了是删除多余的字段
        del validated_data['password2']
        del validated_data['sms_code']
        del validated_data['allow']

        # 进行创建和保存
        user = super().create(validated_data)
        # 把密码进行密文处理
        user.set_password(validated_data['password'])
        user.save()

        # 补充并且记录登录状态token
        # JWT_PAYLOAD_HANDLER 写的就是用户的信息
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        # 把user信息写到payload中
        payload = jwt_payload_handler(user)
        # 对payload进行加密`
        token = jwt_encode_handler(payload)
        # 设置token字段
        user.token = token

        return user


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'mobile', 'email', 'email_active')


class AddEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email')
        # 添加字段的限制。限制email字段不能为空
        extra_kwargs = {
            'email': {
                'required': True
            }
        }

    def update(self, instance, validated_data):
        email = validated_data.get('email')
        verify_url = instance.generate_verify_email_url()
        instance.email = validated_data.get('email')
        instance.save()
        send_email_code.delay(email, verify_url)
        return instance


class AddressSerializer(serializers.ModelSerializer):
    province = serializers.StringRelatedField(read_only=True)
    city = serializers.StringRelatedField(read_only=True)
    district = serializers.StringRelatedField(read_only=True)
    province_id = serializers.IntegerField(label='省ID', required=True)
    city_id = serializers.IntegerField(label='市ID', required=True)
    district_id = serializers.IntegerField(label='区ID', required=True)
    mobile = serializers.RegexField(label='手机号', regex=r'^1[3-9]\d{9}$')

    class Meta:
        model = Address
        # exclude 是取反 除了这几个其他的
        exclude = ['user', 'is_deleted', 'create_time', 'update_time']


    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        print(self.context)
        return super().create(validated_data)
