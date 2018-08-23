from django.db import models

# Create your models here.
from django.db import models
from utils.models import BaseModel

class OAuthQQUser(BaseModel):
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