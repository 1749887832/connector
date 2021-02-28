from django.http import JsonResponse
from port.jky.bin.msgDispose import msgReturn, msgCheck
from port.models import UserProfile


class UserHandle:
    def __init__(self):
        super().__init__()

    @msgCheck.login_check
    def showUser(self):
        try:
            user = UserProfile.objects.all()
            data = list()
            for i in user:
                content = dict()
                content['id'] = i.user_id
                content['user_name'] = i.user_name
                data.append(content)
            return JsonResponse(msgReturn.Msg().Success(data=data), safe=False, json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            return JsonResponse(msgReturn.Msg().Error(msg=str(e)), safe=False, json_dumps_params={'ensure_ascii': False})
