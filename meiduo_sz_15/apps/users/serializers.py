# -*- coding: utf-8 -*-
# @File  : serializers.py
# @Author: liheng
# @time: 18-8-22 下午7:12

# serializers.ModelSerializer  必须要有model
# serializers.Serializer
import re

from django_redis import get_redis_connection
from rest_framework import serializers

from celery_tasks.email.tasks import send_verify_mail
from .models import User
# from    .models import User


class RegisterUserSerializer(serializers.ModelSerializer):
    #短信字段,如何生成?
    password2 = serializers.CharField(label='确认密码', write_only=True,allow_blank=False, allow_null=False)
    sms_code = serializers.CharField(label='短信', write_only=True, allow_blank=False, allow_null=False)
    allow = serializers.CharField(label='是否同意协议', write_only=True, allow_blank=False,allow_null=False)
    token = serializers.CharField(label='token', read_only=True)
    class Meta:
        model = User
        #因为ModelSrializer 是根据fileds字段来生成序列化字段的
        #首先要看模型中是否有对应的字段,如果有自动生成
        #如果没有 我们是否实现了,如果没有实现就报错了
        fields = ['username', 'password', 'mobile', 'password2','sms_code','allow', 'token']
        # 如何区设置 自动生成的字段的选项???
        extra_kwargs = {
            'username':{
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                    }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            },
        }
    #对数据的校验有4种方式
    #1.字段类型
    #2.选项
    #3. 单个字段校验, 单个字段的值我们可以实现验证 def validate_filedname
    #4. 多个字段校验


    #手机号的验证
    def validate_mobile(self, value):
        #value就是传过来的值
        if not re.match('1[3-9]\d{9}', value):
            raise serializers.ValidationError('手机号不符合规则')
        #如果满足条件就把值返回就可以
        return value

    def validate_allow(self, value):
        #验证
        #要求前端传递一个字符串
        if value != 'true':
            raise serializers.ValidationError('没有同意协议')
        return value

    #多个字段校验, 是指我们需要用到多个值
    def validate(self, attrs):
        #密码和确认密码需要比对
        password  = attrs.get('password')
        password2  = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError('密码不一致')

        #短信校验
        #1. 获取用户提交的短信验证码
        sms_code = attrs.get('sms_code')
        mobile  = attrs.get('mobile')
        # 2.获取redis中验证码
        redis_conn =get_redis_connection('code')
        redis_code = redis_conn.get('sms_%s' % mobile)
        if redis_code is None:
            raise serializers.ValidationError('验证码已经过期')
        #3.比较  redis_code是bytes类型
        if sms_code != redis_code.decode():
            raise serializers.ValidationError('验证码不正确')

        return  attrs
    # 当序列化器调用 save方法的时候 会自动调用 序列化器中的 create方法,将数据保存到数据库中
    def create(self, validated_data):
        # User.objects.create(**validate_data)

        # validated_data 校验之后的数据

        # 父类方法不能满足我们的需求,我们就需要重写
        # 因为validated_data 有6个字段
        #实际入库只有3个字段
        #我们需要将多余的字段删除
        del validated_data['sms_code']
        del validated_data['password2']
        del validated_data['allow']

        #处理之后的字段是可以入库的  TODO  '为啥要继承'
        #因为父类方法里面没有这些字段,所以需要重写来添加这些字段,如果视图里面用的genericapiview 就不用
        #重写了,自带create和update方法
        user  = super().create(validated_data) #返回的是一个instace实例对象

        # user的密码还是明文,所以要用set_password进行sha256进行加密
        user.set_password(validated_data['password'])
        user.save()    #向数据库里里面写数据了
        # 这里是 数据入库,并且修改密码的地方,我们生成一个token,然后再把token经过序列化返回给客户端
        # jwt 的token如何生成呢?
        from rest_framework_jwt.settings import api_settings

        # 需要获取2个方法
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        # 将用户的信息放到 payload中
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        # token 就是生成好的 jwt token
        user.token = token

        return user

"""
用户中心
"""
# serializers.ModelSerializer  必须要有model
# serializers.Serializer
class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详细信息序列化器
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'mobile', 'email', 'email_active')


"""
邮箱验证
"""
# serializers.ModelSerializer  必须要有model
# serializers.Serializer
class EmailSerializer(serializers.ModelSerializer):
    """
    邮箱序列化
    """

    class Meta:
        model = User     #要create/update的对象
        fields = ('id', 'email')
        extra_kwargs = {    #给已有的字段添加额外的字段
            'email': {
                'required': True #发序列化的时候输入
            }
        }

    def update(self, instance, validated_data):  #instance 就是反序列化的对象
        email = validated_data['email']          #把已经校验过的数据更新到email字段
        instance.email = validated_data['email'] #把email属性绑定到user身上
        instance.save()


        #发送邮件
        #生成激活链接
        verify_url = instance.generate_verify_email_url()

        #发送,注意调用delay方法
        send_verify_mail.delay(email, verify_url)

        return instance   #这里返回的就是User模型的user对象








