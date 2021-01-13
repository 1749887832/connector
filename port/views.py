from django.http import JsonResponse


class Ce:
    def __init__(self):
        super().__init__()
        self.META = None
        self.POST = None

    def Ceshi(self):
        print(self.POST)
        print(self.META.get('HTTP_AUTHORIZATION'))
        print(self.POST.get('username'))
        print(self.POST.get('password'))
        return JsonResponse({'code': '1', 'msg': ' 成功'}, safe=False)
