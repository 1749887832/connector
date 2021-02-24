import jsonpath
import pytest

from port.jky.Controller.Funstorage.replace import Replace
from port.jky.Controller.ParameterSubstitution import Substitution
from port.jky.Controller.ParameterSubstitution.keyword import ChangeKeyword
from port.jky.Controller.ParameterSubstitution.returnassert import RerunAssert
from port.jky.Controller.Requestreturns.Requestreturn import RequestMsg
from port.jky.Controller.getparameters.GetParameters import Parameters
from port.models import Headers, Step


class Test_Batch:
    data = list()

    def setup_class(self):
        self.count = dict()
        Test_Batch().data = Test_Batch().data[0]
        # print(Test_Batch().data)
        print('执行这里')

    def teardown_class(self):
        print(self)
        Test_Batch().data = []

    @pytest.mark.parametrize(['stepId', 'serverIp', 'url', 'body', 'requestType', 'isagrument', 'agruments', 'assert_data'], data)
    def test_batch(self, stepId, serverIp, url, body, requestType, isagrument, agruments, assert_data):
        headers = Substitution.Substitution(url=serverIp).JudgeStatus(ChangeKeyword().ChangeData(Headers.objects.get(id=Step.objects.get(id=stepId).step_headers).headers_body))
        jsonData = RequestMsg.requestAndresponse(url=url, data=Replace.locality(body, self.count), requestype=requestType, headers=headers)
        # print(jsonData)
        assertMsg = list()
        for assertData in assert_data:
            result = jsonpath.jsonpath(jsonData, assertData['argument'])
            if result:
                assertMsg.append({'code': 0, 'assert_result': RerunAssert.rAssert(assertData, result)})
            else:
                assertMsg.append({'code': -1, 'assert_result': '找不到该断言参数'})
        if isagrument:
            for argument in agruments:
                self.count[argument['use_global']] = Parameters.GetParameter(jsondata=jsonData, getarument=argument)[0]['msg']
        # print(jsonData, assertMsg, self.count)


def startBath(data):
    for allData in data:
        Test_Batch().data.append(allData)
    # print(data)
    # print(Test_Batch().data[0])
    pytest.main(['port/jky/Controller/ParameterSubstitution/Batchdebug.py'])
