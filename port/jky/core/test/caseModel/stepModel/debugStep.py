from django.http import JsonResponse

from port.jky.bin.runPytestCase import StepDebugTest
from port.jky.bin.msgDispose import msgReturn, msgCheck
from port.jky.bin.ParameterSubstitution import Substitution
from port.jky.bin.ParameterSubstitution.keyword import ChangeKeyword
from port.jky.bin.RequestAndReturn import Requestreturn
from port.jky.bin.getparameters.GetParameters import Parameters
from port.models import Server, Headers


class StepDebug:
    def __init__(self):
        super().__init__()

    @msgCheck.login_check
    def debugStep(self):
        try:
            debug_step = msgCheck.Check_type(self)
            # 获取服务名
            server_id = debug_step.get('server_value')
            server_ip = Server.objects.get(id=server_id).server_ip
            # 获取请求头信息
            headers_id = debug_step.get('header_value')
            header_name = Headers.objects.get(id=headers_id).headers_body
            # print(server_ip, header_name)
            # headers = replace.Replace(msg=header_name, url=server_ip).Replace_globals()
            headers = Substitution.Substitution(url=server_ip).JudgeStatus(ChangeKeyword().ChangeData(header_name))
            print(headers)
            # 请求的接口
            url = Substitution.Substitution(url=server_ip).JudgeStatus(ChangeKeyword().ChangeData(debug_step.get('step_url')))
            # 获取请求环境信息
            server_value = debug_step.get('server_value')
            # print(header_value, server_value)
            # 请求的类型
            request_type = debug_step.get('step_type')
            # 请求的参数
            request_body = debug_step.get('step_content')
            # print(replace.Replace(msg=request_body).Replace_globals())
            # body = replace.Replace(msg=request_body).Replace_globals()
            body = Substitution.Substitution().JudgeStatus(ChangeKeyword().ChangeData(request_body))
            # 获取请求信息
            print(body)
            jsondata = Requestreturn.RequestMsg().requestAndResponse(url=server_ip + url, data=body, requestType=request_type, headers=headers)
            print(jsondata)
            # 断言参数
            assert_data = debug_step.get('assert_name')
            # 是否想要获取参数
            delivery = debug_step.get('delivery')
            # 获取想要的变量
            global_content = debug_step.get('global_content')
            # print(global_content)
            # print(body, headers, request_type, server_ip + url)
            # print(Requestreturn.RequestMsg().requestAndresponse(server_ip + url, body, request_type, headers))
            request_data = StepDebug.start(jsondata, assert_data)
            print(request_data)
            print(type(delivery))
            if delivery:
                content = Parameters.GetParameter(jsonData=jsondata, getArgument=global_content)
            else:
                content = None
                print('this')
                pass
            return JsonResponse(msgReturn.Msg().Success(data={'list': jsondata, 'assert_result': request_data, 'extend': content}), safe=False)
        except Exception as e:
            return JsonResponse(msgReturn.Msg().Error(msg=str(e)), safe=False)