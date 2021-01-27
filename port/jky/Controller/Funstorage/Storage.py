import requests
import urllib3


class All_Stoarage:
    def __init__(self, ip=None):
        self.data = None
        self.ip = ip
        self.url = '/service-user/auth/employee'
        self.get_token = self.get_token()
        super().__init__()

    def get_token(self):
        self.data = {"type": "employee", "identityType": 1, "ip": "0.0.0.0", "account": "13555555555", "password": "88888888", "assistant": False}
        urllib3.disable_warnings()
        content = requests.post(url=self.ip + self.url, json=self.data, verify=False)
        token = content.json()['data']['token']
        return 'Bearer ' + token
