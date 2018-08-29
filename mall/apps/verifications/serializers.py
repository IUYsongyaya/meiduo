# -*- coding: utf-8 -*-
# @File  : serializers.py
# @Author: huwenxin
# @time: 18-8-20 下午3:55
from rest_framework import serializers
from django_redis import get_redis_connection

class RegisterSMSCodeSerializer(serializers.Serializer):

    """
    创建验证的字段
    """

    text = serializers.CharField(label='用户输入的验证码', max_length=4, min_length=4, required=True)
    image_code_id = serializers.UUIDField(label='验证码的唯一性ID')

    def validate(self, attrs):
        """
        重写validate对字段进行验证
        :param attrs:
        :return:
        """
        text = attrs.get('text')
        image_code_id = attrs.get('image_code_id')

        # 链接redis去出验证信息
        redis_conn = get_redis_connection('code')
        redis_text = redis_conn.get('img_%s' % image_code_id)

        if redis_text is None:
            raise serializers.ValidationError('验证码已经过期')

        if text.lower() != redis_text.decode().lower():
            raise serializers.ValidationError('验证码输入错误')

        return attrs