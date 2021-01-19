from django.contrib.auth.models import User
from django.http import JsonResponse
from port.jky.Controller import msg_return

from port.models import Global


class Global_handle:
    def __init__(self):
        super().__init__()

    def show_global(self):
        try:
            allglobal = Global.objects.all()
            total = len(allglobal)
            data = list()
            for i in allglobal:
                context = dict()
                context['id'] = i.id
                context['globals_name'] = i.globals_name
                context['use_name'] = i.use_name
                context['globals_type'] = i.globals_type
                context['use_type'] = i.use_type
                context['cite_arguments'] = i.cite_arguments
                context['create_time'] = i.create_time
                context['content'] = i.content
                context['create_user'] = i.create_user
                data.append(context)
            return JsonResponse(msg_return.Msg().Success(data=data, total=total), safe=False)
        except Exception as e:
            return JsonResponse(msg_return.Msg().Error(code=-1, msg=str(e)), safe=False)
