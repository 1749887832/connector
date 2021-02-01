from port.models import Global


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
                pass
            else:
                continue
        return msg
    # 判断是实时的还是固定的
