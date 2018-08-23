# -*- coding: utf-8 -*-
# @File  : utils.py
# @Author: liheng
# @time: 18-8-23 下午7:43

# 抽取/封装的原则:
# 1. 如果实现功能的代码出现了2次,将代码进行封装
# 2. 部分代码(一行也算是部分代码)实现了指定的功能就封装起来


"""
封装的步骤:
1. 将要封装的代码 复制到一个函数(不需要定义参数)中
2. 哪里有问题,改哪里,哪里缺少变量定义为 参数
3. 将复制的代码注释掉之后,进行验证,验证没有问题再把抽取的代码删除
"""
import json
from urllib.parse import urlencode, parse_qs
from urllib.request import urlopen

from django.conf import settings

class OauthQQ(object):
    """
    QQ授权工具

    """
    def get_auth_url(self):

        base_url = 'https://graph.qq.com/oauth2.0/authorize?'
        #
        # # 2. 将参数放在字典中
        params = {
            'response_type': 'code',
            'client_id': settings.QQ_APP_ID,
            'redirect_uri': settings.QQ_REDIRECT_URL,
            'state': 'test',
        }
        #
        # 3.
        # 将query字典转换为url路径中的查询字符串
        auth_url = base_url + urlencode(params)
        print('这是拼接好的url地址: %s' % auth_url)

        return auth_url

    def get_access_token_by_code(self, code):
        # PC网站：https://graph.qq.com/oauth2.0/token
        # GET
        # grant_type      必须      授权类型，在本步骤中，此值为“authorization_code”。
        # client_id       必须      申请QQ登录成功后，分配给网站的appid。
        # client_secret   必须      申请QQ登录成功后，分配给网站的appkey。
        # code            必须      上一步返回的authorization
        # redirect_uri    必须      与上面一步中传入的redirect_uri保持一致。
        # 2. base_url
        base_url = 'https://graph.qq.com/oauth2.0/token?'
        # 3. 拼接参数
        params = {
            'grant_type': 'authorization_code',
            'client_id': settings.QQ_APP_ID,
            'client_secret': settings.QQ_APP_KEY,
            'code': code,
            'redirect_uri': settings.QQ_REDIRECT_URL,
        }

        url = base_url + urlencode(params)

        # urlopen 来获取url请求的数据
        # 4. 通过urlopen来获取数据
        # 它返回的值,需要我们使用 read来读取,读取的是二进制数据
        response = urlopen(url)

        data = response.read().decode()

        # print(data)

        # 'access_token=3A2F1F985D5801C980E14E0890C82CAE&expires_in=7776000&refresh_token=6B96080C5E5D0BEBB5EB950983339C26'

        # 5. 通过 pares_qs 将qs查询字符串格式数据转换为python的字典
        access_data = parse_qs(data)

        # print(dict)
        # 多采用调试模式去查看数据
        token = access_data.get('access_token')[0]

        return token

    def get_openid_by_token(self, token):
        """
        PC网站：https://graph.qq.com/oauth2.0/me
        2 请求方法
        GET
        3 请求参数
        请求参数请包含如下内容：
        参数	是否必须	含义
        access_token	必须	在Step1中获取到的access token。

        """
        #1.获取baseurl
        base_url = 'https://graph.qq.com/oauth2.0/me?'

        # 2. 参数
        params = {
            'access_token': token
        }
        # 3. url
        url = base_url + urlencode(params)
        # 4. 根据url获取数据
        response = urlopen(url)

        data = response.read().decode()

        # print(data)
        # 5. 解析数据
        # 因为它返回的数据 不是 字典类型,我们要想获取 字典数据,需要对这个字符串进行截取
        # 'callback( {"client_id":"101474184","openid":"483C55DADEF65CC5735695CBC262F979"} );'
        try:
            openid_data = json.loads(data[10:-4])
        except Exception:
            raise Exception('数据获取错误')

        # print(openid_data)

        return openid_data['openid']