import jsonpath


class Parameters:
    def __init__(self):
        super().__init__()

    @staticmethod
    def GetParameter(jsondata, getarument):
        datalist = list()
        try:
            for i in getarument:
                msg = jsonpath.jsonpath(jsondata, i['urlarument'])
                if msg:
                    if int(i['urlindex']) == -2:
                        datalist.append(msg)
                    else:
                        datalist.append({'msg': msg[int(i['urlindex'])]})
                else:
                    continue
            return datalist
        except Exception as e:
            return [{'msg': str(e)}]
