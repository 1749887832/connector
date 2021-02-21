import requests
import urllib3
from django.db.models import Max
from django.http import JsonResponse

from port.jky.Controller import msg_check, msg_return, debug_Test
from port.jky.Controller.Funstorage import replace
from port.jky.Controller.ParameterSubstitution.keyword import ChangeKeyword
from port.jky.Controller.Requestreturns import Requestreturn
from port.jky.Controller.getparameters.GetParameters import Parameters
from port.models import Step, Server, Headers, Assert, Part, UserProfile
from port.jky.Controller.ParameterSubstitution import Substitution


class Step_handle:
    def __init__(self):
        super().__init__()
        self.POST = None

    @msg_check.login_check
    def show_step(self):
        # 获取id
        test_step = msg_check.Check_type(self)
        test_id = test_step.get('id')
        page = int(test_step.get('page'))
        limit = int(test_step.get('limit'))
        try:
            all_step = Step.objects.filter(test_id=test_id).order_by('step_order')
            count = len(all_step)
            showstep = all_step[limit * (page - 1):limit * page]
            data = list()
            for step in showstep:
                content = dict()
                content['id'] = step.id
                content['step_url'] = step.step_url
                content['request_type'] = step.request_type
                content['request_data'] = step.request_data
                content['get_global'] = step.get_global
                content['response_result'] = step.response_result
                content['create_time'] = step.create_time.strftime('%Y-%m-%d')
                content['create_user'] = UserProfile.objects.get(user_id=step.create_user).user_name
                content['result'] = step.result
                content['order'] = step.step_order
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
        # 获取请求头
        header_value = add_step.get('header_value')
        if msg_return.JudgeAllIsNull.checkandreturn(header_value, add_step, step_url, step_type, step_body):
            print(step_delivery, case_id)
            try:
                # 查询用例的最大执行顺序
                maxOrder = Step.objects.filter(test_id=case_id).aggregate(Max('step_order'))
                # 写入步骤
                step_object = Step.objects.create(
                    step_url=step_url,
                    request_type=step_type,
                    request_data=step_body,
                    get_global=step_delivery,
                    create_user=add_step.user_id,
                    step_content=step_content,
                    create_time=msg_return.ReturnTime.getnowTime(),
                    step_order=maxOrder['step_order__max'] + 1,
                    test_id=case_id,
                    step_headers=header_value,
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
                            argument=i['urlarument'],
                            partIndex=i['urlindex'],
                            step_id=step_id
                        )
                return JsonResponse(msg_return.Msg().Success(), safe=False)

            except Exception as e:
                return JsonResponse(msg_return.Msg().Error(msg=str(e)), safe=False)
        else:
            return JsonResponse(msg_return.Msg().Error(msg='必填参数不能为空'), safe=False, json_dumps_params={'ensure_ascii': False})

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
            jsondata = Requestreturn.RequestMsg().requestAndresponse(url=server_ip + url, data=body, requestype=request_type, headers=headers)
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
            request_data = debug_Test.start(jsondata, assert_data)
            print(request_data)
            print(type(delivery))
            if delivery:
                content = Parameters.GetParameter(jsondata=jsondata, getarument=global_content)
            else:
                content = None
                print('this')
                pass
            return JsonResponse(msg_return.Msg().DebugSuccess(data={'list': jsondata, 'assert_result': request_data, 'extend': content}), safe=False)
        except Exception as e:
            return JsonResponse(msg_return.Msg().Error(msg=str(e)), safe=False)

    @msg_check.login_check
    def debug_api(self):
        apidata = msg_check.Check_type(self)
        urlname = apidata.get('urlname')
        urlbody = apidata.get('urlbody')
        urltype = apidata.get('urltype')
        server = apidata.get('server')
        headers = apidata.get('headers')
        # 获取参数
        agrument = apidata.get('getvalue')
        print(agrument)
        print(urlname, urltype, server, urlbody)
        # 返回了请求体
        if msg_return.JudgeAllIsNull.checkandreturn(urlname, urltype, server):
            try:
                # 获取请求
                serverip = Server.objects.get(id=server).server_ip
                # 解析请求体
                data = Substitution.Substitution(url=serverip).JudgeStatus(ChangeKeyword().ChangeData(urlbody))
                # 解析url
                urlname = Substitution.Substitution(url=serverip).JudgeStatus(ChangeKeyword().ChangeData(urlname))
                print(urlname)
                print(data, serverip)
                if headers not in ['', 'null', None]:
                    # 获取请求头
                    headersbody = Headers.objects.get(id=headers).headers_body
                    # print(headersbody)
                    # 解析请求头
                    headers = Substitution.Substitution(url=serverip).JudgeStatus(ChangeKeyword().ChangeData(headersbody))
                # 获取调试结果
                contendata = Requestreturn.RequestMsg.requestAndresponse(url=serverip + urlname, data=ChangeKeyword().ChangeData(data), requestype=urltype, headers=headers)
                print(contendata)
                if msg_return.JudgeAllIsNull.checkandreturn(agrument[0]['urlarument'], agrument[0]['urlindex']):
                    getparameters = Parameters.GetParameter(jsondata=contendata, getarument=agrument)
                else:
                    getparameters = ''
                # print(contendata)
            except Exception as e:
                return JsonResponse(msg_return.Msg().Error(msg=str(e)), safe=False)
        else:
            return JsonResponse(msg_return.Msg().Error(msg='必填项不能为空!'), safe=False, json_dumps_params={'ensure_ascii': False})
        return JsonResponse(msg_return.Msg().Success(data={'list': contendata, 'extend': getparameters}), safe=False, json_dumps_params={'ensure_ascii': False})

    @msg_check.login_check
    def del_Step(self):
        try:
            delstep = msg_check.Check_type(self)
            step_id = delstep.get('id')
            if len(Assert.objects.filter(step_id=step_id)) > 0:
                Assert.objects.filter(step_id=step_id).delete()
            if len(Part.objects.filter(step_id=step_id)) > 0:
                Part.objects.filter(step_id=step_id).delete()
            Step.objects.filter(id=step_id).delete()
            return JsonResponse(msg_return.Msg().Success(msg='删除成功'), safe=False, json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            return JsonResponse(msg_return.Msg().Error(msg=str(e)), safe=False, json_dumps_params={'ensure_ascii': False})

    @msg_check.login_check
    def showAllStep(self):
        try:
            testID = msg_check.Check_type(self).get('testID')
            allStep = Step.objects.filter(test_id=testID).order_by('step_order')
            data = list()
            for step in allStep:
                content = dict()
                content['id'] = step.id
                content['order'] = step.step_order
                content['type'] = step.request_type
                content['url'] = step.step_url
                content['content'] = step.step_content
                data.append(content)
            return JsonResponse(msg_return.Msg().Success(data=data), safe=False, json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            return JsonResponse(msg_return.Msg().Error(msg=str(e)), safe=False, json_dumps_params={'ensure_ascii': False})
