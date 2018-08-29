from django.db import models

# Create your models here.
from django.db import models

from mell import settings
from utils.models import BaseModel
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadData

class OAuthQQUser(BaseModel):
    """
    继承BaseModel
    QQ登录用户数据
    """

    # 外键关联 users.User
    # 主表删，字表也删
    # 主表删， 子表不让删
    # 主表删， 子表为null
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='用户')
    openid = models.CharField(max_length=64, verbose_name='openid', db_index=True)

    class Meta:
        db_table = 'tb_oauth_qq'
        verbose_name = 'QQ登录用户数据'
        verbose_name_plural = verbose_name


    @staticmethod
    def check_openid(access_token):
        # 解密openid 并且返回
        serializer = Serializer(settings.SECRET_KEY, expires_in=3600)
        return serializer.loads(access_token).get('openid')

    @staticmethod
    def save_user_token(open_id):
        # 保持功能
        # 进行序列化， 加密 设置时间
        serializer = Serializer(settings.SECRET_KEY, expires_in=3600)
        try:
            token = serializer.dumps({'openid': open_id})
        except BadData:
            # 出现异常，就是前段传过来的数据不正确
            return None
        return token.decode()