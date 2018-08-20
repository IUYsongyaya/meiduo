from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection
from rest_framework.views import APIView

from libs.captcha.captcha import captcha


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
        # captcha = Captcha.instance()
        name,text,image = captcha.generate_captcha()
        #通过redis保存验证码
        redis_conn = get_redis_connection('code')
        redis_conn.setex('img_%s' % image_code_id, 60, text)
        #将图片返回
        # 注意,图片是二进制,我们通过HttpResponse返回

        return HttpResponse(image, content_type='image/jpeg')
