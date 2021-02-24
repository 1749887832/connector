class RerunAssert:
    def __init__(self):
        super().__init__()

    @classmethod
    def rAssert(cls, assert_name, result):
        try:
            # 判断断言类型和参数类型
            if assert_name['type'] == 'equal':
                if assert_name['argument_type'] == 'int':
                    assert result[0] == int(assert_name['value'])
                elif assert_name['argument_type'] == 'float':
                    assert result[0] == float(assert_name['value'])
                else:
                    assert result[0] == assert_name['value']
            elif assert_name['type'] == 'not_equal':
                if assert_name['argument_type'] == 'int':
                    assert result[0] != int(assert_name['value'])
                elif assert_name['argument_type'] == 'float':
                    assert result[0] != float(assert_name['value'])
                else:
                    assert result[0] != assert_name['value']
            elif assert_name['type'] == 'less':
                if assert_name['argument_type'] == 'int':
                    assert result[0] > int(assert_name['value'])
                elif assert_name['argument_type'] == 'float':
                    assert result[0] > float(assert_name['value'])
                else:
                    assert result[0] > assert_name['value']
            elif assert_name['type'] == 'greater':
                if assert_name['argument_type'] == 'int':
                    assert result[0] < int(assert_name['value'])
                elif assert_name['argument_type'] == 'float':
                    assert result[0] < float(assert_name['value'])
                else:
                    assert result[0] < assert_name['value']
            elif assert_name['type'] == 'less_equal':
                if assert_name['argument_type'] == 'int':
                    assert result[0] <= int(assert_name['value'])
                elif assert_name['argument_type'] == 'float':
                    assert result[0] <= float(assert_name['value'])
                else:
                    assert result[0] <= assert_name['value']
            elif assert_name['type'] == 'greater_equal':
                if assert_name['argument_type'] == 'int':
                    assert result[0] >= int(assert_name['value'])
                elif assert_name['argument_type'] == 'float':
                    assert result[0] >= float(assert_name['value'])
                else:
                    assert result[0] >= assert_name['value']
            elif assert_name['type'] == 'in_to':
                if assert_name['argument_type'] == 'int':
                    assert result[0] in int(assert_name['value'])
                elif assert_name['argument_type'] == 'float':
                    assert result[0] in float(assert_name['value'])
                else:
                    assert result[0] in assert_name['value']
            elif assert_name['type'] == 'not_in':
                if assert_name['argument_type'] == 'int':
                    assert result[0] not in int(assert_name['value'])
                elif assert_name['argument_type'] == 'float':
                    assert result[0] not in float(assert_name['value'])
                else:
                    assert result[0] not in assert_name['value']
            # else:
            #     print('断言失败')
            # print(assert_name['name'], '断言成功')
            return '断言成功'
        except Exception as e:
            print(e)
            # print(assert_name['name'], '断言失败')
            return '断言失败'
