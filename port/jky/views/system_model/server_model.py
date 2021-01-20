from django.http import JsonResponse

from port.jky.Controller import msg_return
from port.models import Server
from port.jky.Controller import msg_check
import datetime


class Server_handle:
    def __init__(self):
        super().__init__()
        self.POST = None
        self.GET = None

    # 显示所有的服务
    @msg_check.login_check
    def show_server(self):
        data = msg_check.Check_type(self)
        server_name = msg_return.Msg().ReNone(message=data.get('username'))
        page = int(data.get('page'))
        limit = int(data.get('limit'))
        try:
            all_server = Server.objects.filter(server_name__icontains=server_name)
            server = all_server[limit * (page - 1):limit * page]
            total = len(all_server)
            data = []
            for i in server:
                content = dict()
                content['id'] = i.id
                content['name'] = i.server_name
                content['server_ip'] = i.server_ip
                content['server_describe'] = i.server_describe
                content['server_status'] = True if i.server_status == 'true' else False
                content['create_time'] = i.create_time.strftime('%Y-%m-%d %H:%M:%S')
                data.append(content)
            return JsonResponse(msg_return.Msg().Success(data=data, total=total), safe=False)
        except Exception as e:
            print(e)
            return JsonResponse(msg_return.Msg().Error(msg=str(e)), safe=False)

    # 修改服务的状态
    @msg_check.login_check
    def update_server(self):
        server_id = msg_check.Check_type(self).get('id')
        try:
            Server.objects.filter(id=server_id).update(
                server_status=str(msg_check.Check_type(self).get('server_status')).lower()
            )
            return JsonResponse(msg_return.Msg().Success(msg='修改成功'), safe=False)
        except Exception as e:
            print(e)
            return JsonResponse(msg_return.Msg().Error(msg=str(e)), safe=False)

    # 添加服务
    @msg_check.login_check
    def add_server(self):
        data = msg_check.Check_type(self)
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
                    create_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                )
                new_server.save()
                return JsonResponse(msg_return.Msg().Success(msg='服务IP添加成功'), safe=False)
            else:
                return JsonResponse(msg_return.Msg().Success(code=1001, msg='服务IP已存在，无需新建'), safe=False)
        except Exception as e:
            print(e)
            return JsonResponse(msg_return.Msg().Error(msg=str(e)), safe=False)

    # 删除服务
    @msg_check.login_check
    def delete_server(self):
        data = msg_check.Check_type(self)
        server_id = data.get('id')
        server_ip = data.get('server_ip')
        try:
            if len(Server.objects.filter(id=server_id, server_ip=server_ip)) != 0:
                Server.objects.filter(id=server_id).delete()
                return JsonResponse(msg_return.Msg().Success(msg='删除成功'), safe=False)
            else:
                return JsonResponse(msg_return.Msg().Error(code=1001, msg='无该服务IP'), safe=False)
        except Exception as e:
            return JsonResponse(msg_return.Msg().Error(msg=str(e)), safe=False)

    # 修改服务
    @msg_check.login_check
    def edit_server(self):
        data = msg_check.Check_type(self)
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
            return JsonResponse(msg_return.Msg().Success(msg='修改成功'), safe=False)
        except Exception as e:
            return JsonResponse(msg_return.Msg().Error(code=-1, msg=str(e)), safe=False)