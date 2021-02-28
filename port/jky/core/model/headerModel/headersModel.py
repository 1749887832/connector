from django.http import JsonResponse
from port.jky.bin.msgDispose import msgReturn, msgCheck
from port.models import Headers


class HeadersHandle:
    def __init__(self):
        super().__init__()

    @msgCheck.login_check
    def showHeaders(self):
        all_headers = Headers.objects.all()
        count = len(all_headers)
        try:
            data = list()
            for header in all_headers:
                content = dict()
                content['id'] = header.id
                content['headers_name'] = header.headers_name
                content['headers_body'] = header.headers_body
                content['headers_content'] = header.headers_content
                data.append(content)
            return JsonResponse(msgReturn.Msg().Success(data=data, total=count), safe=False, json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            return JsonResponse(msgReturn.Msg().Error(msg=str(e)), safe=False, json_dumps_params={'ensure_ascii': False})

    @msgCheck.login_check
    def addHeaders(self):
        headers = msgCheck.Check_type(self)
        header_name = headers.get('header_name')
        header_data = headers.get('header_data')
        header_content = headers.get('header_content')
        try:
            header = Headers.objects.create(
                headers_name=header_name,
                headers_body=header_data,
                headers_content=header_content,
                create_time=msgReturn.ReturnTime.getNowTime(),
                create_user=headers.user_id
            )
            header.save()
            return JsonResponse(msgReturn.Msg().Success(), safe=False, json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            print(e)
            return JsonResponse(msgReturn.Msg().Error(msg=str(e)), safe=False, json_dumps_params={'ensure_ascii': False})
