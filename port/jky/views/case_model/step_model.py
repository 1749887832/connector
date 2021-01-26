from django.http import JsonResponse

from port.jky.Controller import msg_check, msg_return, debug_Test
from port.jky.Controller.Token import debug_token
from port.models import Step, Server, Headers


class Step_handle:
    def __init__(self):
        super().__init__()

    @msg_check.login_check
    def show_step(self):
        # 获取id
        test_step = msg_check.Check_type(self)
        test_id = test_step.get('id')
        try:
            all_step = Step.objects.filter(test_id=test_id)
            count = len(all_step)
            data = list()
            for step in all_step:
                content = dict()
                content['id'] = step.id
                content['step_url'] = step.step_url
                content['request_type'] = step.request_type
                content['request_data'] = step.request_data
                content['get_global'] = step.get_global
                content['argument'] = step.argument
                content['response_result'] = step.response_result
                content['result'] = step.result
                data.append(content)
            return JsonResponse(msg_return.Msg().Success(data=data, total=count), safe=False)
        except Exception as e:
            return JsonResponse(msg_return.Msg().Error(msg=str(e)), safe=False)

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
        # 获取服务名
        server_id = debug_step.get('server_value')
        server_ip = Server.objects.get(id=server_id).server_ip
        # 获取请求头信息
        headers_id = debug_step.get('header_value')
        header_name = Headers.objects.get(id=headers_id).headers_body
        print(server_ip, header_name)
        # 请求的接口
        url = debug_step.get('step_url')
        # 获取请求头信息
        header_value = debug_step.get('header_value')
        # 获取请求环境信息
        server_value = debug_step.get('server_value')
        # print(header_value, server_value)
        # 请求的类型
        request_type = debug_step.get('step_type')
        # 请求的参数
        request_body = debug_step.get('step_content')
        # 断言参数
        assert_data = debug_step.get('assert_name')
        # 获取到token
        token = debug_token.Test_Token('https://yf1.jkwljy.com').get_token()
        headers = {'Content-Type': 'application/json;charset=UTF-8', 'Authorization': token}
        # request_data = debug_Test.start('https://yf1.jkwljy.com' + url, headers, request_type, request_body, assert_data)
        # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', request_data)
        return JsonResponse(msg_return.Msg().Success(), safe=False)
