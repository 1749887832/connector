from django.http import JsonResponse
from port.jky.bin.msgDispose import msgReturn, msgCheck
from port.models import Global, GlobalPort, UserProfile


class GlobalHandle:
    def __init__(self):
        super().__init__()
        self.user = None

    @msgCheck.login_check
    def showGlobal(self):
        try:
            show_global = msgCheck.Check_type(self)
            limit = show_global.get('limit')
            page = show_global.get('page')
            start_time = show_global.get('start_time') if show_global.get('start_time') not in ['', None] else '1000-01-01 00:00:00'
            end_time = show_global.get('end_time') if show_global.get('end_time') not in ['', None] else '2099-12-31 23:59:59'
            chose_option = show_global.get('chose_option')
            globalname = show_global.get('globalname')
            all_global = Global.objects.filter(globals_name__contains=globalname, create_time__range=(start_time, end_time), create_user__contains=chose_option)
            globals_data = all_global[limit * (page - 1):limit * page]
            total = len(all_global)
            data = list()
            for i in globals_data:
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
            return JsonResponse(msgReturn.Msg().Success(data=data, total=total), safe=False, json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            return JsonResponse(msgReturn.Msg().Error(code=-1, msg=str(e)), safe=False, json_dumps_params={'ensure_ascii': False})

    # 添加变量
    def addGlobal(self):
        all_global = msgCheck.Check_type(self)
        # 获取变量名
        state_name = all_global.get('statename')
        # 获取使用名
        globalname = all_global.get('globalname')
        # 获取类型
        global_type = all_global.get('globaltype')
        # 获取接口还是函数
        real_type = all_global.get('realtype')
        # 获取参数值
        global_argument = all_global.get('globalagrument')
        # 获取参数类型
        globals_type = all_global.get('globalstyle')
        # 获取描述
        content = all_global.get('content')
        try:
            # 判断使用名是否存在
            if len(Global.objects.filter(use_name=globalname)) != 0:
                return JsonResponse(msgReturn.Msg().Error(msg='使用名已存在!'), safe=False, json_dumps_params={'ensure_ascii': False})
            else:
                if global_type in [0, '0']:
                    # 存固定的变量
                    if msgReturn.JudgeAllIsNull.checkAndReturn(state_name, globalname, global_type, globals_type):
                        add = Global.objects.create(
                            globals_name=state_name,
                            use_name=globalname,
                            globals_type=global_type,
                            use_type=globals_type,
                            cite_arguments=global_argument,
                            create_time=msgReturn.ReturnTime.getNowTime(),
                            content=content,
                            create_user=self.user.id
                        )
                    else:
                        return JsonResponse(msgReturn.Msg().Error(msg='必填项不能为空!'), json_dumps_params={'ensure_ascii': False})
                else:
                    # 存实时的函数
                    if real_type in [0, '0']:
                        # 获取函数名
                        fun_name = all_global.get('funname')
                        if msgReturn.JudgeAllIsNull.checkAndReturn(fun_name, all_global, state_name, globalname, global_type, real_type, globals_type):
                            add = Global.objects.create(
                                globals_name=state_name,
                                use_name=globalname,
                                use_type=globals_type,
                                globals_type=state_name,
                                cite_arguments=fun_name,
                                globals_fun='fun',
                                content=content,
                                create_time=msgReturn.ReturnTime.getNowTime(),
                                create_user=self.user.id
                            )
                        else:
                            return JsonResponse(msgReturn.Msg().Error(msg='必填项不能为空!'), json_dumps_params={'ensure_ascii': False})
                    else:
                        # 获取接口参数
                        url_body = all_global.get('urlbody')
                        # 获取接口ip
                        urlname = all_global.get('urlname')
                        # 获取接口请求方式
                        urltype = all_global.get('urltype')
                        # 获取获取参数
                        getvalue = all_global.get('getvalue')
                        # 获取请求头
                        headers = all_global.get('headers')
                        if msgReturn.JudgeAllIsNull.checkAndReturn(state_name, globalname, global_type, urlname, urltype, url_body, getvalue[0]['urlarument'], getvalue[0]['urlindex']):
                            if headers in ['null', None, '']:
                                globaldata = GlobalPort.objects.create(
                                    globals_url=urlname,
                                    globals_type=urltype,
                                    globals_body=url_body,
                                    globals_argument=getvalue[0]['urlarument'],
                                    globals_index=getvalue[0]['urlindex']
                                )
                            else:
                                globaldata = GlobalPort.objects.create(
                                    globals_url=urlname,
                                    globals_type=urltype,
                                    globals_body=url_body,
                                    globals_headers=headers,
                                    globals_argument=getvalue[0]['urlarument'],
                                    globals_index=getvalue[0]['urlindex']
                                )
                            add = Global.objects.create(
                                use_type=globals_type,
                                globals_name=state_name,
                                use_name=globalname,
                                globals_type=global_type,
                                cite_arguments=globaldata.id,
                                globals_fun='port',
                                content=content,
                                create_time=msgReturn.ReturnTime.getNowTime(),
                                create_user=self.user.id
                            )
                            globaldata.save()
                        else:
                            return JsonResponse(msgReturn.Msg().Error(msg='必填项不能为空!'), json_dumps_params={'ensure_ascii': False})
                add.save()
                return JsonResponse(msgReturn.Msg().Success(data='添加成功'), safe=False, json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            return JsonResponse(msgReturn.Msg().Error(msg=str(e)), safe=False, json_dumps_params={'ensure_ascii': False})

    def deleteGlobal(self):
        try:
            global_id = msgCheck.Check_type(self).get('id')
            # print(global_id)
            globals = Global.objects.get(id=global_id)
            if globals.globals_type == '1' and globals.globals_fun == 'port':
                GlobalPort.objects.filter(id=globals.cite_arguments).delete()
            Global.objects.filter(id=global_id).delete()
            return JsonResponse(msgReturn.Msg().Success(msg='删除成功'), safe=False, json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            return JsonResponse(msgReturn.Msg().Error(msg=str(e)), safe=False, json_dumps_params={'ensure_ascii': False})
