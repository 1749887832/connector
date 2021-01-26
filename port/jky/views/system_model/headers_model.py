from django.http import JsonResponse

from port.jky.Controller import msg_return, msg_check
from port.models import Headers


class Headers_handle:
    def __init__(self):
        super().__init__()
        self.user = None

    @msg_check.login_check
    def show_headers(self):
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
            return JsonResponse(msg_return.Msg().Success(data=data, total=count), safe=False)
        except Exception as e:
            return JsonResponse(msg_return.Msg().Error(msg=str(e)), safe=False)

    @msg_check.login_check
    def add_headers(self):
        headers = msg_check.Check_type(self)
        header_name = headers.get('header_name')
        header_data = headers.get('header_data')
        header_content = headers.get('header_content')
        try:
            header = Headers.objects.create(
                headers_name=header_name,
                headers_body=header_data,
                headers_content=header_content,
                create_user=self.user.id
            )
            header.save()
            return JsonResponse(msg_return.Msg().Success(), safe=False)
        except Exception as e:
            print(e)
            return JsonResponse(msg_return.Msg().Error(msg=str(e)), safe=False)
