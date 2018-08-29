from random import randint

from django.http import HttpResponse
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from libs.captcha.captcha import Captcha
from libs.yuntongxun.sms import CCP
from .serializers import RegisterSMSCodeSerializer


class RegisterImageCodeView(APIView):

    def get(self, reuqest, image_code_id):
        """
        图片验证码接口
        /verifications/imagecodes/(?P<image_code_id>.+)/
        :param reuqest:
        :param Image_code_id:
        :return:
        """

        # 调用第三方库来生成验证码
        captcha = Captcha.instance()
        text, image = captcha.generate_captcha()
        print(text)

        # 获取reids
        code_redis = get_redis_connection('code')
        # 把text放到redis中
        code_redis.setex('img_%s' % image_code_id, 60, text)

        # 把图片返回
        return HttpResponse(image, content_type='image/jpg')


class RegisterSMSCodeView(GenericAPIView):

    def get(self, request, mobile):
        """
        /verifications/smscodes/(?P<mobile>1[356789]\d{9}/?text=xxxx&image_code_id=xxx
        需要验证验证码 就是image_code_id 还是 text 还要发送的手机号
        :param request:
        :return:
        """
        data = request.query_params
        # 创建序列化，对数据进行验证
        serializer = RegisterSMSCodeSerializer(data=data)
        # 开启生成异常
        serializer.is_valid(raise_exception=True)

        # 记录手机的验证时间
        redis_conn = get_redis_connection('code')

        redis_mobile = redis_conn.get('mobile')
        if redis_mobile:
            return Response(status=status.HTTP_429_TOO_MANY_REQUESTS)

        # 生成短信验证码
        sms_code = '%06d' % randint(0, 999999)
        print(sms_code)
        # 把验证码存放到redis中
        redis_conn.setex('sms_%s' % mobile, 3000, sms_code)

        # 发送短信
        # ccp = CCP()
        # ccp.send_template_sms(mobile, [sms_code, 5], 1)
        from celery_tasks.sms.tasks import send_sms_code
        send_sms_code.delay(mobile, sms_code)

        return Response({'message': 'ok'})