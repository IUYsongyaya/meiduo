# -*- coding: utf-8 -*-
# @File  : serializers.py
# @Author: liheng
# @time: 18-8-20 下午8:25

import logging

from django_redis import get_redis_connection
from redis import RedisError
from rest_framework import serializers

logger = logging.getLogger('meiduo')
# serializers.ModelSerializer
# serializers.Serializer
# 选择 ModelSerializer 和 Serializer的区别
# 1. ModelSerializer 自动生成了字段
# 2.ModelSerializer 自动生成了 create和update方法
# 3. ModelSerializer 必须有 Model(模型)

# 图片验证码, uuid
# 没有模型
class RegisterSmscodeSerializer(serializers.Serializer):
    text = serializers.CharField(label='图片验证码', max_length=4,min_length=4, required=True)
    image_code_id = serializers.UUIDField(label='uuid')

    # 序列化器在进行验证的时候至少有4中方案
    # 第一种: 字段类型 UUIDField
    # 第二种: 字段选项 max_length=4,min_length=4
    # 第三种: 单个字段校验  def valide_字段名
    # 第四种: 多个字段校验 def validate

    # def validate_text(self,value):
    #
    #     # 图片验证码比较 是比较用户提交的 和 redis中
    #     # redis中的图片需要通过 image_code_id 获取
    #     # 这个函数中没有 iamge_code_id 所以 需要在多个字段的函数中进行验证
    #
    #     # 为什么返回呢? 因为 用户肯定有输入正确的时候,必须把正确的数据返回
    #     return value
    #attrs 其实他就是data
    def validate(self, data):
        #1.获取用户提交的
        text = data.get('text')
        image_code_id = data.get('image_code_id')
        #2.获取redis中的数据
        redis_conn = get_redis_connection('code')

        redis_text = redis_conn.get('img_%s'% image_code_id)

        #判断获取的redis_text的值
        if redis_text is None:
            raise serializers.ValidationError('图片验证码已经过期')

        #如果已经获取到redis中的数据的话,就可以删掉redis里的数据了
        try:
            redis_conn.delete('img_%s' % image_code_id)
        except RedisError as e:
            logger.error(e)

        # 3. 比较
        # 注意点: redis的数据 是 bytes类型
        #       不区分大小写
        if redis_text.decode().lower() != text.lower():
            raise serializers.ValidationError("图片验证码输入错误")

        return data















