import jsonpath


class Parameters:
    def __init__(self):
        super().__init__()

    @staticmethod
    def GetParameter(jsonData, getArgument):
        datalist = list()
        try:
            for i in getArgument:
                msg = jsonpath.jsonpath(jsonData, i['urlarument'])
                if msg:
                    if int(i['urlindex']) == -2:
                        datalist.append({'msg': msg})
                    else:
                        datalist.append({'msg': msg[int(i['urlindex'])]})
                else:
                    datalist.append({'msg': '未找到该参数'})
            return datalist
        except Exception as e:
            return [{'msg': str(e)}]
