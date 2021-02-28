from django.http import JsonResponse

from port.jky.bin.msgDispose import msgReturn, msgCheck
from port.jky.bin.ParameterSubstitution import Substitution
from port.jky.bin.runPytestCase.BatchDebugTest import startBath
from port.jky.bin.ParameterSubstitution.keyword import ChangeKeyword
from port.models import Server, Step, Part, Assert


class CaseDebug:
    def __init__(self):
        super().__init__()

    def debugCase(self):
        try:
            allTest = msgCheck.Check_type(self)
            testList = allTest.get('testList')
            serverIp = Server.objects.get(id=allTest.get('serverId')).server_ip
            # print(serverIp)
            # print(testList)
            batchList = list()
            for test in testList:
                # 解析url
                url = Substitution.Substitution(url=serverIp).JudgeStatus(ChangeKeyword().ChangeData(Step.objects.get(id=test).step_url))
                # 解析请求body
                body = Substitution.Substitution(url=serverIp).JudgeStatus(ChangeKeyword().ChangeData(Step.objects.get(id=test).request_data))
                # 获取绑定的请求头，并解析
                # header = Headers.objects.get(id=Step.objects.get(id=test).step_headers).headers_body
                # headers = Substitution.Substitution(url=serverIp).JudgeStatus(ChangeKeyword().ChangeData(Headers.objects.get(id=Step.objects.get(id=test).step_headers).headers_body))
                # print(headers)
                # jsonData = RequestMsg.requestAndresponse(url=serverIp + url, data=body, requestype=Step.objects.get(id=test).request_type, headers=headers)
                allPart = Part.objects.filter(step_id=test)
                requestType = Step.objects.get(id=test).request_type
                getGlobal = Step.objects.get(id=test).get_global
                allAssert = Assert.objects.filter(step_id=test)
                assertList = list()
                for assertData in allAssert:
                    assertDict = dict()
                    assertDict['id'] = assertData.id
                    assertDict['argument'] = assertData.argument
                    assertDict['type'] = assertData.assert_type
                    assertDict['argument_type'] = assertData.argument_type
                    assertDict['value'] = assertData.assert_expect
                    assertList.append(assertDict)
                # print(assertList)
                partList = list()
                for part in allPart:
                    content = dict()
                    content['use_global'] = part.use_global
                    content['urlarument'] = part.argument
                    content['urlindex'] = part.partIndex
                    partList.append(content)
                # print(partList)
                batchList.append([test, serverIp, serverIp + url, body, requestType, getGlobal, partList, assertList])
                # arguments = Parameters.GetParameter(jsondata=jsonData, getarument=partList)
                # print(arguments)
                # print(url, '--->', body)
                # print(headers)
                # print(jsonData)
            # print(batchList)
            dataList = startBath(data=batchList)
            # print(dataList)
            return JsonResponse(msgReturn.Msg().Success(data=dataList), safe=False, json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            return JsonResponse(msgReturn.Msg().Error(msg=str(e)), safe=False, json_dumps_params={'ensure_ascii': False})
