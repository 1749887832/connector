from django.http import JsonResponse
from port.jky.Controller import msg_return, msg_check
from port.jky.Controller.ParameterSubstitution import Substitution
from port.jky.Controller.ParameterSubstitution.Batchdebug import startBath
from port.jky.Controller.ParameterSubstitution.keyword import ChangeKeyword
from port.models import Test, UserProfile, Step, Server, Part, Assert


class Test_handle:
    def __init__(self):
        super().__init__()
        self.body = None
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
            test = msg_check.Check_type(self)
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
            return JsonResponse(msg_return.Msg().Success(data=data, msg='成功', total=total), safe=False)
        except Exception as e:
            return JsonResponse(msg_return.Msg().Error(code=-1, msg=str(e)), safe=False)

    def debugTest(self):
        try:
            allTest = msg_check.Check_type(self)
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
            return JsonResponse(msg_return.Msg().Success(data=dataList), safe=False, json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            return JsonResponse(msg_return.Msg().Error(msg=str(e)), safe=False, json_dumps_params={'ensure_ascii': False})
