import pytest
import requests
import jsonpath

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
        # print('执行case', self.data)
        # print(type(self.data[-1]))
        print(type(self.data[-1]))
        content = requests.post(url=self.data[0], headers=self.data[1], json=self.data[-1], verify=False)
        Test_Debug_Step().response_body.append(content.json())
        # print('执行case', Test_Debug_Step().request_body)
        # print(content.json())
        for assert_name in Test_Debug_Step().assert_data[0]:
            # print(content.json())
            # print(assert_name['name'])
            # print(jsonpath.jsonpath(content.json(), assert_name['name']))
            result = jsonpath.jsonpath(content.json(), assert_name['name'])
            print(result)
            # print(result)
            if result:
                # print(assert_name['name'])
                try:
                    if assert_name['type'] == 'equal':
                        assert result[0] == assert_name['value']
                    elif assert_name['type'] == 'not_equal':
                        assert result[0] != assert_name['value']
                    elif assert_name['type'] == 'less':
                        assert result[0] < assert_name['value']
                    elif assert_name['type'] == 'greater':
                        assert result[0] > assert_name['value']
                    elif assert_name['type'] == 'less_equal':
                        assert result[0] <= assert_name['value']
                    elif assert_name['type'] == 'greater_equal':
                        assert result[0] >= assert_name['value']
                    elif assert_name['type'] == 'in_to':
                        assert assert_name['value'] in result
                    elif assert_name['type'] == 'not_in':
                        assert assert_name['value'] not in result
                    # else:
                    #     print('断言失败')
                    print(assert_name['name'], '断言成功')
                    Test_Debug_Step.assert_result.append({'code': 0, 'assert_result': '断言成功'})
                except Exception as e:
                    print(e)
                    print(assert_name['name'], '断言失败')
                    Test_Debug_Step.assert_result.append({'code': -1, 'assert_result': '断言失败'})
            else:
                print('找不到该断言参数', assert_name['name'])
                Test_Debug_Step.assert_result.append({'code': -1, 'assert_result': '找不到该断言参数'})

        Test_Debug_Step.response_body.append(Test_Debug_Step.assert_result)

    def teardown_class(self):
        self.data = list()
        self.assert_data = list()


def start(url, headers, request_type, request_body, assert_name):
    # print(assert_name)
    print(request_type)
    start_debug = Test_Debug_Step()
    start_debug.data.append(url)
    start_debug.data.append(headers)
    start_debug.data.append(request_body)
    start_debug.assert_data.append(assert_name)
    # print('实例化', start_debug.data)
    # print(url, headers, request_type)
    # for i in args:
    #     for j in i:
    #         print(j)
    pytest.main(['port/jky/Controller/debug_Test.py', '-vs'])
    print(start_debug.response_body)
    return start_debug.response_body
