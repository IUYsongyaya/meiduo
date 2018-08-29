import json
from urllib.parse import urlencode, parse_qs
from urllib.request import urlopen

# Create your views here.
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from mell import settings
from oauth.models import OAuthQQUser
from oauth.serializers import QQTokenSerializer
from utils.models import BaseModel


def get_auth_url():
    url = "https://graph.qq.com/oauth2.0/authorize?"

    # 加上必要的参数
    params = {
        "response_type": "code",
        "client_id": settings.QQ_APP_ID,
        "redirect_uri": settings.QQ_REDIRECT_URL,
        "state": '/',
    }

    auth_url = url + urlencode(params)

    return auth_url



def get_access_token(code):
    url = "https://graph.qq.com/oauth2.0/token?"

    params = {
        "grant_type": "authorization_code",
        "client_id": settings.QQ_APP_ID,
        "client_secret": settings.QQ_APP_KEY,
        "code": code,
        "redirect_uri": settings.QQ_REDIRECT_URL,
    }

    auth_url = url + urlencode(params)
    response = urlopen(auth_url)
    data = response.read().decode()

    query_params = parse_qs(data)
    # 获取到token
    access_token = query_params.get('access_token')

    if access_token is None:
        raise Exception('获取token失败')

    return access_token[0]


def get_open_id(access_token):
    url = "https://graph.qq.com/oauth2.0/me?"

    params = {
        "access_token": access_token,
    }

    url = url + urlencode(params)
    response = urlopen(url).read().decode()
    resp_str = json.loads(response[10:-4])
    return resp_str['openid']




class QQAuthURLView(APIView):
    # /oauth/qq/statues/
    def get(self, request):
        # 实现qq登录
        # 需要返回给一个指定的qq登录的页面上去
        # 就是返回一个URL就行了
        """
        PC网站：https://graph.qq.com/oauth2.0/authorize
        response_type	必须	授权类型，此值固定为“code”。
        client_id	必须	申请QQ登录成功后，分配给应用的appid。
        redirect_uri	必须	成功授权后的回调地址，必须是注册appid时填写的主域名下的地址，建议设置为网站首页或网站的用户中心。注意需要将url进行URLEncode。
        state	必须	client端的状态值。用于第三方应用防止CSRF攻击，成功授权后回调时会原样带回。请务必严格按照流程检查用户与state参数状态的绑定。
        scope	可选	请求用户授权时向用户显示的可进行授权的列表。
        可填写的值是API文档中列出的接口，以及一些动作型的授权（目前仅有：do_like），如果要填写多个接口名称，请用逗号隔开。
        例如：scope=get_user_info,list_album,upload_pic,do_like
        不传则默认请求对接口get_user_info进行授权。
        建议控制授权项的数量，只传入必要的接口名称，因为授权项越多，用户越可能拒绝进行任何授权。
        display	可选	仅PC网站接入时使用。
        用于展示的样式。不传则默认展示为PC下的样式。
        如果传入“mobile”，则展示为mobile端下的样式。
        """
        auth_url = get_auth_url()

        return Response({'auth_url': auth_url})



class QQTokenView(GenericAPIView):
    serializer_class = QQTokenSerializer

    def get(self, request):
        """
        PC网站：https://graph.qq.com/oauth2.0/token
        grant_type	必须	授权类型，在本步骤中，此值为“authorization_code”。
        client_id	必须	申请QQ登录成功后，分配给网站的appid。
        client_secret	必须	申请QQ登录成功后，分配给网站的appkey。
        code	必须	上一步返回的authorization code。
        如果用户成功登录并授权，则会跳转到指定的回调地址，并在URL中带上Authorization Code。
        例如，回调地址为www.qq.com/my.php，则跳转到：
        http://www.qq.com/my.php?code=520DD95263C1CFEA087******
        注意此code会在10分钟内过期。
        redirect_uri	必须	与上面一步中传入的redirect_uri保持一致。
        :param request:
        :return:
        """
        code = request.query_params.get('code')
        access_token = get_access_token(code)

        open_id = get_open_id(access_token)

        try:
            # 查询用户是否存在
            qq_user = OAuthQQUser.objects.get(openid=open_id)
        except OAuthQQUser.DoesNotExist:
            # 如果用户不存在的时候
            # 把openid进行加密传递给前段
            token = OAuthQQUser.save_user_token(open_id)
            print(token)
            return Response({'access_token': token})

        else:
            # 用户已经绑定成功， 就设置token
            user = qq_user.user
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            # 把信息返回给前段页面
            response = Response({
                'token': token,
                'user_id': user.id,
                'username': user.username
            })

            return response

    def post(self, request):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # 生成已登录的token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        response = Response({
            'token': token,
            'user_id': user.id,
            'username': user.username
        })

        return response
