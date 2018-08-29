# -*- coding: utf-8 -*-
# @File  : serializer.py
# @Author: huwenxin
# @time: 18-8-28 下午3:42
from rest_framework import serializers

from areas.models import Area


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ('id', 'name')


class SubAreaSerializer(serializers.ModelSerializer):
    # 关联类型   自关联  read_only = True 只读 many = True 一对多的关系
    subs = AreaSerializer(read_only=True, many=True)

    class Meta:
        model = Area
        # fields = ('area_set', 'id', 'name')

        fields = ('subs',)
