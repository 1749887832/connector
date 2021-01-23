from django.http import JsonResponse
from port.jky.Controller import msg_return, msg_check, debug_Test
from port.models import Test
from port.jky.Controller.Token import debug_token


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

    @msg_check.login_check
    def add_Step(self):
        return JsonResponse(msg_return.Msg().Success(), safe=False)

    """
        author：liuhuangxin
        time:2021年1月23日13:56:40
    """

    @msg_check.login_check
    def debug_Step(self):
        debug_step = msg_check.Check_type(self)
        # 请求的接口
        url = debug_step.get('step_url')
        # 请求的类型
        request_type = debug_step.get('step_type')
        # 请求的参数
        request_body = debug_step.get('step_content')
        # 断言参数
        assert_data = debug_step.get('assert_name')
        print(url, request_type, request_body, assert_data)
        # 获取到token
        token = debug_token.Test_Token('https://yf1.jkwljy.com').get_token()
        print(token)
        headers = {'Content-Type': 'application/json;charset=UTF-8', 'Authorization': token}
        request_data = debug_Test.start('https://yf1.jkwljy.com' + url, headers, request_type, request_body, assert_data)
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', request_data)
        return JsonResponse(msg_return.Msg().Success(data=request_data), safe=False)
