from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,BadData

from meiduo_sz_15 import settings


class User(AbstractUser):
    """用户模型"""
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')

    email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def generate_verify_email_url(self):

        serializer = Serializer(settings.SECRET_KEY,3600)

        # 加载用户信息
        token = serializer.dumps({'user_id':self.id, 'email':self.email})
        #注意拼接的过程中 对token进行decode操作

        verify_url = 'http://www.meiduo.site:8080/success_verify_email.html?token=' + token.decode()

        return verify_url

    @staticmethod
    def check_verify_email_token(token):
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            # 加载token
            result = serializer.loads(token)
        except BadData:
            return None
        else:
            user_id = result.get('user_id')
            email = result.get('email')
            try:
                user = User.objects.get(id=user_id, email=email)
            except User.DoesNotExist:
                user = None
            else:
                return user




