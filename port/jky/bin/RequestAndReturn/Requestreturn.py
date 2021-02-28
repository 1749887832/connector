import requests
import urllib3
import json


class RequestMsg:
    def __init__(self):
        super().__init__()

    @staticmethod
    def requestAndResponse(url, data, requestType, headers=None):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        if requestType == 'POST':
            if headers in ['', 'null', None]:
                content = requests.post(url=url, json=json.loads(data), verify=False)
            else:
                content = requests.post(url=url, headers=json.loads(headers), json=json.loads(data), verify=False)
        else:
            if headers is None:
                content = requests.get(url=url, params=data, verify=False)
            else:
                content = requests.get(url=url, params=data, headers=json.loads(headers), verify=False)
        return content.json()
