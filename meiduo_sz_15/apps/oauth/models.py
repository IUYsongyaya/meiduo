from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
# 这里导包的时候可以用from xxxx  import  xxxxx as  'name'  来给名字比较长的取个别名
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature, BadData

from utils.models import BaseModel


class OAuthQQUser(BaseModel):
    # 这里继承了basemodel基类里面,增加了两个字段 updatetime createtime

    """
    QQ登录用户数据
    """

    # 1对1,1对多, 级联操作
    # 主表数据删除,子表数据该怎么做?

    # 主表删,子表也删除
    # 主表删,子表不让删除
    # 主表删,子表设置为NULL


    # 外键 关联的时候是想关联 其他子应用的模型类,语法为: 子应用.模型类
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='用户')
    openid = models.CharField(max_length=64, verbose_name='openid', db_index=True)

    class Meta:
        db_table = 'tb_oauth_qq'
        verbose_name = 'QQ登录用户数据'
        verbose_name_plural = verbose_name

    # 对象方法  def generic_token_by_openid(self,openid):

    # 类方法   @classmethod
    #         def generic_token_by_openid(cls,openid):

    # 静态方法
    # @staticmethod
    # def generic_token_by_openid(openid):

    @staticmethod
    def generate_save_user_token(openid):
        # 1.创建序列化器   这里要导入django.conf里面个的settings!!!
        serializer = Serializer(settings.SECRET_KEY, expires_in=3600)
        # 2.加密处理 这里获取的是一个bytes的内容
        token = serializer.dumps({'openid': openid})
        print('这是加密以后的openid: %s' % token)
        return token.decode()

    @staticmethod
    def openid_by_token(access_token):
        #1.创建序列化器 这里要导入django.conf里面个的settings!!!
        print('这是传入的access_token: %s' % access_token)
        serializer = Serializer(settings.SECRET_KEY, 3600)
        #2.解密
        try:
            result = serializer.loads(access_token)
            #result = {'openid':xxxx}
            print('loads以后的access_token: %s' % result)
        except BadData:
            return None
        else:
            return result.get('openid')


