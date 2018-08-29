from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from areas.models import Area
from areas.serializer import AreaSerializer, SubAreaSerializer


class AreasInfoView(CacheResponseMixin, ReadOnlyModelViewSet):
    # CacheResponseMixin 为缓存
    # ReadOnlyModelViewSet 为视图集
    # 分页设置
    pagination_class = None

    def get_queryset(self):
        # 重写get_queryset 根据动作来返回字段
        if self.action == 'list':
            # 返回指定的字段  是省的字段
            return Area.objects.filter(parent=None)
        else:
            # 把所有的字段都返回 这个就是另内的查询
            return Area.objects.all()

    def get_serializer_class(self):

        # 根据请求的动作来返回指定的序列化器
        if self.action == 'list':
            return AreaSerializer
        else:
            return SubAreaSerializer
