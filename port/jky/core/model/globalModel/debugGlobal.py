from django.http import JsonResponse
from port.jky.bin.msgDispose import msgReturn, msgCheck
from port.jky.bin.ParameterSubstitution import Substitution
from port.jky.bin.ParameterSubstitution.keyword import ChangeKeyword
from port.jky.bin.RequestAndReturn import Requestreturn
from port.jky.bin.getparameters.GetParameters import Parameters
from port.models import Server, Headers


class GlobalDebug:
    def __init__(self):
        super().__init__()

    @msgCheck.login_check
    def debugGlobal(self):
        apidata = msgCheck.Check_type(self)
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
        if msgReturn.JudgeAllIsNull.checkAndReturn(urlname, urltype, server):
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
                contendata = Requestreturn.RequestMsg.requestAndResponse(url=serverip + urlname, data=ChangeKeyword().ChangeData(data), requestType=urltype, headers=headers)
                print(contendata)
                if msgReturn.JudgeAllIsNull.checkAndReturn(agrument[0]['urlarument'], agrument[0]['urlindex']):
                    getparameters = Parameters.GetParameter(jsonData=contendata, getArgument=agrument)
                else:
                    getparameters = ''
                # print(contendata)
            except Exception as e:
                return JsonResponse(msgReturn.Msg().Error(msg=str(e)), safe=False)
        else:
            return JsonResponse(msgReturn.Msg().Error(msg='必填项不能为空!'), safe=False, json_dumps_params={'ensure_ascii': False})
        return JsonResponse(msgReturn.Msg().Success(data={'list': contendata, 'extend': getparameters}), safe=False, json_dumps_params={'ensure_ascii': False})
