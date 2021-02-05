import json

import jsonpath
import requests
import urllib3

from port.jky.Controller.Funstorage import Storage
from port.models import Global, GlobalPort, Headers


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


class Substitution:
    def __init__(self, url=None):
        self.url = url
        self.AllGlobal = GetGlobalsList()
        super().__init__()

    # 判断参数是否使用了全局变量
    def JudgeStatus(self, msg):
        # print(Substitution().AllGlobal)
        for i in Substitution().AllGlobal:
            # print(i['use_name'])
            if i['use_name'] in msg:
                # 执行替换的操作
                data = self.JudgeType(i, msg)
                # print(data)
                msg = self.JudgeStatus(data)
        return msg

    # 判断是实时的还是固定的
    def JudgeType(self, body, msg):
        # print(body, msg)
        if body['use_type'] in [1, '1']:
            msg = self.JudgeFun(body, msg)
        else:
            # msg = msg.replace(body['use_name'], body['cite_arguments'])
            msg = self.JudgeChangeType(body, msg, body['cite_arguments'])
        return msg

    # 判断是函数还是接口
    def JudgeFun(self, body, msg):
        if body['globals_fun'] == 'fun':
            # msg = msg.replace(body['use_name'], getattr(Storage.All_Stoarage(), body['cite_arguments']))
            msg = self.JudgeChangeType(body, msg, getattr(Storage.All_Stoarage(), body['cite_arguments']))
            # print(msg)
        else:
            # print(body, msg)
            msg = self.JudgePort(body, msg)
        return msg

    # 接口获取全局变量
    def JudgePort(self, body, msg):
        globalport = GlobalPort.objects.get(id=body['cite_arguments'])
        # print(globalport)
        # 获取接口的请求头id
        # msg = Substitution().JudgeStatus(body, msg)
        globalsheaders = globalport.globals_headers
        # print(globalsheaders)
        urllib3.disable_warnings()
        # 判断接口是否有请求头
        # print(self.url)
        if globalsheaders is None:
            # 如果没有请求头那么就默认是获取登录的token
            # print(globalport.globals_body)
            jsondata = self.JudgeStatus(globalport.globals_body)
            # print(self.url + globalport.globals_url)
            if globalport.globals_type == 'POST':
                content = requests.post(url=self.url + globalport.globals_url, json=eval(jsondata), verify=False)
            else:
                content = requests.get(url=self.url + globalport.globals_url, params=jsondata, verify=False)
        else:
            # 获取请求头
            globalbody = Headers.objects.get(id=globalsheaders).headers_body
            headers = self.JudgeStatus(globalbody)
            # print(headers)
            # print(globalport.globals_url)
            if globalport.globals_type == 'POST':
                content = requests.post(url=self.url + globalport.globals_url, headers=eval(headers), json=eval(globalport.globals_body.encode('utf-8')), verify=False)
            else:
                content = requests.get(url=self.url + globalport.globals_url, headers=eval(headers), params=globalport.globals_body, verify=False)
        # print(content.json())
        usegloabals = jsonpath.jsonpath(content.json(), globalport.globals_argument)
        # print(usegloabals)
        if usegloabals:
            # msg = msg.replace(body['use_name'], usegloabals[int(globalport.globals_index)])
            msg = self.JudgeChangeType(body, msg, usegloabals[int(globalport.globals_index)])
        else:
            # msg = msg.replace(body['use_name'], 'undefined')
            msg = self.JudgeChangeType(body, msg, 'undefined')
        return msg

    # 判断使用类型
    def JudgeChangeType(self, body, old, new):
        if body['globals_type'] == 'str':
            msg = old.replace(body['use_name'], '"' + str(new) + '"')
        else:
            msg = old.replace(body['use_name'], str(new))
        return msg
