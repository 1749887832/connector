class Replace:
    def __init__(self):
        super().__init__()

    @classmethod
    def locality(cls, chang_data, data_dict):
        # 替换的请求参数中的true或者false，因为true或false是python中的关键字，会导致错误
        if 'true' in chang_data:
            chang_data = chang_data.replace('true', 'True')
        if 'false' in chang_data:
            chang_data = chang_data.replace('false', 'False')
        # 替换掉请求参数中使用的变量
        for i in data_dict:
            chang_data = chang_data.replace(str(i), str(data_dict[i]))
        return chang_data

    @classmethod
    def changType(cls, msg):
        typeDict = {
            'equal': '等于',
            'not_equal': '不等于',
            'less': '小于',
            'greater': '大于',
            'less_equal': '小于等于',
            'greater_equal': '大于等于',
            'in_to': '包含',
            'not_in': '不包含',
        }
        return typeDict[msg]
