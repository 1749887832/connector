from django.contrib.auth.models import User
from django.http import JsonResponse
from port.jky.Controller import msg_return, msg_check

from port.models import Global, GlobalPort


class Global_handle:
    def __init__(self):
        super().__init__()
        self.user = None

    @msg_check.login_check
    def show_global(self):
        try:
            allglobal = Global.objects.all()
            total = len(allglobal)
            data = list()
            for i in allglobal:
                context = dict()
                context['id'] = i.id
                context['globals_name'] = i.globals_name
                context['use_name'] = i.use_name
                context['globals_type'] = i.globals_type
                context['use_type'] = i.use_type
                context['cite_arguments'] = i.cite_arguments
                context['create_time'] = i.create_time.strftime('%Y-%m-%d %H:%M:%S')
                context['content'] = i.content
                context['create_user'] = i.create_user
                data.append(context)
            return JsonResponse(msg_return.Msg().Success(data=data, total=total), safe=False)
        except Exception as e:
            return JsonResponse(msg_return.Msg().Error(code=-1, msg=str(e)), safe=False)

    # 添加变量
    def add_global(self):
        allglobal = msg_check.Check_type(self)
        # 获取变量名
        statename = allglobal.get('statename')
        # 获取使用名
        globalname = allglobal.get('globalname')
        # 获取类型
        globaltype = allglobal.get('globaltype')
        # 获取接口还是函数
        realtype = allglobal.get('realtype')
        # 获取参数值
        globalagrument = allglobal.get('globalagrument')
        # 获取参数类型
        globalstyle = allglobal.get('globalstyle')
        # 获取描述
        content = allglobal.get('content')
        print(statename, globalname, type(globaltype), type(globalstyle), type(globalstyle))
        try:
            if globaltype in [0, '0']:
                print('this')
                add = Global.objects.create(
                    globals_name=statename,
                    use_name=globalname,
                    globals_type=globaltype,
                    use_type=globalstyle,
                    cite_arguments=globalagrument,
                    create_time=msg_return.ReturnTime.getnowTime(),
                    content=content,
                    create_user=self.user.id
                )
            else:
                print('here')
                if realtype in [0, '0']:
                    add = Global.objects.create(
                        globals_name=statename,
                        use_name=globalname,
                        use_type=globalstyle,
                        globals_type=globaltype,
                        cite_arguments=globalagrument,
                        globals_fun='fun',
                        content=content,
                        create_time=msg_return.ReturnTime.getnowTime(),
                        create_user=self.user.id
                    )
                else:
                    # 获取接口参数
                    urlbody = allglobal.get('urlbody')
                    # 获取接口ip
                    urlname = allglobal.get('urlname')
                    # 获取接口请求方式
                    urltype = allglobal.get('urltype')
                    # 获取获取参数
                    getvalue = allglobal.get('getvalue')
                    # 获取请求头
                    headers = allglobal.get('headers')
                    globaldata = GlobalPort.objects.create(
                        globals_url=urlname,
                        globals_type=urltype,
                        globals_headers=headers if headers is not None else None,
                        globals_body=urlbody,
                        globals_argument=getvalue[0]['urlarument'],
                        globals_index=getvalue[0]['urlindex']
                    )
                    add = Global.objects.create(
                        use_type=globalstyle,
                        globals_name=statename,
                        use_name=globalname,
                        globals_type=globaltype,
                        cite_arguments=globaldata.id,
                        globals_fun='port',
                        content=content,
                        create_time=msg_return.ReturnTime.getnowTime(),
                        create_user=self.user.id
                    )
                    globaldata.save()
            add.save()
            return JsonResponse(msg_return.Msg().Success(data='添加成功'), safe=False)
        except Exception as e:
            return JsonResponse(msg_return.Msg().Error(msg=str(e)), safe=False)
