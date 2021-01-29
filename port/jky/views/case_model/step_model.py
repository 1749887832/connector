from django.http import JsonResponse

from port.jky.Controller import msg_check, msg_return, debug_Test
from port.jky.Controller.Funstorage import replace
from port.jky.Controller.Token import debug_token
from port.models import Step, Server, Headers, Assert, Part


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
        add_step = msg_check.Check_type(self)
        # 获取接口地址
        step_url = add_step.get('step_url')
        # 获取接口请求方式
        step_type = add_step.get('step_type')
        # 获取请求body
        step_body = add_step.get('step_content')
        # 获取断言参数
        step_assert = add_step.get('assert_name')
        # 获取是否存储变量
        step_delivery = add_step.get('delivery')
        # 获取存储变量
        step_global = add_step.get('global_content')
        # 获取描述
        step_content = add_step.get('step_data')
        # 获取case_id
        case_id = add_step.get('case_id')
        print(step_delivery, case_id)
        try:
            # 写入步骤
            step_object = Step.objects.create(
                step_url=step_url,
                request_type=step_type,
                request_data=step_body,
                get_global=step_delivery,
                create_user=add_step.user_id,
                step_content=step_content,
                test_id=case_id
            )
            step_object.save()
            step_id = step_object.id
            # 写入断言参数
            for i in list(step_assert):
                Assert.objects.create(
                    argument=i['name'],
                    assert_type=i['type'],
                    assert_expect=i['value'],
                    argument_type=i['argument_type'],
                    step_id=step_id
                )
            # 写入获取参数
            if step_delivery:
                for i in list(step_global):
                    print(i)
                    Part.objects.create(
                        use_global=i['global_name'],
                        argument=i['argument'],
                        step_id=step_id
                    )
            return JsonResponse(msg_return.Msg().Success(), safe=False)
        except Exception as e:
            return JsonResponse(msg_return.Msg().Error(msg=str(e)), safe=False)

    """
        author：liuhuangxin
        time:2021年1月23日13:56:40
    """

    @msg_check.login_check
    def debug_Step(self):
        try:
            debug_step = msg_check.Check_type(self)
            # 获取服务名
            server_id = debug_step.get('server_value')
            server_ip = Server.objects.get(id=server_id).server_ip
            # 获取请求头信息
            headers_id = debug_step.get('header_value')
            header_name = Headers.objects.get(id=headers_id).headers_body
            # print(server_ip, header_name)
            headers = replace.Replace(msg=header_name, url=server_ip).Replace_globals()
            # 请求的接口
            url = debug_step.get('step_url')
            # 获取请求环境信息
            server_value = debug_step.get('server_value')
            # print(header_value, server_value)
            # 请求的类型
            request_type = debug_step.get('step_type')
            # 请求的参数
            request_body = debug_step.get('step_content').encode('utf-8')
            # print(replace.Replace(msg=request_body).Replace_globals())
            body = replace.Replace(msg=request_body).Replace_globals()
            # 断言参数
            assert_data = debug_step.get('assert_name')
            # 是否想要获取参数
            delivery = debug_step.get('delivery')
            # 获取想要的变量
            global_content = debug_step.get('global_content')
            # print(global_content)
            request_data = debug_Test.start(server_ip + url, headers, request_type, body, assert_data, delivery, global_content)
            return JsonResponse(msg_return.Msg().Success(data=request_data), safe=False)
        except Exception as e:
            return JsonResponse(msg_return.Msg().Error(msg=str(e)), safe=False)
