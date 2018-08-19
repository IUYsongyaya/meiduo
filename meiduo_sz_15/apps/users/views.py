from django.shortcuts import render

# Create your views here.
# GET /users/usernames/(?P<username>\w{5,20})/count/
#创建路由
from rest_framework.response import Response
from rest_framework.views import APIView

# from apps.users.models import User
from .models import User


class RegisterUsernameCountAPIView(APIView):
    """
    获取用户个数

    """
    def get(self, request, username):
        #通过模型查询,获取用户个数
        count = User.objects.filter(username=username).count()
        #组织数据
        context = {
            'count' : count,
            'username' :username
        }
        return Response(context)