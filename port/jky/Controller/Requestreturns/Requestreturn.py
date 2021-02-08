import requests
import urllib3


class RequestMsg:
    def __init__(self):
        super().__init__()

    @staticmethod
    def requestAndresponse(url, data, requestype, headers=None):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        print(url, data, requestype)
        if requestype == 'POST':
            if headers in ['', 'null', None]:
                # print(url, data, requestype)
                content = requests.post(url=url, json=eval(data), verify=False)
                # print(content.json())
                # print(content.text)
            else:
                content = requests.post(url=url, headers=eval(headers), json=eval(data), verify=False)
                # print(content.json())
        else:
            if headers is None:
                content = requests.get(url=url, params=data, verify=False)
            else:
                content = requests.get(url=url, params=data, headers=eval(headers), verify=False)
        return content.json()
