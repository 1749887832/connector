from django.http import JsonResponse

from port.jky.Controller import msg_return, msg_check
from port.jky.Controller.msg_return import ReturnTime
from port.models import Cell


class AddTestClass:
    def __init__(self):
        super().__init__()

    def addTest(self):
        try:
            test = msg_check.Check_type(self)
            belongProject = test.get('belongProject')
            content = test.get('content')
            testName = test.get('testName')
            person = test.get('person')
            time = test.get('time')
            startTime = time[0].split('T')[0]
            endTime = time[1].split('T')[0]
            cell = Cell.objects.create(
                belongProject=belongProject,
                person=person,
                content=content,
                testName=testName,
                startTime=startTime,
                endTime=endTime,
                createUser=test.user_id,
                createTime=ReturnTime.getnowTime(),
            )
            cell.save()
            return JsonResponse(msg_return.Msg().Success(msg='新建成功'), safe=False, json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            return JsonResponse(msg_return.Msg().Error(msg=str(e)), safe=False, json_dumps_params={'ensure_ascii': False})
