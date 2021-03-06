from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate, login, logout
from port.jky.bin.msgDispose import msgReturn, msgCheck


class UserLoginAndLogout(ObtainAuthToken):
    def __init__(self):
        super().__init__()
        self.body = None
        self.user = None
        self.META = None
        self.POST = None

    def userLogin(self):
        username = msgCheck.Check_type(self).get('username')
        password = msgCheck.Check_type(self).get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            # 判断用户是否为可登录状态
            if user.is_active:
                # 删除原来的token
                Token.objects.filter(user=user).delete()
                # 创建新的token并传递给前端
                token = Token.objects.create(user=user)
                # 记录用户为登录状态
                login(self, user)
                # print(token)
                return JsonResponse({'code': 0, 'msg': ' 成功', 'token': token.key}, safe=False)
            else:
                return JsonResponse({'code': 0, 'msg': '当前账户没有激活，请联系管理员'}, safe=False)
        else:
            return JsonResponse({'code': -1, 'msg': '用户名或密码错误'}, safe=False)

    def userLogout(self):
        try:
            user_data = User.objects.get(id=self.user.id)
            username = user_data.username
            password = user_data.password
            user = authenticate(username=username, password=password)
            if user is not None:
                logout(self)
                Token.objects.get(user_id=self.user.id).delete()
                return JsonResponse(msgReturn.Msg().Success(msg='退出成功'))
            else:
                return JsonResponse(msgReturn.Msg().Success(msg='退出成功'))
        except Exception as e:
            print(e)
        finally:
            return JsonResponse(msgReturn.Msg().Success(msg='退出成功'))
