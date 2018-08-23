from django.http import HttpResponse
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.verifications.serializers import RegisterSmscodeSerializer
from libs.captcha.captcha import captcha
from libs.yuntongxun.sms import CCP


class RegisterImageCodeView(APIView):
    """
    生成验证码
    GET verifications/imagecodes/(?P<image_code_id>.+)/
    需要通过JS生成一个唯一码,以确保后台对图片进行校验
    """
    def get(self, request, image_code_id):
        print(1)
        """
        通过第三方库,生成图片和验证码,我们需要对验证码进行redis保存

        思路为:
        创建图片和验证码
        通过redis进行保存验证码,需要在设置中添加 验证码数据库选项
        将图片返回
        """
        #创建图片和验证码
        text,image = captcha.generate_captcha()
        print('图片验证码为 % s ' % text)
        #创建链接
        redis_conn = get_redis_connection('code')
        # 通过redis保存验证码
        redis_conn.setex('img_%s' % image_code_id, 60, text)
        #将图片返回
        # 注意,图片是二进制,我们通过HttpResponse返回

        return HttpResponse(image, content_type='image/jpeg')

# APIView
# GenericAPIView
# ListAPIView,RetrieveAPIView

class RegisterSMSCodeView(APIView):
    """
    GET     /verifications/smscodes/?P<mobile>1[3-9]\d{9}/?text=xxxx&image_code_id=xxxx
    GET     /verifications/smscodes/?mobile=xxxx&text=xxxx&image_code_id=xxxx
    GET     /verifications/smscodes/mobile/text/image_code_id/
    前端点击按钮的时候,后台会给指定的手机号发送验证码,前端会进行一个倒计时
    需要给指定的手机发送验证码
    图片验证码就是防止用户频繁操作而设置的,所以需要对图片验证码进行校验

    思路:
    1.前端需要将手机号,还有图片验证码和对应的image_code_id传递过来
    2.对图片验证码和uuid进行校验,手机号也要校验
    3.需要对手机号发送记录进行判断(60秒之内是否发送过)
    4.生成随机短信验证码
    5.redis记录短信内容
    6.发送短信

    获取短信验证码
    GET /verifications/smscodes/(?P<mobile>1[3-9]\d{9})/?text=xxxx&image_code_id=xxxx
    获取短信验证码,首先需要校验 验证码
    思路:
    创建序列化器,定义text 和 image_code_id
    redis 判断该用户是否频繁获取
    生成短信验证码
    redis增加记录
    发送短信
    返回响应

    """
    #1.获取验证码:
    def get(self, request, mobile, celery_tasks=None):
        # 2. 对图片验证码和uuid进行校验, 手机号也要校验
        #需要对数据进行验证(反序列化)
        #/(?P<mobile>1[3-9]\d{9})/?text=xxxx&image_code_id=xxxx
        #获取get中的查询字符串的时候需要使用request中的query_params
        data = request.query_params
        #创建序列化器械
        serializer = RegisterSmscodeSerializer(data=data)
        serializer.is_valid()
        #3.需要对手机号发送记录进行判断(60秒之内是否有发送过)
        redis_conn = get_redis_connection('code')
        #获取发送的状态
        if redis_conn.get('sms_flag_%s'%  mobile):
            return Response(status=status.HTTP_429_TOO_MANY_REQUESTS)
        #4.生成短信
        from random import randint
        sms_code = '%06d' % randint(0,999999)
        print('手机验证码为: %s' % sms_code)
        #5.redis记录短信内容后面注册的时候需要验证   60秒以后过期,用的默认的1号模板 key time value\
        # 记录为string
        redis_conn.setex('sms_%s'%mobile,5*60,sms_code)
        # 记录发送状态
        redis_conn.setex('sms_flag_%s' % mobile, 60, 1)
        # 6.发送短信
        # ccp = CCP() # mobile:向谁发 []:发什么, 60:过期时间, 1:模板  ,
        # ccp.send_template_sms(mobile, [sms_code], 60, 1)
        from celery_tasks.sms.tasks import send_sms_code
        # 注意: 异步任务必须使用 delay调用
        # delay的参数是 和 任务的参数是一致的
        # send_sms_code(mobile,sms_code) --错误代码 不能这样发送
        send_sms_code.delay(mobile, sms_code)

        return Response({'message': 'ok'})











