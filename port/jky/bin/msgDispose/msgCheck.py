import json
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from port.jky.bin.msgDispose import msgReturn


# 登录验证的装饰器
def login_check(login_func):
    def func(data):
        login_id = data.user.id
        login_token = data.META.get('HTTP_AUTHORIZATION')
        try:
            # 校验用户和token是否匹配
            if len(Token.objects.filter(user_id=login_id, key=login_token)) != 0:
                return login_func(data)
            else:
                return JsonResponse(msgReturn.Msg().Error(code=1010, msg='登录信息失效，请重新登录'), safe=False, json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            return JsonResponse(msgReturn.Msg().Error(code=-1, msg=str(e)), safe=False, json_dumps_params={'ensure_ascii': False})
    return func


# POST请求还是GET请求的装饰器
def request_type(request_func):
    def request_fun(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            return request_func(data)
        else:
            data = request.GET
            return request_func(data)

    return request_fun


# 这是处理请求的方法
"""
    勿动
"""


class Check_type:
    def __init__(self, request):
        self.request = request
        self.user_id = self.request.user.id
        super().__init__()

    def get(self, name):
        if self.request.method == 'POST':
            data = json.loads(self.request.body)
            return data.get(name)
        else:
            return self.request.GET.get(name)
