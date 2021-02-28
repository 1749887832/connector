from django.contrib.auth.models import User
from django.http import JsonResponse
from port.jky.bin.msgDispose import msgReturn, msgCheck
from port.models import Server, UserProfile


class ServerHandle:
    def __init__(self):
        self.body = None
        super().__init__()

    # 显示所有的服务
    @msgCheck.login_check
    def showServer(self):
        try:
            if len(self.body) == 0:
                all_server = Server.objects.all()
                total = len(all_server)
            else:
                data = msgCheck.Check_type(self)
                server_name = data.get('servername') if data.get('servername') is not None else ''
                page = int(data.get('page'))
                limit = int(data.get('limit'))
                server = Server.objects.filter(server_name__icontains=server_name)
                all_server = server[limit * (page - 1):limit * page]
                total = len(server)
            data = []
            for i in all_server:
                content = dict()
                content['id'] = i.id
                content['name'] = i.server_name
                content['server_ip'] = i.server_ip
                content['server_describe'] = i.server_describe
                content['server_status'] = True if i.server_status == 'true' else False
                content['create_user'] = UserProfile.objects.get(user_id=User.objects.get(id=i.create_user).id).user_name
                content['create_time'] = i.create_time.strftime('%Y-%m-%d')
                data.append(content)
            return JsonResponse(msgReturn.Msg().Success(data=data, total=total), safe=False, json_dumps_params={"ensure_ascii": False})
        except Exception as e:
            print(e)
            return JsonResponse(msgReturn.Msg().Error(msg=str(e)), safe=False, json_dumps_params={'ensure_ascii': False})

    # 修改服务的状态
    @msgCheck.login_check
    def updateServer(self):
        server_id = msgCheck.Check_type(self).get('id')
        try:
            Server.objects.filter(id=server_id).update(
                server_status=str(msgCheck.Check_type(self).get('server_status')).lower()
            )
            return JsonResponse(msgReturn.Msg().Success(msg='修改成功'), safe=False, json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            print(e)
            return JsonResponse(msgReturn.Msg().Error(msg=str(e)), safe=False, json_dumps_params={'ensure_ascii': False})

    # 添加服务
    @msgCheck.login_check
    def addServer(self):
        data = msgCheck.Check_type(self)
        servername = data.get('servername')
        serverip = data.get('serverip')
        server_desc = data.get('server_desc')
        try:
            # 判断服务名是否存在
            if len(Server.objects.filter(server_ip=serverip)) == 0:
                new_server = Server.objects.create(
                    server_name=servername,
                    server_ip=serverip,
                    server_describe=server_desc,
                    create_time=msgReturn.ReturnTime.getNowTime(),
                    create_user=data.user_id
                )
                new_server.save()
                return JsonResponse(msgReturn.Msg().Success(msg='服务IP添加成功'), safe=False, json_dumps_params={'ensure_ascii': False})
            else:
                return JsonResponse(msgReturn.Msg().Success(code=1001, msg='服务IP已存在，无需新建'), safe=False, json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            print(e)
            return JsonResponse(msgReturn.Msg().Error(msg=str(e)), safe=False, json_dumps_params={'ensure_ascii': False})

    # 删除服务
    @msgCheck.login_check
    def deleteServer(self):
        data = msgCheck.Check_type(self)
        server_id = data.get('id')
        server_ip = data.get('server_ip')
        try:
            if len(Server.objects.filter(id=server_id, server_ip=server_ip)) != 0:
                Server.objects.filter(id=server_id).delete()
                return JsonResponse(msgReturn.Msg().Success(msg='删除成功'), safe=False, json_dumps_params={'ensure_ascii': False})
            else:
                return JsonResponse(msgReturn.Msg().Error(code=1001, msg='无该服务IP'), safe=False, json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            return JsonResponse(msgReturn.Msg().Error(msg=str(e)), safe=False, json_dumps_params={'ensure_ascii': False})

    # 修改服务
    @msgCheck.login_check
    def editServer(self):
        data = msgCheck.Check_type(self)
        server_id = data.get('server_id')
        servername = data.get('servername')
        serverip = data.get('serverip')
        server_desc = data.get('server_desc')
        try:
            Server.objects.filter(id=server_id).update(
                server_name=servername,
                server_ip=serverip,
                server_describe=server_desc
            )
            return JsonResponse(msgReturn.Msg().Success(msg='修改成功'), safe=False, json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            return JsonResponse(msgReturn.Msg().Error(code=-1, msg=str(e)), safe=False, json_dumps_params={'ensure_ascii': False})
