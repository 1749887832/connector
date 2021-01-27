from port.jky.Controller.Funstorage import Storage
from port.models import Global


class Replace:
    def __init__(self, msg=None, url=None):
        self.msg = msg
        self.url = url
        self.data = list()
        super().__init__()

    def Get_globals(self):
        try:
            all_global = Global.objects.all()
            for i in all_global:
                content = dict()
                content['id'] = i.id
                content['use_name'] = i.use_name
                content['globals_type'] = i.globals_type
                content['use_type'] = i.use_type
                content['cite_arguments'] = i.cite_arguments
                self.data.append(content)
            return self.data
        except Exception as e:
            print(e)

    # 这是替换全局变量
    def Replace_globals(self):
        self.data = self.Get_globals()
        print(self.data)
        try:
            for i in self.data:
                print(i['use_name'])
                # 判断请求body中是否含有全局变量
                if i['use_name'] in self.msg:
                    # 判断使用变量的类型是实时还是固定
                    if i['use_type'] == '1':
                        # 判断使用的变量是int还是str
                        if i['globals_type'] == 'str':
                            print('this')
                            if self.url is None:
                                self.msg = self.msg.replace(i['use_name'], '"' + getattr(Storage.All_Stoarage(), i['cite_arguments']) + '"')
                            else:
                                self.msg = self.msg.replace(i['use_name'], '"' + getattr(Storage.All_Stoarage(ip=self.url), i['cite_arguments']) + '"')
                        elif i['globals_type'] == 'int':
                            if self.url is None:
                                self.msg = self.msg.replace(i['use_name'], getattr(Storage.All_Stoarage(), i['cite_arguments']))
                            else:
                                self.msg = self.msg.replace(i['use_name'], getattr(Storage.All_Stoarage(ip=self.url), i['cite_arguments']))
                    elif i['use_type'] == '0':
                        self.msg = self.msg.replace(i['use_name'], i['cite_arguments'])
                else:
                    continue
            return self.msg
        except Exception as e:
            print(e)
            return self.msg
