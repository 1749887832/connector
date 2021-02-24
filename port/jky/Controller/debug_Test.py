import json

import pytest
import requests
import jsonpath

from port.jky.Controller.ParameterSubstitution.returnassert import RerunAssert

"""
    author:liuhuangxin
    time:2021年1月23日22:05:57
"""


class Test_Debug_Step:
    # 请求信息
    data = list()
    # 响应信息
    response_body = list()
    # 断言参数
    assert_data = list()
    # 断言结果
    assert_result = list()

    # # 参数结果
    # globals_result = list()
    # # 是否获取参数
    # is_delivery = list()

    def setup_class(self):
        self.assert_result = list()
        self.response_body = list()

    def test_case(self):
        # 判断是POST请求还是GET请求
        # if self.data[0].upper() == 'POST':
        #     content = requests.post(url=self.data[1], headers=json.loads(self.data[2]), data=self.data[3], verify=False)
        # else:
        #     content = requests.get(url=self.data[1], headers=json.loads(self.data[2]), params=self.data[3], verify=False)
        # # print(content)
        # Test_Debug_Step().response_body.append(content.json())
        # 循环取出断言
        for assert_name in Test_Debug_Step().assert_data[0]:
            # print(assert_name['name'])
            # print(jsonpath.jsonpath(content.json(), assert_name['name']))
            # 取出断言实际结果
            result = jsonpath.jsonpath(Test_Debug_Step().data[0], assert_name['name'])
            # print(result)
            # 判断断言参数是否存在
            if result:
                # print(assert_name['name'])
                Test_Debug_Step.assert_result.append({'code': 0, 'assert_result': RerunAssert.rAssert(assert_name, result)})
            else:
                # print('找不到该断言参数', assert_name['name'])
                Test_Debug_Step.assert_result.append({'code': -1, 'assert_result': '找不到该断言参数'})

        # Test_Debug_Step().response_body.append(Test_Debug_Step.assert_result)
        # if Test_Debug_Step().is_delivery[0]:
        #     for all_globals in self.data[4]:
        #         global_all = jsonpath.jsonpath(content.json(), all_globals['argument'])
        #         if global_all:
        #             Test_Debug_Step.globals_result.append({'code': 0, 'msg': global_all[int(all_globals['index'])]})
        #         else:
        #             Test_Debug_Step.globals_result.append({'code': -1, 'msg': '没有找到该参数'})
        #     Test_Debug_Step().response_body.append(Test_Debug_Step.globals_result)

    def teardown_class(self):
        self.data = list()
        self.assert_data = list()
        # self.globals_result = list()
        # self.is_delivery = list()


def start(jsondata, assert_name):
    # print(url, headers, request_type, request_body, assert_name)
    start_debug = Test_Debug_Step()
    # print(assert_name)
    start_debug.data.append(jsondata)
    start_debug.assert_data.append(assert_name)
    pytest.main(['port/jky/Controller/debug_Test.py', '-vs'])
    # print(start_debug.response_body)
    return start_debug.assert_result
