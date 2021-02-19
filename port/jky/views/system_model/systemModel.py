"""
这是系统模块板块
"""
from django.http import JsonResponse
from port.jky.Controller import msg_return


class systemModel:
    def __init__(self):
        super().__init__()

    def showAllModel(self):
        return JsonResponse(msg_return.Msg().Success(), safe=False)

    def addModel(self):
        return JsonResponse(msg_return.Msg().Success(), safe=False)

    def delModel(self):
        return JsonResponse(msg_return.Msg().Success(), safe=False)

    def updateModel(self):
        return JsonResponse(msg_return.Msg().Success(), safe=False)
