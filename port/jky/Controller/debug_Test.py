import pytest
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

    def setup_class(self):
        self.assert_result = list()
        self.response_body = list()

    def test_case(self):
        # 循环取出断言
        for assert_name in Test_Debug_Step().assert_data[0]:
            # 取出断言实际结果
            result = jsonpath.jsonpath(Test_Debug_Step().data[0], assert_name['name'])
            # 判断断言参数是否存在
            if result:
                Test_Debug_Step.assert_result.append(RerunAssert.rAssert(assert_name, result))
            else:
                Test_Debug_Step.assert_result.append({'code': -1, 'assert_result': '找不到该断言参数'})

    def teardown_class(self):
        self.data = list()
        self.assert_data = list()


def start(jsondata, assert_name):
    start_debug = Test_Debug_Step()
    start_debug.data.append(jsondata)
    start_debug.assert_data.append(assert_name)
    pytest.main(['port/jky/Controller/debug_Test.py'])
    return start_debug.assert_result
