import json

import jsonpath
import requests
import urllib3

from port.jky.bin.Funstorage import Storage
from port.jky.bin.ParameterSubstitution.keyword import ChangeKeyword
from port.models import Global, GlobalPort, Headers


def GetGlobalsList():
    all_globals = Global.objects.all()
    data = list()
    for allGlobal in all_globals:
        content = dict()
        content['id'] = allGlobal.id
        content['globals_name'] = allGlobal.globals_name
        content['use_name'] = allGlobal.use_name
        content['globals_type'] = allGlobal.globals_type
        content['use_type'] = allGlobal.use_type
        content['globals_fun'] = allGlobal.globals_fun
        content['cite_arguments'] = allGlobal.cite_arguments
        data.append(content)
    return data


class Substitution:
    def __init__(self, url=None):
        self.url = url
        self.AllGlobal = GetGlobalsList()
        super().__init__()

    # 判断参数是否使用了全局变量
    def JudgeStatus(self, msg):
        for i in Substitution().AllGlobal:
            if i['use_name'] in msg:
                # 执行替换的操作
                data = self.JudgeType(i, msg)
                msg = self.JudgeStatus(data)
        return msg

    # 判断是实时的还是固定的
    def JudgeType(self, body, msg):
        if body['globals_type'] in [1, '1']:
            msg = self.JudgeFun(body, msg)
        else:
            msg = self.JudgeChangeType(body, msg, body['cite_arguments'])
        return msg

    # 判断是函数还是接口
    def JudgeFun(self, body, msg):
        if body['globals_fun'] == 'fun':
            msg = self.JudgeChangeType(body, msg, getattr(Storage.AllStorages(), body['cite_arguments']))
        else:
            msg = self.JudgePort(body, msg)
        return msg

    def JudgePort(self, body, msg):
        global_port = GlobalPort.objects.get(id=body['cite_arguments'])
        # 获取接口的请求头id
        globals_headers = global_port.globals_headers
        urllib3.disable_warnings()
        # 判断接口是否有请求头
        json_data = self.JudgeStatus(global_port.globals_body)
        if globals_headers in ['', 'null', None]:
            # 如果没有请求头那么就默认是获取登录的token
            if global_port.globals_type == 'POST':
                content = requests.post(url=self.url + global_port.globals_url, json=eval(ChangeKeyword().ChangeData(json_data)), verify=False)
            else:
                content = requests.get(url=self.url + global_port.globals_url, params=eval(ChangeKeyword().ChangeData(json_data)), verify=False)
        else:
            # 获取请求头
            global_body = Headers.objects.get(id=globals_headers).headers_body
            headers = self.JudgeStatus(global_body)
            if global_port.globals_type == 'POST':
                content = requests.post(url=self.url + global_port.globals_url, headers=json.loads(headers), json=eval(ChangeKeyword().ChangeData(json_data)), verify=False)
            else:
                content = requests.get(url=self.url + global_port.globals_url, headers=json.loads(headers), params=eval(ChangeKeyword().ChangeData(json_data)), verify=False)
        use_globals = jsonpath.jsonpath(content.json(), global_port.globals_argument)
        if use_globals:
            msg = self.JudgeChangeType(body, msg, use_globals[int(global_port.globals_index)])
        else:
            msg = self.JudgeChangeType(body, msg, 'undefined')
        return msg

    # 判断使用类型
    @classmethod
    def JudgeChangeType(cls, body, old, new):
        if body['use_type'] == 'str':
            msg = old.replace(body['use_name'], '"' + str(new) + '"')
        else:
            msg = old.replace(body['use_name'], str(new))
        return msg
