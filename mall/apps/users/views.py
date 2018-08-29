from django.shortcuts import render

# Create your views here.
from rest_framework import mixins
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from users.serializers import RegisterCreateSerializer, UserDetailSerializer, AddEmailSerializer, AddressSerializer
from .models import User, Address


class RegisterUsernameCountAPIView(APIView):
    def get(self, request, username):
        """"
        /user/username/?P<username>/count/
        """

        # 根据前段传来的名字进行数据查询
        # 如果为0 就是数据库里面没有这条数据可以进行注册
        # 如果为1 就是数据库里面有这条数据了

        count = User.objects.filter(username=username).count()

        data = {
            'count': count,
            'username': username,
        }

        return Response(data=data)


class RegisterPhoneCountAPIView(APIView):
    def get(self, request, phone):
        print('手机 get 请求')
        """
        /users/phones/(?P<phone>\d{11})/count/
        :param request:
        :param phone:
        :return:
        """

        count = User.objects.filter(mobile=phone).count()
        data = {
            'count': count,
            'phone': phone,
        }

        return Response(data=data)


class RegisterCreateView(APIView):
    # serializer_class = RegisterCreateSerializer

    # def post(self, request):
    #     print(111)
    #     # serializer = RegisterCreateSerializer(data=request.data)
    #     # serializer.is_valid()
    #     # serializer.save()
    #     return self.create(request)

    def post(self, request):
        print('post 请求')
        serializer = RegisterCreateSerializer(data=request.data)
        serializer.is_valid()
        serializer.save()

        return Response({'message': 'ok'})


class UserDetailView(GenericAPIView):

    # 权限限制， IsAuthenticated只能登录访问
    permission_classes = [IsAuthenticated]


    def get(self, request):
        user = request.user
        # instance = user 根据字段来查询模型类
        serializer = UserDetailSerializer(instance=user)
        return Response(serializer.data)

# class UserDetailView(RetrieveAPIView):
#
#     permission_classes = [IsAuthenticated]
#
#     serializer_class = UserDetailSerializer
#
#     def get_object(self):
#         return self.request.user

# users/emails/
# class EmailView(APIView):
#     # 自己写的
#     permission_classes = [IsAuthenticated]
#     def put(self, request):
#
#         # 更新数据 添加邮箱
#         user = request.user
#         # serializer (instance 是装user装换成序列化器的东西，  data 就是数据
#         # request.data 接收页面传来的接送josn数据
#         serializer = AddEmailSerializer(user,data=request.data)
#
#         serializer.is_valid()
#         # 如果是新的数据会调用create 不是新的就调用update
#         serializer.save()
#
#         return Response({'message': 'ok'})

class EmailView(UpdateAPIView):
    # 权限控制   允许登录的人才能进入
    permission_classes = [IsAuthenticated]

    serializer_class = AddEmailSerializer

    def get_object(self):
        # get_object 返回的是pk 现在指定返回的是对象
        # 因为页面上没有传pk
        return self.request.user


class VerificationEmailView(APIView):
    # / users / emails / verification /?token = xxxx

    def get(self, request):
        # 获取get请求
        token = request.query_params.get('token')

        # token 不存在的时候
        if not token:
            return Response({'message':'缺少token'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.check_verify_email_token(token)

        # 判断user 不为空的时候
        if user is None:
            return Response({'message': '链接无效'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.email_active = True
            user.save()
            return Response({'message': 'ok'})


# GenericAPIView
# class AddressView(CreateModelMixin, GenericAPIView):
#
#     # serializer_class = AddressSerializer
#     permission_classes = [IsAuthenticated]
#
#     # def create(self, request, *args, **kwargs):
#     #     return super().create(request, *args, **kwargs)
#
#     def post(self, request):
#         # {'city_id': 130500, 'title': 'xzxcxzcxz', 'receiver': 'xzxcxzcxz', 'tel': '',
#         # 'district_id': 130525, 'place': 'zxczxczxczx', 'email': '', 'mobile': '13333333333', 'province_id': 130000}
#         print(request.data)
#         serializer = AddressSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({'message': 'ok'})
#
#     def get(self, request):
#
#         # 查询已有的地址
#         address = Address.objects.filter(is_deleted=False)
#         print(address)
#         return Response(address)

class AddressView(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,GenericViewSet):

    serializer_class = AddressSerializer

    permission_classes = [IsAuthenticated]

    # 重写查询集  查询的只删除的
    def get_queryset(self):
        return self.request.user.addresses.filter(is_deleted=False)

    def create(self, request, *args, **kwargs):
        count = request.user.addresses.count()

        if count >= 20:
            return Response({'message':'保存地址数量已经达到上限'},status=status.HTTP_400_BAD_REQUEST)

        return super().create(request,*args,**kwargs)






