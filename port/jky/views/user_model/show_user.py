from django.http import JsonResponse

from port.jky.Controller import msg_return
from port.models import UserProfile


class User_handle:
    def __init__(self):
        super().__init__()

    def show_user(self):
        try:
            user = UserProfile.objects.all()
            data = list()
            for i in user:
                content = dict()
                content['id'] = i.user_id
                content['user_name'] = i.user_name
                data.append(content)
            return JsonResponse(msg_return.Msg().Success(data=data), safe=False)
        except Exception as e:
            return JsonResponse(msg_return.Msg().Error(msg=str(e)), safe=False)
