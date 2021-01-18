from django.http import JsonResponse

from port.jky.Controller import msg_return
from port.models import Server
from port.jky.Controller import msg_check


class Server_handle:
    def __init__(self):
        super().__init__()
        self.POST = None
        self.GET = None

    @msg_check.login_check
    def show_server(self):
        server_name = msg_return.Msg().ReNone(message=self.GET.get('servername'))
        page = int(self.GET.get('page'))
        limit = int(self.GET.get('limit'))
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
                data.append(content)
            return JsonResponse(msg_return.Msg().Success(data=data, total=total), safe=False)
        except Exception as e:
            print(e)
            return JsonResponse(msg_return.Msg().Error(msg=str(e)), safe=False)

    @msg_check.login_check
    def update_server(self):
        server_id = self.POST.get('id')
        try:
            Server.objects.filter(id=server_id).update(
                server_status=self.POST.get('server_status')
            )
            return JsonResponse(msg_return.Msg().Success(msg='修改成功'), safe=False)
        except Exception as e:
            print(e)
            return JsonResponse(msg_return.Msg().Error(msg=str(e)), safe=False)

    @msg_check.login_check
    def add_server(self):
        print(self.POST)
        servername = self.POST.get('servername')
        serverip = self.POST.get('serverip')
        server_desc = self.POST.get('server_desc')
        try:
            # 判断服务名是否存在
            if len(Server.objects.filter(server_ip=serverip)) == 0:
                new_server = Server.objects.create(
                    server_name=servername,
                    server_ip=serverip,
                    server_describe=server_desc
                )
                new_server.save()
                return JsonResponse(msg_return.Msg().Success(msg='服务IP添加成功'), safe=False)
            else:
                return JsonResponse(msg_return.Msg().Success(code=1001, msg='服务IP已存在，无需新建'), safe=False)
        except Exception as e:
            print(e)
            return JsonResponse(msg_return.Msg().Error(msg=str(e)), safe=False)

    @msg_check.login_check
    def delete_server(self):
        server_id = self.POST.get('id')
        server_ip = self.POST.get('server_ip')
        try:
            if len(Server.objects.filter(id=server_id, server_ip=server_ip)) != 0:
                Server.objects.filter(id=server_id).delete()
                return JsonResponse(msg_return.Msg().Success(msg='删除成功'), safe=False)
            else:
                return JsonResponse(msg_return.Msg().Error(code=1001, msg='无该服务IP'), safe=False)
        except Exception as e:
            return JsonResponse(msg_return.Msg().Error(msg=str(e)), safe=False)

    @msg_check.login_check
    def edit_server(self):
        server_id = self.POST.get('server_id')
        servername = self.POST.get('servername')
        serverip = self.POST.get('serverip')
        server_desc = self.POST.get('server_desc')
        try:
            Server.objects.filter(id=server_id).update(
                server_name=servername,
                server_ip=serverip,
                server_describe=server_desc
            )
            return JsonResponse(msg_return.Msg().Success(msg='修改成功'), safe=False)
        except Exception as e:
            return JsonResponse(msg_return.Msg().Error(code=-1, msg=str(e)), safe=False)
