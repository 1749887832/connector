from django.contrib.auth.models import User
from django.http import JsonResponse
from port.jky.Controller import msg_return, msg_check

from port.models import Global, GlobalPort, UserProfile


class Global_handle:
    def __init__(self):
        super().__init__()
        self.user = None

    @msg_check.login_check
    def show_global(self):
        try:
            showglobal = msg_check.Check_type(self)
            limit = showglobal.get('limit')
            page = showglobal.get('page')
            start_time = showglobal.get('start_time') if showglobal.get('start_time') not in ['', None] else '1000-01-01 00:00:00'
            end_time = showglobal.get('end_time') if showglobal.get('end_time') not in ['', None] else '2099-12-31 23:59:59'
            chose_option = showglobal.get('chose_option')
            globalname = showglobal.get('globalname')
            allglobal = Global.objects.filter(globals_name__contains=globalname, create_time__range=(start_time, end_time), create_user__contains=chose_option)
            globals = allglobal[limit * (page - 1):limit * page]
            total = len(allglobal)
            data = list()
            for i in globals:
                context = dict()
                context['id'] = i.id
                context['globals_name'] = i.globals_name
                context['use_name'] = i.use_name
                context['globals_type'] = i.globals_type
                context['use_type'] = i.use_type
                context['cite_arguments'] = i.cite_arguments
                context['create_time'] = i.create_time.strftime('%Y-%m-%d %H:%M:%S')
                context['content'] = i.content
                context['create_user'] = UserProfile.objects.get(user_id=i.create_user).user_name
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
            # 判断使用名是否存在
            if len(Global.objects.filter(use_name=globalname)) != 0:
                return JsonResponse(msg_return.Msg().Error(msg='使用名已存在!'), safe=False)
            else:
                if globaltype in [0, '0']:
                    print('this')
                    # 存固定的变量
                    if msg_return.JudgeAllIsNull.checkandreturn(statename, globalname, globaltype, globalstyle):
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
                        return JsonResponse(msg_return.Msg().Error(msg='必填项不能为空!'))
                else:
                    print('here')
                    # 存实时的函数
                    if realtype in [0, '0']:
                        # 获取函数名
                        funname = allglobal.get('funname')
                        if msg_return.JudgeAllIsNull.checkandreturn(funname, allglobal, statename, globalname, globaltype, realtype, globalstyle):
                            add = Global.objects.create(
                                globals_name=statename,
                                use_name=globalname,
                                use_type=globalstyle,
                                globals_type=globaltype,
                                cite_arguments=funname,
                                globals_fun='fun',
                                content=content,
                                create_time=msg_return.ReturnTime.getnowTime(),
                                create_user=self.user.id
                            )
                        else:
                            return JsonResponse(msg_return.Msg().Error(msg='必填项不能为空!'))
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
                        if msg_return.JudgeAllIsNull.checkandreturn(statename, globalname, globaltype, urlname, urltype, urlbody, getvalue[0]['urlarument'], getvalue[0]['urlindex']):
                            if headers in ['null', None, '']:
                                globaldata = GlobalPort.objects.create(
                                    globals_url=urlname,
                                    globals_type=urltype,
                                    globals_body=urlbody,
                                    globals_argument=getvalue[0]['urlarument'],
                                    globals_index=getvalue[0]['urlindex']
                                )
                            else:
                                globaldata = GlobalPort.objects.create(
                                    globals_url=urlname,
                                    globals_type=urltype,
                                    globals_body=urlbody,
                                    globals_headers=headers,
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
                        else:
                            return JsonResponse(msg_return.Msg().Error(msg='必填项不能为空!'))
                add.save()
                return JsonResponse(msg_return.Msg().Success(data='添加成功'), safe=False)
        except Exception as e:
            return JsonResponse(msg_return.Msg().Error(msg=str(e)), safe=False)

    def del_global(self):
        try:
            global_id = msg_check.Check_type(self).get('id')
            print(global_id)
            globals = Global.objects.get(id=global_id)
            if globals.globals_type == '1' and globals.globals_fun == 'port':
                GlobalPort.objects.filter(id=globals.cite_arguments).delete()
            Global.objects.filter(id=global_id).delete()
            return JsonResponse(msg_return.Msg().Success(msg='删除成功'), safe=False)
        except Exception as e:
            return JsonResponse(msg_return.Msg().Error(msg=str(e)), safe=False)
