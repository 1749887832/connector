from django.http import JsonResponse
from port.jky.bin.msgDispose import msgReturn, msgCheck
from port.models import Test, UserProfile


class CaseHandle:
    def __init__(self):
        super().__init__()
        self.body = None
        self.user = None

    @msgCheck.login_check
    def addCase(self):
        print(self)
        try:
            data = msgCheck.Check_type(self)
            test_name = data.get('casename')
            test_content = data.get('caseesc')
            test_model = data.get('casemodel')
            userid = self.user.id
            test = Test.objects.create(
                test_name=test_name,
                test_model=test_model,
                test_content=test_content,
                create_time=msgReturn.ReturnTime.getNowTime(),
                create_user=userid
            )
            test.save()
            return JsonResponse(msgReturn.Msg().Success(msg='添加成功'), safe=False)
        except Exception as e:
            return JsonResponse(msgReturn.Msg().Error(code=-1, msg=str(e)), safe=False)

    @msgCheck.login_check
    def showCase(self):
        try:
            test = msgCheck.Check_type(self)
            casename = test.get('casename')
            chose_option = test.get('chose_option')
            end_time = test.get('end_time') if test.get('end_time') not in ['', None] else '2099-12-31 23:59:59'
            start_time = test.get('start_time') if test.get('start_time') not in ['', None] else '1000-01-01 00:00:00'
            page = int(test.get('page'))
            limit = int(test.get('limit'))
            all_test = Test.objects.filter(test_name__contains=casename, create_time__range=(start_time, end_time), create_user__contains=chose_option)
            total = len(all_test)
            showtest = all_test[limit * (page - 1):limit * page]
            data = list()
            for test in showtest:
                context = dict()
                context['id'] = test.id
                context['test_name'] = test.test_name
                context['test_content'] = test.test_content
                context['create_user'] = UserProfile.objects.get(user_id=test.create_user).user_name
                context['create_time'] = test.create_time.strftime('%Y-%m-%d %H:%M:%S')
                data.append(context)
            return JsonResponse(msgReturn.Msg().Success(data=data, msg='成功', total=total), safe=False)
        except Exception as e:
            return JsonResponse(msgReturn.Msg().Error(code=-1, msg=str(e)), safe=False)
