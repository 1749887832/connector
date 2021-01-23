import requests
import urllib3

"""
    author:liuhuangxin
    time:2021年1月23日13:58:52
"""


class Test_Token:
    def __init__(self, request_ip):
        self.ip = request_ip
        self.data = None
        self.url = '/service-user/auth/employee'

    def get_token(self):
        self.data = {"type": "employee", "identityType": 1, "ip": "0.0.0.0", "account": "13555555555", "password": "88888888", "assistant": False}
        urllib3.disable_warnings()
        content = requests.post(url=self.ip + self.url, json=self.data, verify=False)
        token = content.json()['data']['token']
        return 'Bearer ' + token
