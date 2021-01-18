import json

from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from port.jky.Controller import msg_return


# 登录验证的装饰器
def login_check(login_func):
    def func(data):
        login_id = data.user.id
        login_token = data.META.get('HTTP_AUTHORIZATION')
        # print(login_id,login_token)
        try:
            # 校验用户和token是否匹配
            if len(Token.objects.filter(user_id=login_id, key=login_token)) != 0:
                return login_func(data)
            else:
                return JsonResponse(msg_return.Msg().Error(code=1010, msg='请先登录'), safe=False)
        except Exception as e:
            print(e)
            return JsonResponse(msg_return.Msg().Error(code=-1, msg=str(e)), safe=False)

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
