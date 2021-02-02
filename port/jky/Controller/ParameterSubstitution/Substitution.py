import jsonpath
import requests
import urllib3

from port.models import Global, GlobalPort


class Substitution:
    def __init__(self):
        self.AllGlobal = self.GetGlobalsList()
        super().__init__()

    @staticmethod
    def GetGlobalsList():
        allglobals = Global.objects.all()
        data = list()
        for allglobal in allglobals:
            content = dict()
            content['id'] = allglobal.id
            content['globals_name'] = allglobal.globals_name
            content['use_name'] = allglobal.use_name
            content['globals_type'] = allglobal.globals_type
            content['use_type'] = allglobal.use_type
            content['globals_fun'] = allglobal.globals_fun
            content['cite_arguments'] = allglobal.cite_arguments
            data.append(content)
        return data

    # 判断参数是否使用了全局变量
    @staticmethod
    def JudgeStatus(msg):
        for i in Substitution().AllGlobal:
            if i['use_name'] in msg:
                # 执行替换的操作
                Substitution().JudgeStatus(Substitution().JudgeType(i, msg))
                pass
        return msg

    # 判断是实时的还是固定的
    @staticmethod
    def JudgeType(body, msg):
        if body['use_type'] == '1':
            msg = Substitution().JudgeFun(body, msg)
        else:
            msg = msg.replace(body['use_name'], body['cite_arguments'])
        return msg

    # 判断是函数还是接口
    @staticmethod
    def JudgeFun(body, msg):
        if body['globals_fun'] == 'fun':
            # msg = msg.replace(body['use_name'],getattr(Storage.All_Stoarage(),body['cite_arguments']))
            pass
        else:
            pass
        return msg

    # 接口获取全局变量
    @staticmethod
    def JudgePort(body, msg):
        globalport = GlobalPort.objects.get(body['cite_arguments'])
        # 获取接口的请求头id
        globalsheaders = globalport.globals_headers
        urllib3.disable_warnings()
        if globalsheaders is None:
            content = requests.post(url=globalport.globals_url, json=globalport.globals_body, verify=False)
            usegloabals = jsonpath.jsonpath(content.json(), body['globals_argument'])
            if usegloabals:
                usegloabals = usegloabals[int(body['globals_index'])]
        if globalport.globals_type == 'POST':
            content = requests.post(url=globalport.globals_url)


if __name__ == '__main__':
    Substitution().JudgeStatus([{'int': '111'}])
