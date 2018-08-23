from urllib.parse import urlencode, parse_qs
from urllib.request import urlopen

from django.conf import settings
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .utils import OauthQQ

"""
urllib.parse.urlencode(query)
将query字典转换为url路径中的查询字符串

urllib.parse.parse_qs(qs)
将qs查询字符串格式数据转换为python的字典

urllib.request.urlopen(url, data=None)
发送http请求，如果data为None，发送GET请求，如果data不为None，发送POST请求
返回response响应对象，可以通过read()读取响应体数据，需要注意读取出的响应体数据为bytes类型
"""

# Create your views here.

#APIView
#GenericAPIView         ----- 用到序列化器的话,就用这个
#ListAPIView,RetrieveAPIView

# from .utils import OauthQQTool

class QQOauthURLView(APIView):
    """
        GET     /oauth/qq/statues/
        1.前端根据用户的点击,发送一个 ajax 请求来获取 后端拼接好的url
        2. 我们要根据 qq的接口文档 生成一个url
        3. 把这个url返回回去
    """
    def get(self, request):
        """
        # 生成auth_url
        # https://graph.qq.com/oauth2.0/authorize
        # 请求参数请包含如下内容：
        # response_type   必须      授权类型，此值固定为“code”。
        # client_id       必须      申请QQ登录成功后，分配给应用的appid。
        # redirect_uri    必须      成功授权后的回调地址，必须是注册appid时填写的主域名下的地址，建议设置为网站首页或网站的用户中心。注意需要将url进行URLEncode。
        # state           必须      client端的状态值。用于第三方应用防止CSRF攻击，成功授权后回调时会原样带回。请务必严格按照流程检查用户与state参数状态的绑定。
        # scope           可选      scope=get_user_info
        """
        # #1. base_url
        # # GET www.baidu.com/a.html?a=xxx&b=xxx
        # # ? 是为了将路径和参数进行分割

        # base_url = 'https://graph.qq.com/oauth2.0/authorize?'
        # #
        # # # 2. 将参数放在字典中
        # params = {
        #     'response_type':'code',
        #     'client_id':settings.QQ_APP_ID,
        #     'redirect_uri':settings.QQ_REDIRECT_URL,
        #     'state':'test',
        # }
        # #
        # # 3.
        # #将query字典转换为url路径中的查询字符串
        # auth_url = base_url + urlencode(params)
        # print('这是拼接好的url地址: %s' % auth_url)
        # 返回响应

        qq = OauthQQ()
        auth_url = qq.get_auth_url()

        return Response({'auth_url':auth_url})
# APIView
# GenericAPIView         ----- 序列化器
# ListAPIView,RetrieveAPIView
class QQTokenView(APIView):
    """
       GET     /oauth/qq/users/?code=xxxxx
       1. 前端 通过一定的方式获取到用户扫描之后,qq返回的code
       2. 我们后台接收到这个code之后 用code换取token,
       3. 看接口文档实现对应的功能
    """
    def get(self, request):
        #1. 获取code
        code = request.query_params.get('code')
        if code is None:
            raise Response(status=status.HTTP_400_BAD_REQUEST)
        # # PC网站：https://graph.qq.com/oauth2.0/token
        # # GET
        #     # grant_type      必须      授权类型，在本步骤中，此值为“authorization_code”。
        #     # client_id       必须      申请QQ登录成功后，分配给网站的appid。
        #     # client_secret   必须      申请QQ登录成功后，分配给网站的appkey。
        #     # code            必须      上一步返回的authorization
        #     # redirect_uri    必须      与上面一步中传入的redirect_uri保持一致。
        # # 2. base_url
        # base_url = 'https://graph.qq.com/oauth2.0/token?'
        # #3.拼接参数
        # params = {
        #     'grant_type': 'authorization_code',
        #     'client_id':settings.QQ_APP_ID,
        #     'client_secret':settings.QQ_APP_KEY,
        #     'code':code,
        #     'redirect_uri':settings.QQ_REDIRECT_URL,
        # }
        # url = base_url + urlencode(params)
        # # urlopen 来获取url请求的数据
        # # 4. 通过urlopen来获取数据
        # # 它返回的值,需要我们使用 read来读取,读取的是二进制数据
        # response = urlopen(url)
        # data = response.read().decode()
        #
        # print('这是data的值: %s' % data)
        #
        # # 'access_token=3A2F1F985D5801C980E14E0890C82CAE&expires_in=7776000&refresh_token=6B96080C5E5D0BEBB5EB950983339C26'
        # # 5. 通过 pares_qs 将qs查询字符串格式数据转换为python的字典
        # access_data = parse_qs(data)
        # # 多采用调试模式去查看数据!!!!!!!!!!!!!!1
        # token = access_data.get('access_token')[0]
        #
        # print('这个是生成的token: %s' % token)
        #
        qq = OauthQQ()
        token = qq.get_access_token_by_code(code)
        openid = qq.get_openid_by_token(token)

        print('这个是生成的openid: %s' % openid)

        return openid

