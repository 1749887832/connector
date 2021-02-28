import jsonpath
import pytest

from port.jky.bin.Funstorage.replace import Replace
from port.jky.bin.ParameterSubstitution import Substitution
from port.jky.bin.ParameterSubstitution.keyword import ChangeKeyword
from port.jky.bin.ParameterSubstitution.returnassert import RerunAssert
from port.jky.bin.RequestAndReturn.Requestreturn import RequestMsg
from port.jky.bin.getparameters.GetParameters import Parameters
from port.models import Headers, Step


class Test_Batch:
    data = []

    def setup_class(self):
        # print(Test_Batch.data)
        self.count = dict()
        self.dataList = []
        # print('执行这里')

    def teardown_class(self):
        self.data = []

    """
        parametrize中data的问题，后续再看
    """

    # @pytest.mark.parametrize(['stepId', 'serverIp', 'url', 'body', 'requestType', 'isagrument', 'agruments', 'assert_data'], data)
    # def test_batch(self, stepId, serverIp, url, body, requestType, isagrument, agruments, assert_data):
    #     headers = Substitution.Substitution(url=serverIp).JudgeStatus(ChangeKeyword().ChangeData(Headers.objects.get(id=Step.objects.get(id=stepId).step_headers).headers_body))
    #     requestBody = Replace.locality(body, self.count)
    #     jsonData = RequestMsg.requestAndresponse(url=url, data=requestBody, requestype=requestType, headers=headers)
    #     # print(jsonData)
    #     assertMsg = list()
    #     for assertData in assert_data:
    #         result = jsonpath.jsonpath(jsonData, assertData['argument'])
    #         dictionary1 = {
    #             'id': assertData['id'],
    #             'argument': assertData['argument'],
    #             'type': Replace.changType(assertData['type']),
    #             'expect': assertData['value'],
    #             'result': result[0]}
    #         dictionary3 = dictionary1.copy()
    #         if result:
    #             dictionary2 = RerunAssert.rAssert(assertData, result)
    #         else:
    #             dictionary2 = {'code': -1, 'assert_result': '找不到该断言参数'}
    #         dictionary3.update(dictionary2)
    #         assertMsg.append(dictionary3)
    #     if isagrument:
    #         for argument in agruments:
    #             argumentList = list()
    #             argumentList.append(argument)
    #             self.count[argument['use_global']] = Parameters.GetParameter(jsondata=jsonData, getarument=argumentList)[0]['msg']
    #     self.dataList.append({'responseData': jsonData, 'assertData': assertMsg, 'requestType': requestType, 'requestBody': requestBody, 'stepId': stepId})
    #     print(self.dataList)
    # print(jsonData, assertMsg, self.count)

    def test_batch(self):
        for batch in Test_Batch.data:
            stepId = batch[0]
            serverIp = batch[1]
            url = batch[2]
            body = batch[3]
            requestType = batch[4]
            is_argument = batch[5]
            arguments = batch[6]
            assert_data = batch[7]
            headers = Substitution.Substitution(url=serverIp).JudgeStatus(ChangeKeyword().ChangeData(Headers.objects.get(id=Step.objects.get(id=stepId).step_headers).headers_body))
            requestBody = Replace.locality(body, self.count)
            jsonData = RequestMsg.requestAndResponse(url=url, data=requestBody, requestType=requestType, headers=headers)
            # print(jsonData)
            assertMsg = list()
            for assertData in assert_data:
                result = jsonpath.jsonpath(jsonData, assertData['argument'])
                dictionary1 = {
                    'id': assertData['id'],
                    'argument': assertData['argument'],
                    'type': Replace.changType(assertData['type']),
                    'expect': assertData['value'],
                    'result': result[0]}
                dictionary3 = dictionary1.copy()
                if result:
                    dictionary2 = RerunAssert.rAssert(assertData, result)
                else:
                    dictionary2 = {'code': -1, 'assert_result': '找不到该断言参数'}
                dictionary3.update(dictionary2)
                assertMsg.append(dictionary3)
            if is_argument:
                for argument in arguments:
                    argumentList = list()
                    argumentList.append(argument)
                    self.count[argument['use_global']] = Parameters.GetParameter(jsonData=jsonData, getArgument=argumentList)[0]['msg']
            self.dataList.append({'responseData': jsonData, 'assertData': assertMsg, 'requestType': requestType, 'requestBody': requestBody, 'stepId': stepId})


def startBath(data):
    for allData in data:
        Test_Batch().data.append(allData)
    pytest.main(['port/jky/bin/ParameterSubstitution/BatchDebugTest.py'])
    return Test_Batch().dataList
