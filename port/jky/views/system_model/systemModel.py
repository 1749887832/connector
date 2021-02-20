"""
这是系统模块板块
"""
from django.http import JsonResponse
from port.jky.Controller import msg_return
from port.models import systemModel, System


class systemModelClass:
    def __init__(self):
        super().__init__()
        self.data = dict()

    def queryModel(self, sysId, modelId=0, dataList=None):
        try:
            allModel = systemModel.objects.filter(systemId=sysId, systemFatherId=modelId)
            if len(allModel) > 0:
                for i in allModel:
                    # print(modelId, '----->', i.systemName)
                    print('this is dataList--->', dataList)
                    if dataList is None:
                        self.data.update({'value': i.id, 'label': i.systemName})
                    else:
                        self.data.update({'children': [{'value': i.id, 'label': i.systemName}]})
                    print('this is self.data-->', self.data)
                    self.queryModel(sysId, i.id, self.data)
        except Exception as e:
            return str(e)

    def showAllModel(self):
        def queryModel(sysId, dataList, modelId=0):
            print(dataList)
            model = systemModel.objects.filter(systemId=sysId, systemFatherId=modelId)
            if len(model) > 0:
                for mo in model:
                    print(mo.systemName)
                    dataList.update({'children': [{'value': mo.id, 'label': mo.systemName}]})
                    queryModel(sysId, dataList['children'][0], mo.id)

        data = dict()
        try:
            allModel = System.objects.all()
            for i in allModel:
                data.update({'value': i.id, 'label': i.system_name,'children':[]})
                print(data)
                queryModel(i.id, data)
                # systemModelClass().queryModel(i.id)
            return JsonResponse(msg_return.Msg().Success(), safe=False)
        except Exception as e:
            return JsonResponse(msg_return.Msg().Error(msg=str(e)), safe=False)

    def addModel(self):
        return JsonResponse(msg_return.Msg().Success(), safe=False)

    def delModel(self):
        return JsonResponse(msg_return.Msg().Success(), safe=False)

    def updateModel(self):
        return JsonResponse(msg_return.Msg().Success(), safe=False)
