import requests
import urllib3
import json

class RequestMsg:
    def __init__(self):
        super().__init__()

    @staticmethod
    def requestAndresponse(url, data, requestype, headers=None):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        print(url, data, requestype)
        # print(headers)
        if requestype == 'POST':
            if headers in ['', 'null', None]:
                print(data)
                content = requests.post(url=url, json=json.loads(data), verify=False)
                # print(content.json())
                # print(content.text)
            else:
                # print(url, data, requestype)
                content = requests.post(url=url, headers=json.loads(headers), json=json.loads(data), verify=False)
                # print(content.json())
        else:
            if headers is None:
                content = requests.get(url=url, params=data, verify=False)
            else:
                content = requests.get(url=url, params=data, headers=json.loads(headers), verify=False)
        # print(content.json())
        return content.json()
