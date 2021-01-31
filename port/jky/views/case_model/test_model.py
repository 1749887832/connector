from django.http import JsonResponse
from port.jky.Controller import msg_return, msg_check
from port.models import Test


class Test_handle:
    def __init__(self):
        super().__init__()
        self.user = None

    @msg_check.login_check
    def add_Test(self):
        print(self)
        try:
            data = msg_check.Check_type(self)
            test_name = data.get('casename')
            test_content = data.get('caseesc')
            test_model = data.get('casemodel')
            userid = self.user.id
            test = Test.objects.create(
                test_name=test_name,
                test_model=test_model,
                test_content=test_content,
                create_time=msg_return.ReturnTime.getnowTime(),
                create_user=userid
            )
            test.save()
            return JsonResponse(msg_return.Msg().Success(msg='添加成功'), safe=False)
        except Exception as e:
            return JsonResponse(msg_return.Msg().Error(code=-1, msg=str(e)), safe=False)

    @msg_check.login_check
    def show_Test(self):
        try:
            all_test = Test.objects.all()
            total = len(all_test)
            data = list()
            for test in all_test:
                context = dict()
                context['id'] = test.id
                context['test_name'] = test.test_name
                context['test_content'] = test.test_content
                context['create_user'] = test.create_user
                context['create_time'] = test.create_time.strftime('%Y-%m-%d %H:%M:%S')
                data.append(context)
            return JsonResponse(msg_return.Msg().Success(data=data, msg='成功', total=total), safe=False)
        except Exception as e:
            return JsonResponse(msg_return.Msg().Error(code=-1, msg=str(e)), safe=False)
