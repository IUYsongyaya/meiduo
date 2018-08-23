from django.shortcuts import render

# Create your views here.
# GET /users/usernames/(?P<username>\w{5,20})/count/
#创建路由
from rest_framework.response import Response
from rest_framework.views import APIView

# from apps.users.models import User
from .serializers import RegisterUserSerializer
from .models import User

# APIView
# GenericAPIView
# ListAPIView,RetrieveAPIView


class RegisterUsernameCountAPIView(APIView):
    """
    获取用户个数
    当光标移动之后,前段需要将用户名发送给我们后端,我们后端根据前段提交的用户名进行数据的查询
    如果数据存在 则表示已经注册
    如果数据不存在 则表示没有注册
    """
    def get(self, request, username):
        #通过模型查询,获取用户个数
        """
        我们后端根据前段提交的用户名进行数据的查询
        查询的数量
        如果数据存在 则表示已经注册
        如果数据不存在 则表示没有注册
        """
        count = User.objects.filter(username=username)
        context = {
            'count':count,
            'username':username
        }
        return Response(context)

class RegisterPhoneCountAPIView(APIView):
    """
    查询手机号的个数
    GET: /users/phones/(?P<mobile>1[345789]\d{9})/count/
    """

    def get(self, request, mobile):
        count = User.objects.filter(mobile=mobile).count()

        context = {
            'count': count,
            'phone': mobile,
        }

        return Response(context)

# APIView
# GenericAPIView  --- 是否用到序列化器
# CreateAPIView
class RegisterUsername(APIView):
    """
    post  /users/

    前端把数据提交给后端,我们进行校验,然后对关键参数入库
    1.前段需要把用户名,密码,确认密码,短信,是否同意我们后端为了安全
      考虑,也让前段发送过来
    2.后端接受数据,我们需要对数据进行校验
    3.校验没问题就入库
    """
    def post(self, request):
        #只要用到序列化器,返回的user就会携带token信息,因为token字段已经定义了在了序列化操作里面
        serializer = RegisterUserSerializer(data=request.data)

        #进行校验
        serializer.is_valid(ValueError=True)
        print(serializer.is_valid())

        #保存数据(会调用create方法)
        serializer.save()

        #序列化的操作,将User信息转换为JSON
        return Response(serializer.data)


# 用户注册完成之后,就认为登录了
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
# # 第二级视图 GenericAPIView
# class RegisterUserView(CreateModelMixin,GenericAPIView):
#     """
#     POST        /users/
#     前端把数据提交给后端,我们后端进行数据的校验,然后数据入库
#
#
#     1. 前端必须把用户名,密码和手机号发送过来, 确认密码,短信,是否同意我们后端为了安全考虑,也让前端
#         发送过来
#     2.后端接受这些数据,我们需要对数据进行校验
#     3. 校验没有问题就入库
#
#     """
#
#     serializer_class =  RegisterUserSerializer
#
#     def post(self, request):
#
#
#         return self.create(request)


# from rest_framework.generics import CreateAPIView
# # 视图的第三级 (抽取)
# class RegisterUserView(CreateAPIView):
#     serializer_class = RegisterUserSerializer



# from users.serialziers import RegisterUserSerializer






















